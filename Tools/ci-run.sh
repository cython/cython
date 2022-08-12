#!/usr/bin/bash

GCC_VERSION=${GCC_VERSION:=8}

# Set up compilers
if [[ $TEST_CODE_STYLE == "1" ]]; then
  echo "Skipping compiler setup"
elif [[ $OSTYPE == "linux-gnu"* ]]; then
  echo "Setting up linux compiler"
  echo "Installing requirements [apt]"
  sudo apt-add-repository -y "ppa:ubuntu-toolchain-r/test"
  sudo apt update -y -q
  sudo apt install -y -q gdb python-dbg python3-dbg gcc-$GCC_VERSION || exit 1

  ALTERNATIVE_ARGS=""
  if [[ $BACKEND == *"cpp"* ]]; then
    sudo apt install -y -q g++-$GCC_VERSION || exit 1
    ALTERNATIVE_ARGS="--slave /usr/bin/g++ g++ /usr/bin/g++-$GCC_VERSION"
  fi
  sudo /usr/sbin/update-ccache-symlinks

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
  echo "No setup specified for $OSTYPE"
fi

echo "/usr/lib/ccache" >> $GITHUB_PATH  # export ccache to path

# Set up miniconda
if [[ $STACKLESS == "true" ]]; then
  echo "Installing stackless python"
  #conda install --quiet --yes nomkl --file=test-requirements.txt --file=test-requirements-cpython.txt
  conda config --add channels stackless
  conda install --quiet --yes stackless || exit 1
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

if [[ $OSTYPE == "msys" ]]; then
  which ccache.exe
  which cl.exe
fi

echo "===================="

# Install python requirements
echo "Installing requirements [python]"
if [[ $PYTHON_VERSION == "2.7"* ]]; then
  pip install wheel || exit 1
  pip install -r test-requirements-27.txt || exit 1
elif [[ $PYTHON_VERSION == "3."[45]* ]]; then
  python -m pip install wheel || exit 1
  python -m pip install -r test-requirements-34.txt || exit 1
else
  python -m pip install -U pip "setuptools<60" wheel || exit 1

  if [[ $PYTHON_VERSION != *"-dev" || $COVERAGE == "1" ]]; then
    python -m pip install -r test-requirements.txt || exit 1

    if [[ $PYTHON_VERSION != "pypy"* && $PYTHON_VERSION != "3."[1]* ]]; then
      python -m pip install -r test-requirements-cpython.txt || exit 1
    fi
  fi
fi

if [[ $TEST_CODE_STYLE == "1" ]]; then
  STYLE_ARGS="--no-unit --no-doctest --no-file --no-pyregr --no-examples"
  python -m pip install -r doc-requirements.txt || exit 1
else
  STYLE_ARGS="--no-code-style"

  # Install more requirements
  if [[ $PYTHON_VERSION != *"-dev" ]]; then
    if [[ $BACKEND == *"cpp"* ]]; then
      echo "WARNING: Currently not installing pythran due to compatibility issues"
      # python -m pip install pythran==0.9.5 || exit 1
    fi

    if [[ $BACKEND != "cpp" && $PYTHON_VERSION != "pypy"* &&
          $PYTHON_VERSION != "2"* && $PYTHON_VERSION != "3.4"* ]]; then
      python -m pip install mypy || exit 1
    fi
  fi
fi

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
  CFLAGS="-Od /Z7 /W4 /wd4711 /wd4127 /wd5045 /wd4820"
else
  CFLAGS="-O0 -ggdb -Wall -Wextra"
fi

if [[ $NO_CYTHON_COMPILE != "1" && $PYTHON_VERSION != "pypy"* ]]; then

  BUILD_CFLAGS="$CFLAGS -O2"
  if [[ $CYTHON_COMPILE_ALL == "1" && $OSTYPE != "msys" ]]; then
    BUILD_CFLAGS="$CFLAGS -O3 -g0 -mtune=generic"  # make wheel sizes comparable to standard wheel build
  fi
  if [[ $PYTHON_SYS_VERSION == "2"* ]]; then
    BUILD_CFLAGS="$BUILD_CFLAGS -fno-strict-aliasing"
  fi

  SETUP_ARGS=""
  if [[ $COVERAGE == "1" ]]; then
    SETUP_ARGS="$SETUP_ARGS --cython-coverage"
  fi
  if [[ $CYTHON_COMPILE_ALL == "1" ]]; then
    SETUP_ARGS="$SETUP_ARGS --cython-compile-all"
  fi
  SETUP_ARGS="$SETUP_ARGS
    $(python -c 'import sys; print("-j5" if sys.version_info >= (3,5) else "")')"

  CFLAGS=$BUILD_CFLAGS \
    python setup.py build_ext -i $SETUP_ARGS || exit 1

  # COVERAGE can be either "" (empty or not set) or "1" (when we set it)
  # STACKLESS can be either  "" (empty or not set) or "true" (when we set it)
  if [[ $COVERAGE != "1" && $STACKLESS != "true" && $BACKEND != *"cpp"* &&
        $LIMITED_API == "" && $EXTRA_CFLAGS == "" ]]; then
    python setup.py bdist_wheel || exit 1
    ls -l dist/ || true
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

RUNTESTS_ARGS=""
if [[ $COVERAGE == "1" ]]; then
  RUNTESTS_ARGS="$RUNTESTS_ARGS --coverage --coverage-html --cython-only"
fi
if [[ $TEST_CODE_STYLE != "1" ]]; then
  RUNTESTS_ARGS="$RUNTESTS_ARGS -j7"
fi

export CFLAGS="$CFLAGS $EXTRA_CFLAGS"
python runtests.py \
  -vv $STYLE_ARGS \
  -x Debugger \
  --backends=$BACKEND \
  $LIMITED_API \
  $EXCLUDE \
  $RUNTESTS_ARGS

EXIT_CODE=$?

ccache -v -v 2>/dev/null

exit $EXIT_CODE
