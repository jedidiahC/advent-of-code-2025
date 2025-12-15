# O(n^2) brute force to test every pair of red tiles
import sys

def calculate_area(r0, r1):
    return (abs(r0[0] - r1[0]) + 1) * (abs(r0[1] - r1[1]) + 1)

def solve_part_one(red_tiles: list[tuple[int, int]]):
    part_one = 0
    for i in range(0, len(red_tiles)):
        for j in range(i + 1, len(red_tiles)):
            r0 = red_tiles[i]
            r1 = red_tiles[j]

            part_one = max(part_one, calculate_area(r0, r1))

    return part_one

# Part 2 - Brute Force Solution:
# Mark tiles between each red tile as green.
# After all red tiles have been processed, we should have a boundary of red and green tiles.
# Pick an uncoloured tile within this boundary and perform a flood-fill to mark all tiles within the boundary to green. (how to determine an uncoloured tile?)

# Any pair of red tiles form a horizontal or vertical lines (no diagonals) -> "every red tile is connected to the red tile before and after it by a straight line of green tiles."

# Afterwards, we can perform an O(n^4) algorithm, to check all pairs of points if they can form a rectangle of green tiles.

# Optimization 1: We can remove the O(n^2) part of checking every tile of the rectangle if they are green/red tiles by
# only checking the edge of the rectangle. If any tile on the edge is not red/green, then the rectangle is not inside the shape.
# We can prove that by checking only edge, the rectangle completely falls within the shape as the shape has no holes.

# Optimization 2: We avoid the floor-fill, only testing if the edges of the rectangle intersect with any of the line segments forming the rectangle.
# This will not if the shape already has line segments that intersect. However, if this is the case, then there is no concept of tiles being "inside" the loops since there is now no clear "outer edge" to the polygon.

# To do this we need to make line intersection querying efficiently, hence, we store line segments in this way:
# Horizontal lines stored by y: {1: [(5, 6), (9, 10)], ...} line segment on y = 1 that goes from x=5 to x=6
# Vertical lines stored by x: {1: [(5, 6), (9, 10)], ...} line segment on x = 1 that goes from y=5 to y=6
# This is a hashmap of coordinates to list of line segments. We can sort the line segments by their starting components to allow for a more efficient binary search log(n) query,
# but im too lazy to do this since there should not be too many co-linear line segments.

def solve_part_two(red_tiles: list[tuple[int, int]]):
    last_red_tile = red_tiles[0]

    horizontal = {}
    vertical = {}

    for red_tile in red_tiles[1:]:
        last_x, last_y = last_red_tile
        x, y = red_tile

        # Store horizontal line:
        if x == last_x:
            if y not in horizontal:
                horizontal[y] = []

            horizontal[y].append(tuple(sorted([last_x, x])))

        # Store vertical line:
        elif y == last_y:
            if x not in vertical:
                vertical[x] = []

            vertical[x].append(tuple(sorted([last_y, y])))

        last_red_tile = red_tile

    # Test if a horizontal or vertical line intersects with the orthogonal lines.
    def does_line_intersect(line: tuple[int, int, int], orthogonal: dict[int, list[tuple[int, int]]]):
        intersect, start, end = line

        # Iterate through every orthogonal line, testing for intersection.
        for p in orthogonal:
            # ignore set of orthogonal that is not within line range.
            if not start < p < end:
                continue

            for ortho_line in orthogonal[p]:
                ortho_line_start, ortho_line_end = ortho_line
                if ortho_line_start <= intersect <= ortho_line_end:
                    return True

        return False

    def generate_rectangle_lines(red_0: tuple[int, int], red_1: tuple[int, int]):
        x0, y0 = red_0
        x1, y1 = red_1

        # Sort the inputs
        if x0 > x1:
            x0, x1 = x1, x0

        if y0 > y1:
            y0, y1 = y1, y0

        horizontal_lines = [(y0, x0, x1), (y1, x0, x1)]
        vertical_lines = [(x0, y0, y1), (x1, y0, y1)]

        return horizontal_lines, vertical_lines

    def is_within_shape(vertical_lines, horizontal_lines, vertical, horizontal):
        # When a few of the edges line up perfectly on the edges of the shape, then we can't tell if the edges intersect the shape edges.

        # check if horizontal lines intersect vertical shape lines
        for h in horizontal_lines:
            if does_line_intersect(h, vertical):
                return False

        # check if vertical lines intersect horizontal shape lines
        for v in vertical_lines:
            if does_line_intersect(v, horizontal):
                return False

        return True

    part_two = 0
    for i in range(0, len(red_tiles)):
        for j in range(i + 1, len(red_tiles)):
            r0 = red_tiles[i]
            r1 = red_tiles[j]

            horizontal_lines, vertical_lines = generate_rectangle_lines(r0, r1)

            if is_within_shape(vertical_lines, horizontal_lines, vertical, horizontal):
                part_two = max(calculate_area(r0, r1), part_two)

    return part_two

def parse_input():
    red_tiles = []
    for line in sys.stdin:
        if line.strip() == '':
            break

        red_tiles.append(tuple(map(int, line.split(','))))

    return red_tiles

def main():
    red_tiles = parse_input()
    part_one_sol, part_two_sol = solve_part_one(red_tiles), solve_part_two(red_tiles)
    print(part_one_sol)
    print(part_two_sol)

main()
