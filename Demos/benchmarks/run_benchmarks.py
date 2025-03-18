import collections
import logging
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time


BENCHMARKS_DIR = pathlib.Path(__file__).parent

BENCHMARK_FILES = sorted(BENCHMARKS_DIR.glob("bm_*.py"))

ALL_BENCHMARKS = [bm.stem for bm in BENCHMARK_FILES]


def run(command, cwd=None, pythonpath=None):
    if pythonpath:
        env = os.environ.copy()
        env['PYTHONPATH'] = pythonpath
    else:
        env = None

    try:
        return subprocess.run(command, cwd=str(cwd) if cwd else None, check=True, capture_output=True, env=env)
    except subprocess.CalledProcessError as exc:
        logging.error(f"Command failed: {' '.join(map(str, command))}\nOutput:\n{exc.stderr.decode()}")
        raise


def copy_benchmarks(bm_dir: pathlib.Path, benchmarks=None):
    util_file = BENCHMARKS_DIR / "util.py"
    if util_file.exists():
        shutil.copy(util_file, bm_dir / util_file.name)

    bm_files = []
    for bm_src_file in BENCHMARK_FILES:
        if benchmarks and bm_src_file.stem not in benchmarks:
            continue
        bm_file = bm_dir / bm_src_file.name
        shutil.copy(bm_src_file, bm_file)
        for dep in BENCHMARKS_DIR.glob(bm_src_file.stem + ".pxd"):
            shutil.copy(dep, bm_dir / dep.name)
        bm_files.append(bm_file)

    return bm_files


def compile_benchmarks(cython_dir: pathlib.Path, bm_files: list[pathlib.Path], cythonize_args=None):
    bm_count = len(bm_files)
    rev_hash = get_git_rev(rev_dir=cython_dir)
    bm_list = ', '.join(bm_file.stem for bm_file in bm_files)
    cythonize_args = cythonize_args or []
    logging.info(f"Compiling {bm_count} benchmark{'s' if bm_count != 1 else ''} with Cython gitrev {rev_hash}: {bm_list}")
    run([sys.executable, str(cython_dir / "cythonize.py"), f"-j{bm_count or 1}", "-i", *bm_files, *cythonize_args], cwd=cython_dir)


def get_git_rev(revision=None, rev_dir=None):
    command = ["git", "describe", "--long"]
    if revision:
        command.append(revision)
    output = run(command, cwd=rev_dir)
    _, rev_hash = output.stdout.decode().strip().rsplit('-', 1)
    return rev_hash[1:]


def git_clone(rev_dir, revision):
    rev_hash = get_git_rev(revision)
    run(["git", "clone", "-n", "--no-single-branch", ".", str(rev_dir)])
    run(["git", "checkout", rev_hash], cwd=rev_dir)


def find_benchmark_cname(c_file_path: pathlib.Path):
    module_name = c_file_path.stem
    prefix = f"__pyx_pw_{len(module_name)}{module_name}_"
    with c_file_path.open(encoding='utf8') as c_file:
        for line in c_file:
            if prefix in line and 'run_benchmark(' in line:
                start = line.index(prefix)
                end = line.index('(', start)
                cname = line[start:end]
                if cname.endswith('run_benchmark'):
                    return cname
    raise RuntimeError(f"Failed to find benchmark function in generated C file: {c_file_path.name}")


def copy_profile(bm_dir, module_name, profiler):
    timestamp = int(time.time() * 1000)
    profile_input = bm_dir / "profile.out"
    data_file_name = f"{profiler}_{module_name}_{timestamp:X}.data"

    if profiler == 'callgrind':
        bm_dir_str = str(bm_dir) + os.sep
        with open(profile_input) as data_file_in:
            with open(data_file_name, mode='w') as data_file_out:
                for line in data_file_in:
                    if bm_dir_str in line:
                        # Remove absolute file paths to link to local file copy below.
                        line = line.replace(bm_dir_str, "")
                    data_file_out.write(line)
    else:
        shutil.move(profile_input, data_file_name)

    shutil.move(bm_dir / f"{module_name}.c", f"{module_name}.c")
    for ext in bm_dir.glob(f"{module_name}.*so"):
        shutil.move(str(ext), ext.name)


def run_benchmark(bm_dir, module_name, pythonpath=None, profiler=None):
    logging.info(f"Running benchmark '{module_name}'.")

    repeat = 9
    command = []

    if profiler:
        if profiler == 'perf':
            command = ["perf", "record", "--quiet", "-g", "--branch-any", "--output=profile.out"]
        elif profiler == 'callgrind':
            repeat = 1  # The warmup runs are enough for profiling.
            benchmark_cname = find_benchmark_cname(bm_dir / f"{module_name}.c")
            command = [
                "valgrind", "--tool=callgrind",
                "--dump-instr=yes", "--collect-jumps=yes",
                f"--toggle-collect={benchmark_cname}",
                "--callgrind-out-file=profile.out",
            ]

    command += [sys.executable, "-c", f"import {module_name} as bm; bm.run_benchmark(4); print(bm.run_benchmark({repeat:d}))"]


    output = run(command, cwd=bm_dir, pythonpath=pythonpath)

    if profiler:
        copy_profile(bm_dir, module_name, profiler)

    for line in output.stdout.decode().splitlines():
        if line.startswith('[') and line.endswith(']'):
            timings = [float(t) for t in line[1:-1].split(', ')]
            return timings
    else:
        logging.error(f"Benchmark failed: {module_name}\nOutput:\n{output.stderr.decode()}")
        raise RuntimeError(f"Benchmark failed: {module_name}")


def run_benchmarks(bm_dir, benchmarks, pythonpath=None, profiler=None):
    timings = {}
    for benchmark in benchmarks:
        timings[benchmark] = run_benchmark(bm_dir, benchmark, pythonpath=pythonpath, profiler=profiler)
    return timings


def benchmark_revisions(benchmarks, revisions, cythonize_args=None, profiler=None):
    python_version = "Python %d.%d.%d" % sys.version_info[:3]
    logging.info(f"### Comparing revisions in {python_version}: {' '.join(revisions)}.")

    hashes = {}
    timings = {}
    for revision in revisions:
        plain_python = revision == 'Python'
        revision_name = python_version if plain_python else f"Cython '{revision}'"

        if not plain_python:
            revision_name = f"Cython '{revision}'"
            rev_hash = get_git_rev(revision)
            if rev_hash in hashes:
                logging.info(f"### Ignoring revision '{revision}': same as '{hashes[rev_hash]}'")
                continue

            hashes[rev_hash] = revision

        with tempfile.TemporaryDirectory() as base_dir_str:
            logging.info(f"### Preparing benchmark run for {revision_name}.")
            base_dir = pathlib.Path(base_dir_str)
            cython_dir = base_dir / "cython" / revision
            bm_dir = base_dir / "benchmarks" / revision

            git_clone(cython_dir, revision=revision if revision != 'Python' else None)

            bm_dir.mkdir(parents=True)
            bm_files = copy_benchmarks(bm_dir, benchmarks)
            if not plain_python:
                compile_benchmarks(cython_dir, bm_files, cythonize_args)

            logging.info(f"### Running benchmarks for {revision_name}.")
            pythonpath = cython_dir if plain_python else None
            with_profiler = None if plain_python else profiler
            timings[revision_name] = run_benchmarks(bm_dir, benchmarks, pythonpath=pythonpath, profiler=with_profiler)

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
    for revision_name, bm_timings in rev_timings.items():
        for benchmark, timings in bm_timings.items():
            timings_by_benchmark[benchmark][revision_name] = sorted(timings)

    for benchmark, revision_timings in timings_by_benchmark.items():
        logging.info(f"### Benchmark '{benchmark}' (min/median/max):")
        for revision_name, timings in revision_timings.items():
            tmin, tmed, tmax = timings[0], timings[len(timings)//2], timings[-1]
            logging.info(
                f"    {revision_name[:25]:25} = {format_time(tmin):>12}, {format_time(tmed):>12}, {format_time(tmax):>12}"
            )


def parse_args(args):
    from argparse import ArgumentParser, RawDescriptionHelpFormatter
    parser = ArgumentParser(
        description="Run benchmarks against different Cython tags/revisions.",
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-b", "--benchmarks",
        dest="benchmarks", default=','.join(ALL_BENCHMARKS),
        help="The list of benchmark selectors to run, simple substrings, separated by comma.",
    )
    parser.add_argument(
        "--with-python",
        dest="with_python", action="store_true", default=False,
        help="Also run the benchmarks in plain Python for direct comparison.",
    )
    parser.add_argument(
        "--perf",
        dest="profiler", action="store_const", const="perf", default=None,
        help="Run Linux 'perf record' on the benchmark process.",
    )
    parser.add_argument(
        "--callgrind",
        dest="profiler", action="store_const", const="callgrind", default=None,
        help="Run Valgrind's callgrind profiler on the benchmark process.",
    )
    parser.add_argument(
        "revisions",
        nargs="*", default=[],
        help="The git revisions to check out and benchmark.",
    )

    return parser.parse_known_args(args)


if __name__ == '__main__':
    options, cythonize_args = parse_args(sys.argv[1:])

    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s  %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    benchmark_selectors = set(bm.strip() for bm in options.benchmarks.split(","))
    benchmarks = [bm for bm in ALL_BENCHMARKS if any(selector in bm for selector in benchmark_selectors)]
    if benchmark_selectors and not benchmarks:
        logging.error("No benchmarks selected!")
        sys.exit(1)

    revisions = list({rev: rev for rev in options.revisions})  # deduplicate in order
    if options.with_python:
        revisions.append('Python')
    timings = benchmark_revisions(benchmarks, revisions, cythonize_args, profiler=options.profiler)
    report_revision_timings(timings)
