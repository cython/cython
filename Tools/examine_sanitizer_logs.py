import sys
import re

POS_MATCH = re.compile(r"^[^:]+:\d+:\d+: ")

def check_file(filename) -> int:
    failed_count = 0
    with open(filename) as f:
        for line in f:
            if not POS_MATCH.match(line) or line.startswith("WARNING: ThreadSanitizer"):
                continue
            if line.startswith("conftest.c"):
                # this is in the Python setup - we don't care
                continue
            if "applying zero offset to null pointer" in line:
                # This is OK in C++ and dropped in clang21 (on DW's laptop) so treat it as fine.
                continue
            # anything not specifically included is a failure
            failed_count += 1
            print(line)
    return failed_count

failed_count = 0

if len(sys.argv) == 2 and sys.argv[1].endswith('.*'):
    # No issues so the pattern has not expanded
    print(f"No logs found with pattern '{sys.argv[1]}'")
    exit(0)
for arg in sys.argv[1:]:
    print(f"Looking at file '{arg}':")
    failed_count += check_file(arg)

exit(failed_count)
