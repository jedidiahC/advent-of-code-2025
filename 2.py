# Brute Force would be to loop through every id in each range and validate id in O(k) time
# k being the total number of digits for a given id

import sys

def is_repeated_x_times(id_str, x) -> bool:
    if len(id_str) % x != 0:
        return False

    # First we check if each letter of a segment
    for i in range(len(id_str) // x):
        # Check each segment
        for j in range(1,x):
            # Check if the letter at position i is the same as the letter at position i + segment length * j
            if id_str[i] != id_str[len(id_str) // x * j + i]:
                return False

    return True

def solve(ranges: list[tuple[int, int]]) -> int:
    part_one = 0
    part_two = 0

    for id_range in ranges:
        for id in range(id_range[0], id_range[1] + 1):
            id_str = str(id)

            if is_repeated_x_times(id_str, 2):
                part_one += id
                part_two += id
                continue

            sieve = [x % 2 != 0 for x in range(len(id_str) + 1)]

            for i in range(3, len(id_str) + 1):
                if not sieve[i]: # Not prime
                    continue

                if is_repeated_x_times(id_str, i):
                    part_two += id
                    break

                # Cross out multiples of i.
                multiple = i
                for multiple in range(i, len(id_str), i):
                    sieve[multiple] = False

    return (part_one, part_two)


def parse_input() -> list[tuple[int, int]]:
    ranges = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        for range_input in line.split(','):
            start, end = map(int, range_input.split('-'))
            ranges.append((start, end))

    return ranges

def main():
    ranges = parse_input()
    result = solve(ranges)
    print(result)

main()
