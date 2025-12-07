import sys

# We simply track the x positions where there is a beam.
# The splitter dictionary will store a key(row) to splitter_x_positions
# i.e. { 5: {1, 5} } means that in row 5 we have splitters at x positions 1 and 5.
def solve_part_one(starting_pos: tuple[int, int], boundary: tuple[int, int], splitters: dict[int, set[int]]) -> int:
    current_row = starting_pos[1] + 1
    beams = [starting_pos[0]]
    part_one = 0

    while current_row < boundary[1]:
        next_beams = []

        for beam_x in beams:
            # If the beam encounters a splitter, split.
            if current_row in splitters and beam_x in splitters[current_row]:
                part_one += 1
                for next_beam_x in [beam_x - 1, beam_x + 1]:
                    if next_beam_x not in next_beams and 0 <= next_beam_x < boundary[0]:
                        next_beams.append(next_beam_x)

            # If the beam did not split, continue. but don't double count if merge with split beam.
            elif beam_x not in next_beams:
                next_beams.append(beam_x)

        beams = next_beams
        current_row += 1

    return part_one

# We need to count the total number of unique paths taken by the beam.
# Recursion: 2^splitters per row. 2 choices (left, right). If we brute force, we need to count 2^n.

# DP: we sum up number of ways to reach each x_position on the last row.
def solve_part_two(starting_pos: tuple[int, int], boundary: tuple[int, int], splitters: dict[int, set[int]]):
    current_row = starting_pos[1] + 1
    beams = {starting_pos[0]: 1}

    while current_row < boundary[1]:
        next_beams = {}

        for beam_x in beams:
            # If the beam encounters a splitter, split.
            if current_row in splitters and beam_x in splitters[current_row]:
                for next_beam_x in [beam_x - 1, beam_x + 1]:
                    if 0 <= next_beam_x < boundary[0]:
                        if next_beam_x not in next_beams:
                            next_beams[next_beam_x] = 0

                        next_beams[next_beam_x] += beams[beam_x]

            # If the beam did not split, continue.
            else:
                if beam_x not in next_beams:
                    next_beams[beam_x] = 0

                next_beams[beam_x] += beams[beam_x]

        beams = next_beams
        current_row += 1

    return sum(beams.values())

def parse_input():
    starting_pos = None

    current_row = 0
    x_boundary = None

    splitters = {}

    for line in sys.stdin:
        if starting_pos == None:
            x = line.find('S')

            if x != -1:
                starting_pos = (x, current_row)
                x_boundary = len(line) - 1 # minus one to exclude the line break.

            current_row += 1
            continue

        row_splitters = set()
        for index, char in enumerate(line):
            if char == '^':
                row_splitters.add(index)

        if len(row_splitters) > 0:
            splitters[current_row] = row_splitters

        current_row += 1

    boundary = (x_boundary, current_row)

    return starting_pos, boundary, splitters

def main():
    starting_pos, boundary, splitters = parse_input()
    part_one = solve_part_one(starting_pos, boundary, splitters)
    part_two = solve_part_two(starting_pos, boundary, splitters)

    print(part_one, part_two)

main()
