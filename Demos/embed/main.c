#include "Python.h"
#include "embedded.h"

int main(int argc, char *argv) {
  Py_Initialize();
  initembedded();
  spam();
  Py_Finalize();
}
