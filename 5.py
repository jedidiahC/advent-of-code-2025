import sys

# We want to process the ranges, merging them into con
def count_fresh_ingredients(ranges: list[tuple[int, int]]):
    # sort ranges by their start id.
    sorted_ranges = list(sorted(ranges, key=lambda r: r[0]))
    count = 0
    last = -1

    for start, end in sorted_ranges:
        # If the new range ends before the merged range, it completely overlaps with the merged range.
        # this works because the ranges are sorted by their start ids.
        if end <= last:
            continue

        # Here, the new range overlaps with the merged range so, we "extend" the merged range.
        if start <= last:
            count += end - last
        # Otherwise, the new range does not overlap, so we simply add the ids in the new range.
        else:
            count += end - start + 1

        last = max(end, last)

    return count



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

    part_two = count_fresh_ingredients(ranges)

    return part_one, part_two

def parse_input():
    ranges = []
    available_ingredients = []
    is_processing_ranges = True

    for line in sys.stdin:
        if line.strip() == '':
            is_processing_ranges = False
            continue

        if is_processing_ranges:
            ranges.append(tuple(map(int, line.split('-'))))
        else:
            available_ingredients.append(int(line.strip()))

    return (ranges, available_ingredients)

def main():
    ranges, available = parse_input()
    result = solve(ranges, available)
    print(result)

main()
