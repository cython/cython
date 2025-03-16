import collections
import logging
import pathlib
import shutil
import subprocess
import sys
import tempfile


BENCHMARKS_DIR = pathlib.Path(__file__).parent

BENCHMARK_FILES = sorted(BENCHMARKS_DIR.glob("bm_*.py"))


def run(command, cwd=None):
    try:
        return subprocess.run(command, cwd=str(cwd) if cwd else None, check=True, capture_output=True)
    except subprocess.CalledProcessError as exc:
        logging.error(f"Command failed: {' '.join(map(str, command))}\nOutput:\n{exc.stderr.decode()}")
        raise


def compile_benchmarks(cython_dir: pathlib.Path, bm_dir: pathlib.Path, cythonize_args = None):
    cythonize_args = cythonize_args or []

    util_file = BENCHMARKS_DIR / "util.py"
    if util_file.exists():
        shutil.copy(util_file, bm_dir / util_file.name)

    bm_files = []
    for bm_src_file in BENCHMARK_FILES:
        bm_file = bm_dir / bm_src_file.name
        shutil.copy(bm_src_file, bm_file)
        for dep in BENCHMARKS_DIR.glob(bm_src_file.stem + ".pxd"):
            shutil.copy(dep, bm_dir / dep.name)
        bm_files.append(str(bm_file))

    logging.info(f"Compiling benchmarks.")
    run([sys.executable, str(cython_dir / "cythonize.py"), f"-j{len(bm_files) or 1}", "-i", *bm_files, *cythonize_args], cwd=cython_dir)


def git_clone(rev_dir, revision):
    run(["git", "clone", "-n", ".", str(rev_dir)])
    run(["git", "co", revision], cwd=rev_dir)


def run_benchmark(bm_dir, module_name):
    logging.info(f"Running benchmark '{module_name}'.")
    output = run([sys.executable, "-c", f"import {module_name} as bm; bm.run_benchmark(4); print(bm.run_benchmark(9))"], cwd=bm_dir)

    for line in output.stdout.decode().splitlines():
        if line.startswith('[') and line.endswith(']'):
            timings = [float(t) for t in line[1:-1].split(', ')]
            return timings
    else:
        logging.error(f"Benchmark failed: {module_name}\nOutput:\n{output.stderr.decode()}")
        raise RuntimeError(f"Benchmark failed: {module_name}")


def run_benchmarks(bm_dir, benchmarks):
    timings = {}
    for benchmark in benchmarks:
        timings[benchmark] = run_benchmark(bm_dir, benchmark)
    return timings


def benchmark_revisions(benchmarks, revisions, cythonize_args=None):
    timings = {}
    for revision in revisions:
        with tempfile.TemporaryDirectory() as base_dir_str:
            logging.info(f"### Preparing benchmark run for revision '{revision}'.")
            base_dir = pathlib.Path(base_dir_str)
            cython_dir = base_dir / "cython" / revision
            bm_dir = base_dir / "benchmarks" / revision

            git_clone(cython_dir, revision)

            bm_dir.mkdir(parents=True)
            compile_benchmarks(cython_dir, bm_dir, cythonize_args)

            logging.info(f"### Running benchmarks for revision '{revision}'.")
            timings[revision] = run_benchmarks(bm_dir, benchmarks)
    return timings


def report_revision_timings(rev_timings):
    units = {"nsec": 1e-9, "usec": 1e-6, "msec": 1e-3, "sec": 1.0}
    scales = [(scale, unit) for unit, scale in reversed(units.items())]  # biggest first

    def format_time(t):
        for scale, unit in scales:
            if t >= scale:
                break
        else:
            raise RuntimeError("Timing is below nanoseconds: {t:f}")
        return f"{t / scale :.3f} {unit}"

    timings_by_benchmark = collections.defaultdict(dict)
    for revision, bm_timings in sorted(rev_timings.items()):
        for benchmark, timings in bm_timings.items():
            timings_by_benchmark[benchmark][revision] = sorted(timings)

    for benchmark, revision_timings in timings_by_benchmark.items():
        logging.info(f"### Benchmark '{benchmark}' (min/median/max):")
        for revision, timings in revision_timings.items():
            logging.info(f"    {revision[:20]:20} = {format_time(timings[0]):>12}, {format_time(timings[len(timings)//2]):>12}, {format_time(timings[-1]):>12}")


def parse_args(args):
    from argparse import ArgumentParser, RawDescriptionHelpFormatter
    parser = ArgumentParser(
        description="Run benchmarks against different Cython tags/revisions.",
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-r", "--revision",
        dest='revisions', action='append', default=[],
        help="A git revision to check out and benchmark. More than one is allowed.",
    )
    parser.add_argument(
        "benchmarks",
        nargs="*", default=[bm.stem for bm in BENCHMARK_FILES],
    )

    return parser.parse_known_args(args)


if __name__ == '__main__':
    options, cythonize_args = parse_args(sys.argv[1:])

    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s  %(message)s")
    benchmarks = options.benchmarks or ['master']
    timings = benchmark_revisions(benchmarks, options.revisions, cythonize_args)
    report_revision_timings(timings)
