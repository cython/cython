import collections
import logging
import math
import os
import pathlib
import re
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

ALL_BENCHMARKS = [bm.stem for bm in BENCHMARK_FILES] + ['cythonize']

PROCESSED_BENCHMARKS = frozenset({
    "bm_getitem.py",
})

LIMITED_API_VERSION = max((3, 12), sys.version_info[:2])

PYTHON_VERSION = "%d.%d.%d" % sys.version_info[:3]
if hasattr(sys, '_is_gil_enabled') and not sys._is_gil_enabled():
    PYTHON_VERSION += 't'


try:
    from distutils import sysconfig
    DISTUTILS_CFLAGS = sysconfig.get_config_var('CFLAGS')
except ImportError:
    DISTUTILS_CFLAGS = ''


def median(sorted_list: list):
    return sorted_list[len(sorted_list) // 2]


def mean(values: list):
    return math.fsum(values) / len(values)


def run(command, cwd=None, pythonpath=None, c_macros=None, tmp_dir=None, unset_lang=False, capture_stderr=True):
    env = os.environ.copy()
    if pythonpath:
        env['PYTHONPATH'] = pythonpath
    if c_macros:
        env['CFLAGS'] = env.get('CFLAGS', '') + " " + ' '.join(f" -D{macro}" for macro in c_macros)
    if tmp_dir:
        env.update(CCACHE_NOHASHDIR="1",CCACHE_BASEDIR=str(tmp_dir))
    if unset_lang:
        env['LANG'] = ''

    try:
        return subprocess.run(
            command,
            cwd=str(cwd) if cwd else None,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE if capture_stderr else None,
            env=env,
        )
    except subprocess.CalledProcessError as exc:
        logging.error(f"Command failed: {' '.join(map(str, command))}\nOutput:\n{exc.stderr.decode()}")
        raise


def run_timed_python(python_command, **kwargs):
    output = run(['time', sys.executable, *python_command], unset_lang=True, **kwargs)

    parse = re.compile(r"([0-9.:]+)([%\w]+)").findall

    results = {}
    for line in output.stderr.decode().splitlines()[-2:]:
        for number, name in parse(line):
            if ':' in number:
                value = 0
                factor = 1
                for part in number.split(':'):
                    value = value * factor + float(part)
                    factor *= 60
            else:
                value = float(number)
            results[name] = value

    return results


def copy_benchmarks(bm_dir: pathlib.Path, benchmarks=None, cython_version=None):
    util_file = BENCHMARKS_DIR / "util.py"
    if util_file.exists():
        shutil.copy(util_file, bm_dir / util_file.name)

    bm_files = []
    for bm_src_file in BENCHMARK_FILES:
        if benchmarks and bm_src_file.stem not in benchmarks:
            continue
        bm_file = bm_dir / bm_src_file.name

        if cython_version and bm_src_file.name in PROCESSED_BENCHMARKS:
            transform_file(bm_src_file, bm_file, cython_version)
        else:
            shutil.copy(bm_src_file, bm_file)

        for dep in BENCHMARKS_DIR.glob(bm_src_file.stem + ".pxd"):
            shutil.copy(dep, bm_dir / dep.name)
        bm_files.append(bm_file)

    return bm_files


def transform_file(src, dst, cython_version: tuple):
    """
    Uncomment version dependant code while copying the source file.
    """
    target_rev, *cy_version = cython_version
    base_branch = git_branch(src.parent)

    # We consider both a "major.minor" version number and an optional (PR) feature branch name
    # that added a feature.  If we run from that branch, we exclude the commented code
    # on the same (master) version unless we're targeting 'HEAD'.
    parse_conditional_line = re.compile(r'#\[([0-9.]+)([+])(\w*)\][^#]*#(.*)$').match

    lines = []
    with open(src) as f:
        for line in f:
            if line[0] == '#' and line[1] == '[':
                version, min_or_max, branch_added, rest = parse_conditional_line(line).groups()  # error if parsing fails
                assert min_or_max == '+', min_or_max  # currently only min version used
                min_version = list(map(int, version.split('.')))
                if cy_version > min_version or (
                        cy_version == min_version and (branch_added != base_branch or target_rev == 'HEAD')):
                    line = rest.rstrip() + '\n'
            lines.append(line)

    with open(dst, mode='w') as f:
        f.writelines(lines)


def compile_benchmarks(cython_dir: pathlib.Path, bm_files: list[pathlib.Path], cythonize_args=None, c_macros=None, tmp_dir=None):
    bm_count = len(bm_files)
    rev_hash = get_git_rev(rev_dir=cython_dir)
    bm_list = ', '.join(bm_file.stem for bm_file in bm_files)

    util_files = [path for path in {bm_file.parent / "util.py" for bm_file in bm_files} if path.exists()]
    source_files = bm_files + util_files

    logging.info(f"Compiling {bm_count} benchmark{'s' if bm_count != 1 else ''} with Cython gitrev {rev_hash}: {bm_list}")
    times = run_timed_python(
        [str(cython_dir / "cythonize.py"), f"-j{bm_count or 1}", "-i", *source_files, *(cythonize_args or [])],
        cwd=cython_dir,
        c_macros=c_macros,
        tmp_dir=tmp_dir,
    )
    logging.info(f"Compiled {bm_count} benchmark{'s' if bm_count != 1 else ''} in {times['user']:.2f} seconds")
    return times['user']


def compile_shared_benchmarks(cython_dir: pathlib.Path, bm_files: list[pathlib.Path], c_macros=None, tmp_dir=None):
    extensions = "\n".join([f'''Extension("{bm_file.name.split('.')[0]}", ["{bm_file}"]),''' for bm_file in bm_files])
    with open(tmp_dir / 'setup.py', 'w') as setup_file:
        setup_file.write(f'''
from Cython.Build import cythonize
from Cython.Compiler import Options
from setuptools import setup, Extension

extensions = [
    {extensions}
    Extension("_cyutility", sources=["{tmp_dir}/_cyutility.c"]),
]

setup(
  ext_modules = cythonize(extensions, shared_utility_qualified_name = '_cyutility')
)
'''
    )
    rev_hash = get_git_rev(rev_dir=cython_dir)
    bm_list = ', '.join(bm_file.stem for bm_file in bm_files)
    bm_count = len(bm_files)
    logging.info(f"Compiling {bm_count} benchmark{'s' if bm_count != 1 else ''} with Cython gitrev {rev_hash}: {bm_list}")
    times = run_timed_python(
        ["setup.py", "build_ext", "-i"],
        cwd=tmp_dir,
        pythonpath=cython_dir,
        c_macros=c_macros,
        tmp_dir=tmp_dir,
    )
    return times['user']


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


def git_branch(rev_dir):
    output = run(["git", "branch", "--show-current"], cwd=rev_dir)
    return output.stdout.decode().strip()


def read_cython_version(cython_dir: pathlib.Path):
    with open(cython_dir / "Cython" / "Shadow.py") as f:
        for line in f:
            if line[0] == '_' and line.startswith('__version__'):
                return line.partition('=')[2].strip().strip('"\'')
    raise RuntimeError("Cython '__version__' not found in Shadow.py")


def cythonize_cython(cython_dir: pathlib.Path, c_macros=None):
    compiled_modules = [
        "Cython.Plex.Actions",
        "Cython.Plex.Scanners",
        "Cython.Compiler.FlowControl",
        #"Cython.Compiler.LineTable",  # not in base line Cython revision
        "Cython.Compiler.Scanning",
        "Cython.Compiler.Visitor",
        #"Cython.Runtime.refnanny",  # .pyx
        "Cython.Plex.Machines",
        "Cython.Plex.Transitions",
        "Cython.Plex.DFA",
        "Cython.Compiler.Code",
        "Cython.Compiler.FusedNode",
        "Cython.Compiler.Parsing",
        "Cython.Tempita._tempita",
        "Cython.StringIOTree",
        "Cython.Utils",
        "Cython.Compiler.Lexicon",
        "Cython.Compiler.Pythran",
        "Cython.Build.Dependencies",
        "Cython.Compiler.ParseTreeTransforms",
        "Cython.Compiler.Nodes",
        "Cython.Compiler.ExprNodes",
        "Cython.Compiler.ModuleNode",
        "Cython.Compiler.Optimize",
    ]

    source_files = [
        os.path.join(*module.split('.')) + '.py'
        for module in compiled_modules
    ]
    parallel = f'-j{len(source_files)}'

    cythonize_times = {}

    # Cythonize modules in Python.
    times = run_timed_python(["cythonize.py", "-f", parallel, *source_files], cwd=cython_dir)
    t = times['user']
    logging.info(f"    Cythonize modules in Python: {t:.2f} sec user ({times['elapsed']} sec)")
    cythonize_times['cythonize_python'] = [t]

    # Build binary modules (without cythonize).
    # To avoid partially compiled imports, import all non-compiled Cython modules before compiling them.
    pre_imports = ','.join(compiled_modules)
    times = run_timed_python(
        ["-c", f"import {pre_imports}; import setup; setup.run_build()", "build_ext", "-i", parallel, "--cython-compile-minimal"],
        cwd=cython_dir,
        c_macros=c_macros,
    )
    t = times['user']
    logging.info(f"    'setup.py build_ext --cython-compile-minimal' after translation: {t:.2f} sec user ({times['elapsed']} sec)")
    cythonize_times['cythonize_build_ext'] = [t]

    # Cythonize modules with minimal binary Cython.
    times = run_timed_python(["cythonize.py", "-f", parallel, *source_files], cwd=cython_dir)
    t = times['user']
    logging.info(f"    Cythonize modules with minimal compiled Cython: {t:.2f} sec user ({times['elapsed']} sec)")
    cythonize_times['cythonize_compiled_minimal'] = [t]

    # Build binary modules (without cythonize). Time not reported.
    times = run_timed_python(["setup.py", "build_ext", "-i", parallel], cwd=cython_dir, c_macros=c_macros)
    t = times['user']
    logging.info(f"    'setup.py build_ext' after translation: {t:.2f} sec user ({times['elapsed']} sec)")

    # Cythonize modules with binary Cython.
    times = run_timed_python(["cythonize.py", "-f", parallel, *source_files], cwd=cython_dir)
    t = times['user']
    logging.info(f"    Cythonize modules with compiled Cython: {t:.2f} sec user ({times['elapsed']} sec)")
    cythonize_times['cythonize_compiled'] = [t]

    return cythonize_times


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


def autorange(bench_func, python_executable: str = sys.executable, min_runtime=0.25):
    python_command = [python_executable]
    i = 1
    all_timings = bench_func(python_command, repeat=False, scale=i)
    # We put a minimum bar on the fastest run time (to avoid outliers) of the slowest benchmark,
    # assuming that the other sub-benchmarks will be scaled internally.
    min_actual_time = max(min(timings) for timings in all_timings.values())

    # Quickly scale up by factors of 10.
    # Note that this will be increasingly off for fast non-linear benchmarks, so we stop an order away.
    while min_actual_time * 130 < min_runtime:
        i *= 10
        min_actual_time *= 10

    last_min = 0.
    while True:
        for j in 1, 2, 5:
            number = i * j
            all_timings = bench_func(python_command, repeat=False, scale=number)

            min_actual_time = max(min(timings) for timings in all_timings.values())
            if min_actual_time >= min_runtime:
                if (min_actual_time - min_runtime) / (min_actual_time - last_min) > .4:
                    # Avoid large overshoots due to large j steps.
                    number -= i // (3 if j == 1 else 2 if j == 2 else 1)
                return number

            last_min = min_actual_time

        i *= 10


def _make_bench_func(bm_dir, module_name, pythonpath=None):
    def bench_func(python_command: list, repeat: bool, scale: int):
        py_code = f"import {module_name} as bm; bm.run_benchmark({repeat}, 3); print(bm.run_benchmark({repeat}, {scale:d}))"
        command = python_command + ["-c", py_code]

        output = run(command, cwd=bm_dir, pythonpath=pythonpath, capture_stderr=False)

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
    return {
        bm_path.stem: measure_dll_size(bm_path)
        for bm_path in bm_paths
    }


def measure_all_dll_sizes(directory: pathlib.Path, suffix='.so'):
    return {
        so_file.name.partition('.')[0]: measure_dll_size(so_file)
        for so_file in directory.glob(f"**/*{suffix}")
    }


def measure_dll_size(path: pathlib.Path):
    name = path.stem
    dir = path.parent
    stripped_path = dir / f"{name}.stripped"
    # TODO - this'll only work on unix at the moment because it only looks for .so files
    # (but it's unlikely that Windows will have 'strip' either)
    compiled_path, = dir.glob(f"{name}*.so")
    subprocess.run(
        ["strip", compiled_path, "-g", "-o" , stripped_path ]
    )
    stripped_size = stripped_path.stat().st_size
    stripped_path.unlink()
    return stripped_size


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

    scale = autorange(bench_func)

    logging.info(f"Running benchmark '{module_name}' with scale={scale:_d}.")
    timings = bench_func(python_command, repeat=True, scale=scale)

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


def benchmark_revisions(
        benchmarks, revisions, cythonize_args=None, profiler=None,
        cythonize=False, limited_revisions=(), shared_revisions=(), show_size=False):
    python_version = f"Python {PYTHON_VERSION}"
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

        if revision in shared_revisions:
            logging.info(
                f"### Preparing benchmark run for {revision_name} (Shared Cython module).")
            rev_key = 'S-' + revision_name
            timings[rev_key], sizes[rev_key] = benchmark_revision(
                revision, benchmarks, cythonize_args, profiler, plain_python,
                show_size=show_size, use_shared_module=True
            )

    return timings, sizes


def benchmark_revision(
        revision, benchmarks, cythonize_args=None, profiler=None,
        plain_python=False, c_macros=None, show_size=False, use_shared_module=False):
    with_profiler = None if plain_python else profiler

    if with_profiler:
        cythonize_args = (cythonize_args or []) + ['--annotate']

    benchmark_cythonize = 'cythonize' in benchmarks
    if benchmark_cythonize:
        benchmarks = benchmarks[:]
        benchmarks.remove('cythonize')

    with tempfile.TemporaryDirectory() as base_dir_str:
        base_dir = pathlib.Path(base_dir_str)
        cython_dir = base_dir / "cython" / revision
        bm_dir = base_dir / "benchmarks" / revision

        git_clone(cython_dir, revision=None if plain_python else revision)
        cython_version_str = read_cython_version(cython_dir)
        cython_version = (revision, *map(int, cython_version_str.split('.', 2)[:2]))

        cythonize_times = None
        if benchmark_cythonize:
            logging.info(f"### Running cythonize benchmarks for {revision} (Cython {cython_version_str}).")
            cythonize_times = cythonize_cython(cython_dir, c_macros)

        timings = {}
        sizes = {}

        if benchmarks or benchmark_cythonize:
            logging.info(f"### Preparing benchmark run for {revision} (Cython {cython_version_str}).")
            bm_dir.mkdir(parents=True)
            bm_files = copy_benchmarks(bm_dir, benchmarks, cython_version)

            if plain_python:
                # Exclude non-Python modules.
                bm_files = [bm_file for bm_file in bm_files if bm_file.suffix == '.py']
                benchmarks = [bm_file.stem for bm_file in bm_files]
            else:
                if use_shared_module:
                    compile_shared_benchmarks(cython_dir, bm_files, c_macros=c_macros, tmp_dir=bm_dir)
                else:
                    cythonize_time = compile_benchmarks(cython_dir, bm_files, cythonize_args, c_macros=c_macros, tmp_dir=base_dir_str)
                    if benchmark_cythonize:
                        timings['cythonize_benchmarks'] = [cythonize_time]

                if show_size:
                    sizes.update(measure_benchmark_sizes(bm_files))

        if benchmarks:
            logging.info(f"### Running benchmarks for {revision} (Cython {cython_version_str}).")
            pythonpath = cython_dir if plain_python else None
            fresh_timings = run_benchmarks(bm_dir, benchmarks, pythonpath=pythonpath, profiler=with_profiler)
            timings.update(fresh_timings)

        if cythonize_times:
            timings.update(cythonize_times)
        if show_size and benchmark_cythonize:
            sizes.update(measure_all_dll_sizes(cython_dir))

    return timings, (sizes or None)


def report_revision_timings(rev_timings, csv_out=None):
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
            tmin, tmed, tmean, tmax = timings[0], median(timings), mean(timings), timings[-1]
            diff_str = ""
            if base_line != tmed:
                pdiff = tmed * 100 / base_line - 100
                differences[revision_name].append((abs(pdiff), pdiff, tmed - base_line, benchmark))
                diff_str = f"  ({pdiff:+8.1f} %)"
            logging.info(
                f"    {revision_name[:25]:25} = {format_time(tmin):>12}, {format_time(tmed):>12}, {format_time(tmax):>12}{diff_str}"
            )
            if csv_out is not None:
                csv_out.writerow([
                    benchmark, revision_name, PYTHON_VERSION,
                    format_time(tmin), format_time(tmed), format_time(tmean), format_time(tmax),
                    diff_str,
                ])

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
                diff_str = (
                    f'+{format_time(tdiff)}' if tdiff > 1e-9 else
                    f'-{format_time(-tdiff)}' if tdiff < -1e-9 else
                    '±0'
                )
                logging.info(f"    {benchmark[:25]:<25}:  {pdiff:+8.1f} %   /  {diff_str}")


def report_revision_sizes(rev_sizes, csv_out=None):
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
            if csv_out is not None:
                csv_out.writerow([benchmark, revision_name, PYTHON_VERSION, size, diff_str])

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
        "--with-shared-module",
        dest="with_shared_module", action="append", default=[],
        help="Also run the benchmarks for REVISION against the module using shared module.",
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
    parser.add_argument(
        "--report",
        dest="report_csv", default=None, metavar="FILE",
        help="Write a CSV report of the timings to FILE."
    )
    parser.add_argument(
        "--report-size",
        dest="report_sizes_csv", default=None, metavar="FILE",
        help="Write a CSV report of the module sizes to FILE."
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

    revisions = list({rev: rev for rev in (options.revisions + options.with_limited_api + options.with_shared_module)})  # deduplicate in order
    if options.with_python:
        revisions.append('Python')

    show_sizes = bool(options.show_size or options.report_sizes_csv)

    timings, sizes = benchmark_revisions(
        benchmarks, revisions, cythonize_args,
        profiler=options.profiler,
        limited_revisions=options.with_limited_api,
        shared_revisions=options.with_shared_module,
        show_size=show_sizes,
    )

    if options.report_csv:
        with open(options.report_csv, "w") as f:
            import csv
            report_revision_timings(timings, csv_out=csv.writer(f))
    else:
        report_revision_timings(timings)

    if options.report_sizes_csv:
        with open(options.report_sizes_csv, "w") as f:
            import csv
            report_revision_sizes(sizes, csv_out=csv.writer(f))
    elif show_sizes:
        report_revision_sizes(sizes)
