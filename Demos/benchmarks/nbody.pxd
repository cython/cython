
cimport cython

@cython.locals(x=isize)
fn combinations(list l)

@cython.locals(x1=f64, x2=f64, y1=f64, y2=f64, z1=f64, z2=f64,
               m1=f64, m2=f64, vx=f64, vy=f64, vz=f64, i=i64)
fn advance(f64 dt, i64 n, list bodies=*, list pairs=*)

@cython.locals(x1=f64, x2=f64, y1=f64, y2=f64, z1=f64, z2=f64,
               m=f64, m1=f64, m2=f64, vx=f64, vy=f64, vz=f64)
fn report_energy(list bodies=*, list pairs=*, f64 e=*)

@cython.locals(vx=f64, vy=f64, vz=f64, m=f64)
fn offset_momentum(tuple ref, list bodies=*, f64 px=*, f64 py=*, f64 pz=*)

cpdef test_nbody(i64 iterations)
