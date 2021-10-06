#!/usr/bin/bash

GCC_VERSION=${GCC_VERSION:=8}

# Set up compilers
if [ "${OSTYPE##linux-gnu*}" == "" -a "$TEST_CODE_STYLE" != "1" ]; then
  echo "Installing requirements [apt]"
  sudo apt-add-repository -y "ppa:ubuntu-toolchain-r/test"
  sudo apt update -y -q
  sudo apt install -y -q ccache gdb python-dbg python3-dbg gcc-$GCC_VERSION || exit 1

  ALTERNATIVE_ARGS=""
  if [ -z "${BACKEND##*cpp*}" ]; then
    sudo apt install -y -q g++-$GCC_VERSION || exit 1
    ALTERNATIVE_ARGS="--slave /usr/bin/g++ g++ /usr/bin/g++-$GCC_VERSION"
  fi
  sudo /usr/sbin/update-ccache-symlinks
  echo "/usr/lib/ccache" >> $GITHUB_PATH # export ccache to path

  sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-$GCC_VERSION 60 $ALTERNATIVE_ARGS

  export CC="gcc"
  if [ -z "${BACKEND##*cpp*}" ]; then
    sudo update-alternatives --set g++ /usr/bin/g++-$GCC_VERSION
    export CXX="g++"
  fi
fi
if [ "${OSTYPE##darwin*}" == "" ]; then
  export CC="clang -Wno-deprecated-declarations"
  export CXX="clang++ -stdlib=libc++ -Wno-deprecated-declarations"
fi

# Set up miniconda
if [ "$STACKLESS" == "true" ]; then
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
if [ "$CC" ]; then
  which ${CC%% *}
  ${CC%% *} --version
fi
if [ "$CXX" ]; then
  which ${CXX%% *}
  ${CXX%% *} --version
fi
echo "===================="

# Install python requirements
echo "Installing requirements [python]"
if [ -z "${PYTHON_VERSION##2.7}" ]; then
  pip install wheel || exit 1
  pip install -r test-requirements-27.txt || exit 1
elif [ -z "${PYTHON_VERSION##3.[45]*}" ]; then
  python -m pip install wheel || exit 1
  python -m pip install -r test-requirements-34.txt || exit 1
else
  python -m pip install -U pip setuptools wheel || exit 1

  if [ -n "${PYTHON_VERSION##*-dev}" -o "$COVERAGE" == "1" ]; then
    python -m pip install -r test-requirements.txt || exit 1

    if [ "${PYTHON_VERSION##pypy*}" -a "${PYTHON_VERSION##3.[4789]*}" ]; then
      python -m pip install -r test-requirements-cpython.txt || exit 1
    fi
  fi
fi

if [ "$TEST_CODE_STYLE" == "1" ]; then
  STYLE_ARGS="--no-unit --no-doctest --no-file --no-pyregr --no-examples";
  python -m pip install -r doc-requirements.txt || exit 1
else
  STYLE_ARGS="--no-code-style"

  # Install more requirements
  if [ -n "${PYTHON_VERSION##*-dev}" ]; then
    if [ -z "${BACKEND##*cpp*}" ]; then
      echo "WARNING: Currently not installing pythran due to compatibility issues"
      # python -m pip install pythran==0.9.5 || exit 1
    fi

    if [ "$BACKEND" != "cpp" -a -n "${PYTHON_VERSION##pypy*}" -a
         -n "${PYTHON_VERSION##2*}" -a -n "${PYTHON_VERSION##3.4*}" ]; then
      python -m pip install mypy || exit 1
    fi
  fi
fi

# Run tests
ccache -s 2>/dev/null || true
export PATH="/usr/lib/ccache:$PATH"

if [ "$NO_CYTHON_COMPILE" != "1" -a -n "${PYTHON_VERSION##pypy*}" ]; then

  BUILD_CFLAGS="-O2 -ggdb -Wall -Wextra"
  if [[ $PYTHON_SYS_VERSION == "2"* ]]; then
    BUILD_CFLAGS="$BUILD_CFLAGS -fno-strict-aliasing"
  fi

  SETUP_ARGS=""
  if [ "$COVERAGE" == "1" ]; then
    SETUP_ARGS="$SETUP_ARGS --cython-coverage"
  fi
  if [ "$CYTHON_COMPILE_ALL" == "1" ]; then
    SETUP_ARGS="$SETUP_ARGS --cython-compile-all"
  fi
  SETUP_ARGS="$SETUP_ARGS
    $(python -c 'import sys; print("-j5" if sys.version_info >= (3,5) else "")')"

  CFLAGS=$BUILD_CFLAGS \
    python setup.py build_ext -i $SETUP_ARGS || exit 1

  if [ -z "$COVERAGE" -a -z "$STACKLESS" -a -n "${BACKEND//*cpp*}" -a
       -z "$LIMITED_API" -a -z "$CYTHON_COMPILE_ALL" -a -z "$EXTRA_CFLAGS" ]; then
    python setup.py bdist_wheel || exit 1
  fi
fi

if [ "$TEST_CODE_STYLE" == "1" ]; then
    make -C docs html || exit 1
elif [ -n "${PYTHON_VERSION##pypy*}" ]; then
  # Run the debugger tests in python-dbg if available (but don't fail, because they currently do fail)
  PYTHON_DBG="python$( python -c 'import sys; print("%d.%d" % sys.version_info[:2])' )-dbg"
  if $PYTHON_DBG -V >&2; then CFLAGS="-O0 -ggdb" $PYTHON_DBG runtests.py -vv --no-code-style Debugger --backends=$BACKEND; fi;
fi

export CFLAGS="-O0 -ggdb -Wall -Wextra $EXTRA_CFLAGS"
python runtests.py \
  -vv $STYLE_ARGS \
  -x Debugger \
  --backends=$BACKEND \
   $LIMITED_API \
   $EXCLUDE \
   $(if [ "$COVERAGE" == "1" ]; then echo " --coverage --coverage-html --cython-only"; fi) \
   $(if [ -z "$TEST_CODE_STYLE" ]; then echo " -j7 "; fi)

EXIT_CODE=$?

ccache -s 2>/dev/null || true

exit $EXIT_CODE
