#!/usr/bin/bash

set -x

GCC_VERSION=${GCC_VERSION:=10}

# Set up compilers
if [[ $TEST_CODE_STYLE == "1" ]]; then
  echo "Skipping compiler setup: Code style run"
elif [[ $OSTYPE == "linux-gnu"* && ! "$EXTERNAL_OVERRIDE_CC" ]]; then
  echo "Setting up linux compiler"
  echo "Installing requirements [apt]"
  sudo apt-add-repository -y "ppa:ubuntu-toolchain-r/test"
  sudo apt-get update -y -q
  sudo apt-get install -y -q gdb python3-dbg gcc-$GCC_VERSION || exit 1

  ALTERNATIVE_ARGS=""
  if [[ $BACKEND == *"cpp"* ]]; then
    sudo apt-get install -y -q g++-$GCC_VERSION || exit 1
    ALTERNATIVE_ARGS="--slave /usr/bin/g++ g++ /usr/bin/g++-$GCC_VERSION"
  fi

  sudo apt-get clean

  sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-$GCC_VERSION 60 $ALTERNATIVE_ARGS

  export CC="gcc"
  if [[ $BACKEND == *"cpp"* ]]; then
    sudo update-alternatives --set g++ /usr/bin/g++-$GCC_VERSION
    export CXX="g++"
  fi
elif [[ $OSTYPE == "darwin"* ]]; then
  echo "Setting up macos compiler"
  export CC="clang -Wno-deprecated-declarations"
  export CXX="clang++ -stdlib=libc++ -Wno-deprecated-declarations"
else
  echo "Skipping compiler setup: No setup specified for $OSTYPE"
fi

if [[ $COVERAGE == "1" ]]; then
  echo "Skip setting up compilation caches"
elif [[ $OSTYPE == "msys" ]]; then
  echo "Set up sccache"
  echo "TODO: Make a soft symlink to sccache"
else
  echo "Set up ccache"

  echo "/usr/lib/ccache" >> $GITHUB_PATH  # export ccache to path

  echo "Set up symlinks to ccache"
  cp ccache /usr/local/bin/
  ln -s ccache /usr/local/bin/gcc
  ln -s ccache /usr/local/bin/g++
  ln -s ccache /usr/local/bin/cc
  ln -s ccache /usr/local/bin/c++
  ln -s ccache /usr/local/bin/clang
  ln -s ccache /usr/local/bin/clang++
fi

PYTHON_SYS_VERSION=$(python -c 'import sys; print(sys.version)')

# Log versions in use
echo "===================="
echo "|VERSIONS INSTALLED|"
echo "===================="
echo "Python $PYTHON_SYS_VERSION"

if [[ $CC ]]; then
  which ${CC%% *}
  ${CC%% *} --version
fi

if [[ $CXX ]]; then
  which ${CXX%% *}
  ${CXX%% *} --version
fi

echo "===================="

# Install python requirements
echo "Installing requirements [python]"
if [[ $PYTHON_VERSION == "3.1"[2-9]* || $PYTHON_VERSION == *"-dev" || $PYTHON_VERSION == "pypy-3.11" || $PYTHON_VERSION == "graalpy"* ]]; then
  python -m pip install --no-cache-dir -U pip wheel setuptools || exit 1
else
  # Drop dependencies cryptography and nh3 (purely from twine) when removing support for PyPy3.10.
  python -m pip install --no-cache-dir -U pip "setuptools<60" "wheel<0.46" "twine" "cryptography<42" "nh3<0.2.19" || exit 1
fi
if [[ $PYTHON_VERSION != *"t" && $PYTHON_VERSION != *"t-dev" && $PYTHON_VERSION != "graalpy"* ]]; then
  # twine is not installable on freethreaded Python due to cryptography requirement
  # On GraalPython, it is useless and takes long to install due to its binary dependencies.
  python -m pip install --no-cache-dir -U twine || exit 1
fi
if [[ $PYTHON_VERSION != *"-dev" ]]; then
  python -m pip install --no-cache-dir --pre -r test-requirements.txt || exit 1
elif [[ ! "$SANITIZER_CFLAGS" ]]; then
  # Install packages one by one, allowing failures due to missing recent wheels.
  cat test-requirements.txt | while read package; do python -m pip install --no-cache-dir --pre --only-binary ":all:" "$package" || true; done
fi
if [[ $PYTHON_VERSION == "3.13"* ]]; then
  python -m pip install --no-cache-dir --pre -r test-requirements-313.txt || exit 1
fi
if [[ $PYTHON_VERSION != "pypy"* && $PYTHON_VERSION != "graalpy"* && $PYTHON_VERSION != *"-dev" ]]; then
  python -m pip install --no-cache-dir -r test-requirements-cpython.txt || exit 1
fi

if [[ $TEST_CODE_STYLE == "1" ]]; then
  STYLE_ARGS="--no-unit --no-doctest --no-file --no-pyregr --no-examples"
  python -m pip install --no-cache-dir -r doc-requirements.txt || exit 1
else
  STYLE_ARGS="--no-code-style"

  # Install more requirements
  if [[ $PYTHON_VERSION != *"-dev" ]]; then
    if [[ $BACKEND == *"cpp"* && $OSTYPE != "msys" ]]; then
      python -m pip install --no-cache-dir pythran || exit 1
    fi

    if [[ $BACKEND != "cpp" && $PYTHON_VERSION != "pypy"* && $PYTHON_VERSION != "graalpy"* ]]; then
      python -m pip install --no-cache-dir mypy || exit 1
    fi

  fi
fi

echo "==== Runner resources ===="
df -h

# Run tests
echo "==== Running tests ===="
ccache -s 2>/dev/null || true
export PATH="/usr/lib/ccache:$PATH"

# Most modern compilers allow the last conflicting option
# to override the previous ones, so '-O0 -O3' == '-O3'
# This is true for the latest msvc, gcc and clang
if [[ $OSTYPE == "msys" ]]; then  # for MSVC cl
  # /wd disables warnings
  # 4711 warns that function `x` was selected for automatic inline expansion
  # 4127 warns that a conditional expression is constant, should be fixed here https://github.com/cython/cython/pull/4317
  # (off by default) 5045 warns that the compiler will insert Spectre mitigations for memory load if the /Qspectre switch is specified
  # (off by default) 4820 warns about the code in Python\3.9.6\x64\include ...
  CFLAGS="-Od /Z7 /MP /W4 /wd4711 /wd4127 /wd5045 /wd4820"
elif [[ $OSTYPE == "darwin"* || $CC == "clang" ]]; then
  CFLAGS="-O0 -g2 -Wall -Wextra -Wcast-qual -Wconversion -Wdeprecated -Wunused-result"
else
  CFLAGS="-Og -g2 -Wall -Wextra -Wcast-qual -Wconversion -Wdeprecated -Wunused-result"
fi
# Trying to cover debug assertions in the CI without adding
# extra jobs. Therefore, odd-numbered minor versions of Python
# running C++ jobs get NDEBUG undefined, and even-numbered
# versions running C jobs get NDEBUG undefined.
ODD_VERSION=$(python3 -c "import sys; print(sys.version_info[1]%2)")
if [[ $BACKEND == *"cpp"* && $ODD_VERSION == "1" ]]; then
    CFLAGS="$CFLAGS -UNDEBUG"
elif [[ $ODD_VERSION == "0" ]]; then
    CFLAGS="$CFLAGS -UNDEBUG"
fi

if [[ "$SANITIZER_CFLAGS" ]]; then
    CFLAGS="$CFLAGS $SANITIZER_CFLAGS"
fi

if [[ $NO_CYTHON_COMPILE != "1" && $PYTHON_VERSION != "pypy"* ]]; then

  BUILD_CFLAGS="$CFLAGS -O2"
  if [[ $CYTHON_COMPILE_ALL == "1" && $OSTYPE != "msys" ]]; then
    BUILD_CFLAGS="$CFLAGS -O3 -g0 -mtune=generic"  # make wheel sizes comparable to standard wheel build
  fi

  SETUP_ARGS=""
  if [[ $COVERAGE == "1" ]]; then
    SETUP_ARGS="$SETUP_ARGS --cython-coverage"
  fi
  if [[ $CYTHON_COMPILE_ALL == "1" ]]; then
    SETUP_ARGS="$SETUP_ARGS --cython-compile-all"
  fi
  if [[ $LIMITED_API != "" && $NO_LIMITED_COMPILE != "1" ]]; then
    # in the limited API tests, also build Cython in this mode.
    SETUP_ARGS="$SETUP_ARGS --cython-limited-api"
  fi
  # It looks like parallel build may be causing occasional link failures on Windows
  # "with exit code 1158". DW isn't completely sure of this, but has disabled it in
  # the hope it helps
  SETUP_ARGS="$SETUP_ARGS
    $(python -c 'import sys; print("-j5" if not sys.platform.startswith("win") else "")')"

  CFLAGS=$BUILD_CFLAGS \
    python setup.py build_ext -i $SETUP_ARGS || exit 1

  # COVERAGE can be either "" (empty or not set) or "1" (when we set it)
  if [[ $COVERAGE != "1" && $BACKEND != *"cpp"* && $EXTRA_CFLAGS == "" ]]; then
    python setup.py bdist_wheel || exit 1
    ls -l dist/ || true

    # Check for changelog entry in wheel metadata, except for "...-dev" or "...a0" dev versions.
    grep -q '^__version__.*=.*".*\(a0\|dev[0-9]\?\)"' Cython/Shadow.py || \
      fgrep -q '=======' $( [ -d ?ython-*.dist-info/ ] && echo "?ython-*.dist-info/METADATA" || echo "?ython*.egg-info/PKG-INFO" ) || {
        echo "ERROR: wheel METADATA lacks changelog - did you add a version entry?" ; exit 1; }

    if $( twine --version ); then twine check dist/*.whl; fi
  fi

  echo "Extension modules created during the build:"
  find Cython -name "*.so" -ls | sort -k11
fi

if [[ $TEST_CODE_STYLE == "1" ]]; then
  make -C docs html || exit 1
elif [[ $PYTHON_VERSION != "pypy"* && $OSTYPE != "msys" ]]; then
  # Run the debugger tests in python-dbg if available
  # (but don't fail, because they currently do fail)
  PYTHON_DBG=$(python -c 'import sys; print("%d.%d" % sys.version_info[:2])')
  PYTHON_DBG="python$PYTHON_DBG-dbg"
  if $PYTHON_DBG -V >&2; then
    CFLAGS=$CFLAGS $PYTHON_DBG \
      runtests.py -vv --no-code-style Debugger --backends=$BACKEND
  fi
fi

if [[ $PYTHON_VERSION == "graalpy"* ]]; then
  # [DW] - the Graal JIT and Cython don't seem to get on too well. Disabling the
  # JIT actually makes it faster! And reduces the number of cores each process uses.
  GRAAL_PYTHON_ARGS="--experimental-options --engine.Compilation=false"
  TEST_PARALLELISM=-j2
fi

RUNTESTS_ARGS=""
if [[ $COVERAGE == "1" ]]; then
  RUNTESTS_ARGS="$RUNTESTS_ARGS --coverage --coverage-html --coverage-md --cython-only"
fi
if [[ $TEST_CODE_STYLE != "1" ]]; then
  if [[ ! $TEST_PARALLELISM ]]; then
    TEST_PARALLELISM=-j7
  fi
  RUNTESTS_ARGS="$RUNTESTS_ARGS $TEST_PARALLELISM"
fi


export CFLAGS="$CFLAGS $EXTRA_CFLAGS"
if [[ $PYTHON_VERSION == *"t" ]]; then
  export PYTHON_GIL=0
fi
python $GRAAL_PYTHON_ARGS runtests.py \
  -vv $STYLE_ARGS \
  -x Debugger \
  --backends=$BACKEND \
  $LIMITED_API \
  $SHARED_UTILITY \
  $EXCLUDE \
  $RUNTESTS_ARGS

EXIT_CODE=$?

ccache -s -v -v 2>/dev/null || true

exit $EXIT_CODE
