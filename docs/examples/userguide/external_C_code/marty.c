# marty.c
#include "delorean_api.h"

Vehicle car;

int main(int argc, char *argv[]) {
	Py_Initialize();
	import_delorean();
	car.speed = atoi(argv[1]);
	car.power = atof(argv[2]);
	activate(&car);
	Py_Finalize();
}
