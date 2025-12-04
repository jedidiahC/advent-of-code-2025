import sys

def try_remove(grid: list[list[str]]) -> tuple[int, list[list[str]]]:
    to_remove = 0
    new_grid = []

    for row in range(len(grid)):
        new_grid.append([])

        for col in range(len(grid[0])):
            adjacent = 0

            # If not roll of paper skip.
            if grid[row][col] != '@':
                new_grid[row].append(grid[row][col])
                continue

            for direction in [(-1, -1), (-1, 0), (-1, 1),
                              (0, -1),          (0, 1),
                              (1, -1),  (1, 0), (1, 1)]:
                r, c = row + direction[0], col + direction[1]

                if 0 <= r < len(grid) and 0 <= c < len(grid[0]) and grid[r][c] == '@':
                    adjacent += 1

            if adjacent < 4:
                to_remove += 1
                new_grid[row].append('.')
            else:
                new_grid[row].append('@')

    return to_remove, new_grid

def solve(grid: list[list[str]]):
    part_one = -1
    part_two = 0

    removed = 0
    while True:
        to_remove, grid = try_remove(grid)

        # If nothing to remove, we are done.
        if to_remove == 0:
            break

        part_two += to_remove

        if part_one == -1:
            part_one = to_remove


    return part_one, part_two

def parse_input() -> list[str]:
    grid = []

    for line in sys.stdin:
        grid.append(list(line.strip()))

    return grid

def main():
    grid = parse_input()
    print(solve(grid))

main()
