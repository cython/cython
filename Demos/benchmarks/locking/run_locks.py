import argparse
import locks

parser = argparse.ArgumentParser(
    "run_locks",
    description="This is best run with 'perf stats'. "
                "We aim to minimize both wall-clock time and CPU time (i.e. not spin too hard)")
parser.add_argument("--lock-type", choices=["pymutex", "pythread_type_lock"])
parser.add_argument("--n-threads", type=int, default=4, required=False)
parser.add_argument("--n-iters", type=int, default=1000, required=False)
parser.add_argument("--wait-probability", type=float, default=1.0, required=False)  # as contended as possible
parser.add_argument("--wait-time-ms", type=float, default=1.0, required=False)
parser.add_argument("--idle-time-ms", type=float, default=0.0, required=False)  # immediately try to reacquire

parsed = parser.parse_args()

locks.run(
    parsed.lock_type,
    parsed.n_threads,
    parsed.n_iters,
    parsed.wait_probability,
    parsed.wait_time_ms,
    parsed.idle_time_ms)
