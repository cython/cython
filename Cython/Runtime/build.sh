# Temporary hacky script, should be replaced
# with distutils-based solution.

#PYTHONINC=/local/include/python2.5
PYTHONINC=/usr/include/python2.5

python ../../cython.py refnanny.pyx
gcc -shared -pthread -fPIC -fwrapv -g -Wall \
  -fno-strict-aliasing -I$PYTHONINC \
  -o refnanny.so -I. refnanny.c
