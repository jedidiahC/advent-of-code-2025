
# O(n^2) brute force to test every pair of red tiles

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

# Part 2 - Attempt 2
# for a pair of tiles to form a valid rectangle r.
#   r must lie within the concave polygon formed by the edges [r_x, r_(x - 1)]

# let the polygon formed by connecting all pairs of adjacent red tiles be polygon B
# let the rectangle formed by any pair of red tiles be polygon A
# for polygon A to be valid.
# 1. the remaining 2 tiles forming polygon A that are not the pair of red tiles originally selected must be
#  within or along the boundary of polygon B
# 2. the midpoint of each of the edges of polygon A must also lie within or along the boundary of polygon B

import sys
from typing import TypedDict

# a rectangle is defined by it's bottom-left and top-right vertices
type Point = tuple[int, int]
type Rect = tuple[Point, Point]

type Interval = tuple[int, int]
type Lines = dict[int, list[Interval]]

class Shape(TypedDict):
    vertical: Lines
    horizontal: Lines

type Tile = tuple[int, int]

def create_rectangle(tile_0: Tile, tile_1: Tile) -> Rect:
    x_0, y_0 = tile_0
    x_1, y_1 = tile_1

    # Sort the inputs
    if x_0 > x_1:
        x_0, x_1 = x_1, x_0

    if y_0 > y_1:
        y_0, y_1 = y_1, y_0

    return ((x_0, y_0), (x_1, y_1))

#..............
#.......#XXX#..
#.......XXXXX..
#..OOOOOOOOXX..
#..OOOOOOOOXX..
#..OOOOOOOOXX..
#.........XXX..
#.........#X#..
#..............
# the interval need to share > 1 cell to intersect so we ignore cases where the rectangle just grazes the edge
def is_intersect(interval_0: Interval, interval_1: Interval):
    # Sort the intervals by start.
    if interval_0[0] > interval_1[0]:
        interval_0, interval_1 = interval_1, interval_0

    end_0 = interval_0[1]
    start_1 = interval_1[0]

    return start_1 - end_0 < 0

def calculate_area(rec: Rect) -> int:
    (x0, y0), (x1, y1) = rec
    return (abs(x1 - x0) + 1) * (abs(y1 - y0) + 1)

def solve_part_one(red_tiles: list[Tile]) -> int:
    part_one = 0

    for i in range(len(red_tiles)):
        for j in range(i + 1, len(red_tiles)):
            red_tile_0 = red_tiles[i]
            red_tile_1 = red_tiles[j]

            part_one = max(part_one, calculate_area(create_rectangle(red_tile_0, red_tile_1)))

    return part_one

def build_shape(red_tiles: list[Tile]) -> Shape:
    shape: Shape = {
        "horizontal": {},
        "vertical": {}
    }

    last_red_tile = red_tiles[0]

    tiles_with_looping = red_tiles[1:]
    tiles_with_looping.append(last_red_tile)

    for red_tile in tiles_with_looping:
        last_x, last_y = last_red_tile
        x, y = red_tile

        # Store horizontal line:
        if y == last_y:
            if y not in shape["horizontal"]:
                shape["horizontal"][y] = []

            sorted_tuple = tuple(sorted([last_x, x]))
            shape["horizontal"][y].append((sorted_tuple[0], sorted_tuple[1]))

        # Store vertical line:
        elif x == last_x:
            if x not in shape["vertical"]:
                shape["vertical"][x] = []

            sorted_tuple = tuple(sorted([last_y, y]))
            shape["vertical"][x].append((sorted_tuple[0], sorted_tuple[1]))

        last_red_tile = red_tile

    return shape


def solve_part_two(red_tiles: list[Tile]) -> int:

    # Test if a rectangle strictly intersects with any orthogonal lines.
    def does_rectangle_intersect(rect: Rect, lines: Lines, is_vertical: bool):
        (x_0, y_0), (x_1, y_1) = rect

        # Iterate through every orthogonal line, testing for intersection.
        for pos, line_intervals in lines.items():
            if is_vertical:
                if not x_0 < pos < x_1:
                    continue

                for line_interval in line_intervals:
                    if is_intersect((y_0, y_1), line_interval):
                        return True

            else:
                if not y_0 < pos < y_1:
                    continue

                for line_interval in line_intervals:
                    if is_intersect((x_0, x_1), line_interval):
                        return True

        return False

    # raycast
    def is_point_inside_polygon(x: float, y: float, verticals: Lines):
        cross = 0

        for v_x in verticals:
            if v_x < x:
                continue

            for v in verticals[v_x]:
                (v_y0, v_y1) = v
                if v_y0 < y < v_y1:
                    cross += 1

        return cross % 2 != 0

    def is_rect_within_shape(rect: Rect, shape: Shape):
        # When a few of the edges line up perfectly on the edges of the shape, then we can't tell if the edges intersect the shape edges.
        if does_rectangle_intersect(rect, shape["vertical"], True) or does_rectangle_intersect(rect, shape["horizontal"], False):
            return False

        # check cases where the rectangle's sides lie exactly along the boundary
        # here, the rectangle either lies exactly inside the polygon or outside
        # check all mid points whether within polygon
        (x_0, y_0), (x_1, y_1) = rect
        mid_x = (x_0 + x_1) / 2
        mid_y = (y_0 + y_1) / 2

        return is_point_inside_polygon(mid_x, mid_y, shape["vertical"])

    shape = build_shape(red_tiles)
    part_two = 0

    for i in range(len(red_tiles)):
        for j in range(i + 1, len(red_tiles)):
            rect = create_rectangle(red_tiles[i], red_tiles[j])

            if is_rect_within_shape(rect, shape):
                part_two = max(calculate_area(rect), part_two)

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
