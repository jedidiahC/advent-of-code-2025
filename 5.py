import sys

def solve(ranges: list[tuple[int, int]], available: list[int]) -> int:
    # First, we pre-process the ranges into an ordered dict where the keys are the start of a range.
    # If the start of the range already exists, if the new range is within the old range,
    # otherwise we can extend the end of the old range to the end of the new range.

    # Further optimization can be made if we can always merge overlapping ranges. So how can we detect an overlap?
    # If the end of an old range is within the new range or if the start of the old range.
    # We can use binary search to find the first range that may contain the

    # Brute Force: For every available ingredient, we loop through the ranges, testing whether the ingredient id is within the range.
    part_one = 0
    for id in available:
        for start, end in ranges:
            if start <= id <= end:
                part_one += 1
                break

    return part_one

def parse_input():
    ranges = []
    available_ingredients = []
    is_processing_ranges = True

    for line in sys.stdin:
        if line.strip() == '':
            is_processing_ranges = False
            continue

        if is_processing_ranges:
            ranges.append(list(map(int, line.split('-'))))
        else:
            available_ingredients.append(int(line.strip()))

    return (ranges, available_ingredients)

def main():
    ranges, available = parse_input()
    result = solve(ranges, available)
    print(result)

main()
