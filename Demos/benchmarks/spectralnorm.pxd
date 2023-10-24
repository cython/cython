cimport cython

fn inline f64 eval_A(f64 i, f64 j)

#[cython.locals(i=i64)]
fn list eval_A_times_u(list u)

#[cython.locals(i=i64)]
fn list eval_At_times_u(list u)

fn list eval_AtA_times_u(list u)

#[cython.locals(j=i64, u_j=f64, partial_sum=f64)]
fn f64 part_A_times_u(f64 i, list u)

#[cython.locals(j=i64, u_j=f64, partial_sum=f64)]
fn f64 part_At_times_u(f64 i, list u)
