cdef extern from "omp.h":
    ctypedef struct omp_lock_t
    ctypedef struct omp_nest_lock_t

    ctypedef enum omp_sched_t:
        omp_sched_static = 1,
        omp_sched_dynamic = 2,
        omp_sched_guided = 3,
        omp_sched_auto = 4

    extern void omp_set_num_threads(int)
    extern int omp_get_num_threads()
    extern int omp_get_max_threads()
    extern int omp_get_thread_num()
    extern int omp_get_num_procs()

    extern int omp_in_parallel()

    extern void omp_set_dynamic(int)
    extern int omp_get_dynamic()

    extern void omp_set_nested(int)
    extern int omp_get_nested()

    extern void omp_init_lock(omp_lock_t *)
    extern void omp_destroy_lock(omp_lock_t *)
    extern void omp_set_lock(omp_lock_t *)
    extern void omp_unset_lock(omp_lock_t *)
    extern int omp_test_lock(omp_lock_t *)

    extern void omp_init_nest_lock(omp_nest_lock_t *)
    extern void omp_destroy_nest_lock(omp_nest_lock_t *)
    extern void omp_set_nest_lock(omp_nest_lock_t *)
    extern void omp_unset_nest_lock(omp_nest_lock_t *)
    extern int omp_test_nest_lock(omp_nest_lock_t *)

    extern double omp_get_wtime()
    extern double omp_get_wtick()

    void omp_set_schedule(omp_sched_t, int)
    void omp_get_schedule(omp_sched_t *, int *)
    int omp_get_thread_limit()
    void omp_set_max_active_levels(int)
    int omp_get_max_active_levels()
    int omp_get_level()
    int omp_get_ancestor_thread_num(int)
    int omp_get_team_size(int)
    int omp_get_active_level()

