import sys

wrong_part_two = {
    6675,
    6844,
    4406
}

# Input comes in the form of line break separated L1, R2
# We parse this into a list of integers, where L is negative and R is positive
def parse_input() -> list[int]:
    rotations = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        direction = line[0]
        distance = int(line[1:])

        if direction == 'L':
            rotations.append(-distance)
        elif direction == 'R':
            rotations.append(distance)

    return rotations


def solve(rotations: list[int]):
    part_one = 0 # Number of times we land on 0
    part_two = 0 # Number of times passed through 0

    current_position = 50

    for rotation in rotations:
        # Check how many times we make a full rotation from the start point.
        part_two += (abs(rotation) // 100)

        # If there is less than a full rotation left, check if we pass through 0.

        # if we end exactly on 0,
        # when rotation > 0 current_position + rotation % 100 == 100
        # when rotation < 0 current_position - abs(rotation) % 100 == 0

        # if we go pass 0,
        # when rotation > 0 current_position + rotation % 100 > 100 e.g. 5 to 101
        # when rotation < 0 current_position - abs(rotation) % 100 < 0 e.g. 95 to -5

        if current_position != 0 and abs(rotation) % 100 > 0:
            if rotation > 0 and current_position + rotation % 100 >= 100:
                part_two += 1
            elif rotation < 0 and current_position - abs(rotation) % 100 <= 0:
                part_two += 1

        current_position += rotation
        current_position %= 100

        # If we land on 0, increment part one.
        if current_position == 0:
            part_one += 1

    return (part_one, part_two)

def main():
    rotations = parse_input()
    result = solve(rotations)
    print(result)

main()
