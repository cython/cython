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

BENCHMARK_FILES = sorted(
    list(BENCHMARKS_DIR.glob("bm_*.py")) +
    list((BENCHMARKS_DIR.glob("bm_*.pyx")))
)

ALL_BENCHMARKS = [bm.stem for bm in BENCHMARK_FILES]

LIMITED_API_VERSION = max((3, 12), sys.version_info[:2])


try:
    from distutils import sysconfig
    DISTUTILS_CFLAGS = sysconfig.get_config_var('CFLAGS')
except ImportError:
    DISTUTILS_CFLAGS = ''


def median(sorted_list: list):
    return sorted_list[len(sorted_list) // 2]


def run(command, cwd=None, pythonpath=None, c_macros=None):
    env = None
    if pythonpath:
        env = os.environ.copy()
        env['PYTHONPATH'] = pythonpath
    if c_macros:
        env = env or os.environ.copy()
        env['CFLAGS'] = env.get('CFLAGS', '') + " " + ' '.join(f" -D{macro}" for macro in c_macros)

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


def compile_benchmarks(cython_dir: pathlib.Path, bm_files: list[pathlib.Path], cythonize_args=None, c_macros=None):
    bm_count = len(bm_files)
    rev_hash = get_git_rev(rev_dir=cython_dir)
    bm_list = ', '.join(bm_file.stem for bm_file in bm_files)
    cythonize_args = cythonize_args or []
    logging.info(f"Compiling {bm_count} benchmark{'s' if bm_count != 1 else ''} with Cython gitrev {rev_hash}: {bm_list}")
    run(
        [sys.executable, str(cython_dir / "cythonize.py"), f"-j{bm_count or 1}", "-i", *bm_files, *cythonize_args],
        cwd=cython_dir,
        c_macros=c_macros,
    )


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

    for result_file_name in (f"{module_name}.c", f"{module_name}.html"):
        result_file = bm_dir / result_file_name
        if result_file.exists():
            shutil.move(result_file, result_file_name)

    for ext in bm_dir.glob(f"{module_name}.*so"):
        shutil.move(str(ext), ext.name)


def autorange(bench_func, python_executable: str = sys.executable, min_runtime=0.2):
    python_command = [python_executable]
    i = 1
    while True:
        for j in 1, 2, 5, 8:
            number = i * j
            all_timings = bench_func(python_command, 3, number)
            # FIXME: make autorange work per benchchmark, not per file.
            for timings in all_timings.values():
                if min(timings) >= min_runtime:
                    return number
        i *= 10


def _make_bench_func(bm_dir, module_name, pythonpath=None):
    def bench_func(python_command: list, repeat: int, scale: int):
        py_code = f"import {module_name} as bm; bm.run_benchmark(4); print(bm.run_benchmark({repeat:d}, {scale:d}))"
        command = python_command + ["-c", py_code]

        output = run(command, cwd=bm_dir, pythonpath=pythonpath)

        timings = {}

        for line in output.stdout.decode().splitlines():
            name = module_name
            if line.endswith(']') and '[' in line:
                if ':' in line:
                    name, line = line.split(':', 1)
                    name = name.strip()
                    line = line.strip()
                if line.startswith('['):
                    timings[name] = [float(t) for t in line[1:-1].split(',')]

        if not timings:
            logging.error(f"Benchmark failed: {module_name}\nOutput:\n{output.stderr.decode()}")
            raise RuntimeError(f"Benchmark failed: {module_name}")

        return timings

    bench_func.__name__ = module_name
    return bench_func


def measure_benchmark_sizes(bm_paths: list[pathlib.Path]):
    out = {}
    for bm_path in bm_paths:
        name = bm_path.stem
        dir = bm_path.parent
        stripped_path = dir / f"{name}.stripped"
        # TODO - this'll only work on unix at the moment because it only looks for .so files
        # (but it's unlikely that Windows will have 'strip' either)
        compiled_path, = dir.glob(f"{name}*.so")
        subprocess.run(
            ["strip", compiled_path, "-g", "-o" , stripped_path ]
        )
        out[name] = stripped_path.stat().st_size
    return out


def run_benchmark(bm_dir, module_name, pythonpath=None, profiler=None):
    python_command = []
    if profiler:
        if profiler == 'perf':
            python_command = ["perf", "record", "--quiet", "-g", "--output=profile.out"]
        elif profiler == 'callgrind':
            repeat = 1  # The warmup runs are enough for profiling.
            benchmark_cname = find_benchmark_cname(bm_dir / f"{module_name}.c")
            python_command = [
                "valgrind", "--tool=callgrind",
                "--dump-instr=yes", "--collect-jumps=yes",
                f"--toggle-collect={benchmark_cname}",
                "--callgrind-out-file=profile.out",
            ]

    python_command += [sys.executable]

    bench_func = _make_bench_func(bm_dir, module_name, pythonpath)

    repeat = 9
    scale = autorange(bench_func)

    logging.info(f"Running benchmark '{module_name}' with scale={scale:_d}.")
    timings = bench_func(python_command, repeat, scale)

    timings = {name: [t / scale for t in values] for name, values in timings.items()}

    if profiler:
        copy_profile(bm_dir, module_name, profiler)

    return timings


def run_benchmarks(bm_dir, benchmarks, pythonpath=None, profiler=None):
    timings = {}
    for benchmark in benchmarks:
        timings.update(
            run_benchmark(bm_dir, benchmark, pythonpath=pythonpath, profiler=profiler))
    return timings


def benchmark_revisions(benchmarks, revisions, cythonize_args=None, profiler=None, limited_revisions=(), show_size=False):
    python_version = "Python %d.%d.%d" % sys.version_info[:3]
    logging.info(f"### Comparing revisions in {python_version}: {' '.join(revisions)}.")
    logging.info(f"CFLAGS={os.environ.get('CFLAGS', DISTUTILS_CFLAGS)}")

    hashes = {}
    timings = {}
    sizes = {}
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

        logging.info(f"### Preparing benchmark run for {revision_name}.")
        timings[revision_name], sizes[revision_name] = benchmark_revision(
            revision, benchmarks, cythonize_args, profiler, plain_python, show_size=show_size)

        if revision in limited_revisions:
            logging.info(
                f"### Preparing benchmark run for {revision_name} (Limited API {LIMITED_API_VERSION[0]}.{LIMITED_API_VERSION[1]}).")
            rev_key = 'L-' + revision_name
            timings[rev_key], sizes[rev_key] = benchmark_revision(
                revision, benchmarks, cythonize_args, profiler, plain_python,
                c_macros=["Py_LIMITED_API=0x%02x%02x0000" % LIMITED_API_VERSION],
                show_size=show_size,
            )

    return timings, sizes


def benchmark_revision(revision, benchmarks, cythonize_args=None, profiler=None, plain_python=False, c_macros=None, show_size=False):
    with_profiler = None if plain_python else profiler

    if with_profiler:
        cythonize_args = (cythonize_args or []) + ['--annotate']

    with tempfile.TemporaryDirectory() as base_dir_str:
        base_dir = pathlib.Path(base_dir_str)
        cython_dir = base_dir / "cython" / revision
        bm_dir = base_dir / "benchmarks" / revision

        git_clone(cython_dir, revision=None if plain_python else revision)

        bm_dir.mkdir(parents=True)
        bm_files = copy_benchmarks(bm_dir, benchmarks)
        sizes = None
        if plain_python:
            # Exclude non-Python modules.
            bm_files = [bm_file for bm_file in bm_files if bm_file.suffix == '.py']
            benchmarks = [bm_file.stem for bm_file in bm_files]
        else:
            compile_benchmarks(cython_dir, bm_files, cythonize_args, c_macros=c_macros)
            if show_size:
                sizes = measure_benchmark_sizes(bm_files)

        logging.info(f"### Running benchmarks for {revision}.")
        pythonpath = cython_dir if plain_python else None
        timings = run_benchmarks(bm_dir, benchmarks, pythonpath=pythonpath, profiler=with_profiler)
        return timings, sizes


def report_revision_timings(rev_timings):
    units = {"nsec": 1e-9, "usec": 1e-6, "msec": 1e-3, "sec": 1.0}
    scales = [(scale, unit) for unit, scale in reversed(units.items())]  # biggest first

    def format_time(t):
        pos_t = abs(t)
        for scale, unit in scales:
            if pos_t >= scale:
                break
        else:
            raise RuntimeError(f"Timing is below nanoseconds: {t:f}")
        return f"{t / scale :.3f} {unit}"

    timings_by_benchmark = collections.defaultdict(list)
    for revision_name, bm_timings in rev_timings.items():
        for benchmark, timings in bm_timings.items():
            timings_by_benchmark[benchmark].append((revision_name, sorted(timings)))

    differences = collections.defaultdict(list)
    for benchmark, revision_timings in timings_by_benchmark.items():
        logging.info(f"### Benchmark '{benchmark}' (min/median/max/ ±% of median):")

        # Use median as base line to reduce fluctuation.
        base_line_timings = revision_timings[0][1]
        base_line = median(base_line_timings)

        for revision_name, timings in revision_timings:
            tmin, tmed, tmax = timings[0], median(timings), timings[-1]
            diff_str = ""
            if base_line != tmed:
                pdiff = tmed * 100 / base_line - 100
                differences[revision_name].append((abs(pdiff), pdiff, tmed - base_line, benchmark))
                diff_str = f"  ({pdiff:+8.1f} %)"
            logging.info(
                f"    {revision_name[:25]:25} = {format_time(tmin):>12}, {format_time(tmed):>12}, {format_time(tmax):>12}{diff_str}"
            )

    for revision_name, diffs in differences.items():
        diffs.sort(reverse=True)
        diffs_by_sign = {True: [], False: []}
        for diff in diffs:
            diffs_by_sign[diff[1] < 0].append(diff)

        for is_win, diffs in diffs_by_sign.items():
            if not diffs or diffs[0][0] < 1.0:
                continue
            logging.info(f"Largest {'gains' if is_win else 'losses'} for {revision_name}:")
            cutoff = max(1.0, diffs[0][0] // 3)
            for absdiff, pdiff, tdiff, benchmark in diffs:
                if absdiff < cutoff:
                    break
                logging.info(f"    {benchmark[:25]:<25}:  {pdiff:+8.1f} %   /  {'+' if tdiff > 0 else '-'}{format_time(abs(tdiff))}")


def report_revision_sizes(rev_sizes):
    sizes_by_benchmark = collections.defaultdict(list)
    for revision_name, bm_size in rev_sizes.items():
        if bm_size is None:
            continue
        for benchmark, size in bm_size.items():
            sizes_by_benchmark[benchmark].append((revision_name, size))

    pdiffs_by_revision = collections.defaultdict(list)
    for benchmark, sizes in sizes_by_benchmark.items():
        logging.info(f"### Benchmark '{benchmark}' (size):")
        base_line = sizes[0][1]
        for revision_name, size in sizes:
            diff_str = ""
            if base_line != size:
                pdiff = size * 100 / base_line - 100
                pdiffs_by_revision[revision_name].append(pdiff)
                diff_str = f"  ({pdiff:+8.1f} %)"
            logging.info(f"    {revision_name[:25]:25}:  {size} bytes{diff_str}")

    logging.info(f"### Average size changes:")
    for revision_name, pdiffs in pdiffs_by_revision.items():
        average = sum(pdiffs) / len(pdiffs)
        logging.info(f"    {revision_name[:25]:25}:  {average:+8.1f} %")


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
        "--with-limited",
        dest="with_limited_api", action="append", default=[],
        help="Also run the benchmarks for REVISION against the Limited C-API.",
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
    parser.add_argument(
        "--show-size",
        dest="show_size", action="store_true", default=False,
        help="Report the size of the compiled bencharks."
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

    revisions = list({rev: rev for rev in (options.revisions + options.with_limited_api)})  # deduplicate in order
    if options.with_python:
        revisions.append('Python')
    timings, sizes = benchmark_revisions(
        benchmarks, revisions, cythonize_args,
        profiler=options.profiler,
        limited_revisions=options.with_limited_api,
        show_size=options.show_size
    )
    report_revision_timings(timings)
    if options.show_size:
        report_revision_sizes(sizes)
