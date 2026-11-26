# cython: boundscheck=False, wraparound=False

cpdef void integrate(double[::1] restrict x, double[::1] restrict y, double[::1] restrict z,
                     double[::1] restrict vx, double[::1] restrict vy, double[::1] restrict vz,
                     const double[::1] restrict fx, const double[::1] restrict fy,
                     const double[::1] restrict fz, double dt):
    # One integration step for particles stored as separate coordinate arrays.
    # 'restrict' promises that no two of the arrays share memory, so the
    # C compiler can keep values in registers and vectorise the loop.
    cdef Py_ssize_t i
    for i in range(x.shape[0]):
        vx[i] += fx[i] * dt
        vy[i] += fy[i] * dt
        vz[i] += fz[i] * dt
        x[i] += vx[i] * dt
        y[i] += vy[i] * dt
        z[i] += vz[i] * dt
