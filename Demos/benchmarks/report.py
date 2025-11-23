"""
Report benchmark results from CSV files in Markdown format.
"""

import csv
import itertools
import operator


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

    # Sort by benchmark name.
    rows = sorted(reader, key=operator.itemgetter(0))
    return rows


def format_timings(tmin, tmed, tmax, diff):
    return f"{unbreak(tmed)} ({unbreak(diff.strip(' ()'))})" if diff else unbreak(tmed)


def format_sizes(size, diff):
    return f"{size} ({unbreak(diff.strip(' ()'))})" if diff else size


def build_table(rows, title, data_formatter):
    # Collect all revision names and Python versions, keeping their original order.
    # (The set may not be the same for all benchmarks.)
    revisions = list({row[1]: 1 for row in rows})
    python_versions = list({row[2]: 1 for row in rows})

    # Prepare table column mapping and header.
    pos = itertools.count(1)
    column_map = {
        (pyversion, revision):  next(pos)
        for pyversion in python_versions
        for revision in revisions
    }
    header = [title] + [f"Py{pyversion}: {revision[:22]}" for (pyversion, revision) in column_map]
    row_template = [''] * len(header)

    # For each benchmark, report all timings in separate columns.
    table = []
    empty_column_indices = set(column_map.values())
    for benchmark, bm_rows in itertools.groupby(rows, key=operator.itemgetter(0)):
        row = row_template[:]
        table.append(row)

        row[0] = benchmark
        for _, revision_name, pyversion, *data in bm_rows:
            column_index = column_map[(pyversion, revision_name)]
            empty_column_indices.discard(column_index)
            row[column_index] = data_formatter(*data)

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
