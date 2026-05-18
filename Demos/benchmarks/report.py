"""
Report benchmark results from CSV files in Markdown format.
"""

import csv
import itertools
import operator
import re


def unbreak(s):
    return s.replace(' ', '\N{NO-BREAK SPACE}')


def concat_files(csv_files):
    for csv_file in csv_files:
        with open(csv_file) as f:
            yield from f


def read_rows(csv_rows):
    # CSV Formats:
    # - benchmark, revision_name, pyversion, tmin, tmed, tmax, diff
    # - benchmark, revision_name, pyversion, size, diff
    reader = csv.reader(csv_rows)

    # Sort rows by benchmark name.
    rows = sorted(reader, key=operator.itemgetter(0))
    return rows


def time_in_seconds(time_string):
    units = {"nsec": 1e-9, "usec": 1e-6, "msec": 1e-3, "sec": 1.0}
    number, unit = time_string.split()
    return float(number) * units[unit]


def reformat_time(time_string):
    number, unit = time_string.split()
    return f"{float(number) :.2f}\N{NO-BREAK SPACE}{unit}"


def warn_difference(reference, value, max_margin):
    difference = abs(value - reference) / reference
    is_better = value < reference

    if difference < max_margin:
        return ''
    if difference < max_margin * 2:
        return ' \N{BLACK MEDIUM DOWN-POINTING TRIANGLE}' if is_better else ' \N{UP-POINTING RED TRIANGLE}'
    if difference < max_margin * 3:
        return ' \N{LARGE GREEN CIRCLE}' if is_better else ' \N{LARGE RED CIRCLE}'
    else:
        return ' \N{LARGE GREEN SQUARE}' if is_better else ' \N{LARGE RED SQUARE}'


def format_timings(tmin, tmed, tmean, tmax, diff, *, master_data=None, warn_margin=.1/3.):
    warn = warn_difference(time_in_seconds(master_data[0]), time_in_seconds(tmin), warn_margin) if master_data else ''
    diff_str = f" ({unbreak(diff.strip(' ()'))})" if diff else ''
    return f"{reformat_time(tmin)}{diff_str}{warn}"


def format_sizes(size, diff, *, master_data=None, warn_margin=.01):
    warn = warn_difference(int(master_data[0]), int(size), warn_margin) if master_data else ''
    diff_str = f" ({unbreak(diff.strip(' ()'))})" if diff else ''
    return f"{size}{diff_str}{warn}"


def build_table(rows, title, data_formatter):
    # Collect all revision names, keeping their original order.
    # (The set may not be the same for all benchmarks.)
    revisions = list({row[1]: 1 for row in rows})

    # Collect all Python versions, newest first.
    # Relies on sort stability for Limited API / freethreading / etc.
    find_numbers = re.compile(r"(\d+)").findall
    python_versions = sorted(
        {row[2] for row in rows},
        key=lambda s: tuple([-int(d) for d in find_numbers(s)]),
    )

    # Prepare table column mapping and header.
    pos = itertools.count(1)
    column_map = {
        (pyversion, revision):  next(pos)
        for pyversion in python_versions
        for revision in revisions
    }
    header = [title] + [f"Py{pyversion}: {revision.replace('origin/', '')[:16]}" for (pyversion, revision) in column_map]
    row_template = [''] * len(header)

    # For each benchmark, report all timings in separate columns.
    table = []
    empty_column_indices = set(column_map.values())
    for benchmark, bm_rows in itertools.groupby(rows, key=operator.itemgetter(0)):
        row = row_template[:]
        table.append(row)

        bm_rows = [
            (pyversion, revision_name, pyversion + revision_name.split()[0], data)
            for _, revision_name, pyversion, *data in bm_rows
        ]
        master_data_seen = {
            version_key: data
            for _, revision_name, version_key, data in bm_rows
            if 'master' in revision_name
        }

        if benchmark.startswith('bm_'):
            benchmark = benchmark[3:]
        row[0] = benchmark.replace('_', '\N{ZERO WIDTH SPACE}_')  # Allow line breaks in benchmark name.
        for pyversion, revision_name, version_key, data in bm_rows:
            column_index = column_map[(pyversion, revision_name)]
            empty_column_indices.discard(column_index)
            master_data = master_data_seen.get(version_key) if 'HEAD' in revision_name else None
            row[column_index] = data_formatter(*data, master_data=master_data)

    # Strip empty columns, highest to lowest.
    for column_index in sorted(empty_column_indices, reverse=True):
        del header[column_index]
        for row in table:
            del row[column_index]

    return header, table


def generate_markdown(header, table):
    # Size the table columns.
    column_lengths = [
        max(map(len, map(operator.itemgetter(i), itertools.chain([header], table))))
        for i in range(len(header))
    ]

    # Generate Markdown formatted table lines.
    row_format = ("| {:<%ds}" + " | {:>%ds}" * (len(column_lengths) - 1) + " |\n") % tuple(column_lengths)
    format_row = row_format.format

    yield format_row(*header)
    yield format_row(*['-' * length for length in column_lengths])
    yield from itertools.starmap(format_row, table)


def parse_options(args):
    from argparse import ArgumentParser, RawDescriptionHelpFormatter
    parser = ArgumentParser(
        description="Report benchmark numbers as markdown tables.",
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-t", "--type",
        dest="type", default='timings', choices=['timings', 'sizes'],
        help="The type of report.",
    )
    parser.add_argument(
        "csv_files",
        nargs="*", default=[],
        help="The CSV files to collect data from.",
    )

    return parser.parse_args(args)


def main(args):
    options = parse_options(args)

    rows = read_rows(concat_files(options.csv_files))

    if options.type == 'timings':
        title = "Benchmark timings"
        data_formatter = format_timings
    else:
        title = 'Module sizes'
        data_formatter = format_sizes

    header, table = build_table(rows, title, data_formatter)
    for line in generate_markdown(header, table):
        print(line, end='')


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
