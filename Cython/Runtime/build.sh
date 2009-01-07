cat <<EOF > ../../Cython/Compiler/DebugFlags.py
debug_disposal_code = 0
debug_temp_alloc = 0
debug_coercion = 0

debug_refnanny = 0
EOF


python ../../cython.py refnanny.pyx
gcc -shared -pthread -fPIC -fwrapv -O2 -Wall \
  -fno-strict-aliasing -I/local/include/python2.5 \
  -o refnanny.so -I. refnanny.c

cat <<EOF > ../../Cython/Compiler/DebugFlags.py
debug_disposal_code = 0
debug_temp_alloc = 0
debug_coercion = 0

debug_refnanny = 1
EOF
