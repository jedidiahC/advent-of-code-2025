# Total number possible connections: [(n - 1) * n] / 2
# We will count the sizes of the remaining components.
# How do we track components? Using UFDS to track?
# We generate every possible connection and sort them in ascending order.
# Then, we process 1000 connections and check the number of remaining components in the UFDS.

# To count components:
# Every time, we create a connection, the number of circuits decrease by at most 1.
# This happens when two junctions do not belongs to the same circuit.
# Creating the connection causes the two circuits to merge, decreasing the number of circuits by exactly 1.

from math import sqrt
import sys

def calculate_distance(p0: tuple[int, int, int], p1: tuple[int, int, int]):
    return sqrt((p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2 + (p0[2] - p1[2]) ** 2)

def solve(junctions: tuple[int, int, int]):
    # Generate connections. Each connection is distance, j0, j1.
    connections = []

    for j0, junction_0 in enumerate(junctions):
       for j1 in range(j0 + 1, len(junctions)):
            junction_1 = junctions[j1]
            connections.append((calculate_distance(junction_0, junction_1), j0, j1))

    # Sort connections
    connections.sort(key = lambda c: c[0])

    # For each connection, we test the membership of the two junctions,
    # merging their circuits and decrement result by 1 if they do not belong to the same set/circuit.

    # We will implement UFDS with path compression.

    ufds = [i for i in range(len(junctions))]

    def find_circuit(junction_id: int):

        # Base case: we've hit the root of the tree.
        if ufds[junction_id] == junction_id:
            return junction_id

        parent = find_circuit(ufds[junction_id])
        ufds[junction_id] = parent # Perform path compression here.
        return ufds[junction_id]

    def is_same_circuit(j0: int, j1: int):
        return find_circuit(j0) == find_circuit(j1)

    # No rank heuristic when merging currently.
    def merge_circuits(j0: int, j1: int):
        ufds[find_circuit(j0)] = find_circuit(j1)

    circuits_count = len(junctions)

    part_one = None
    part_two = None

    connections_cutoff = 1000 # need to modify this for the sample input >:(

    def calculate_part_one():
        circuits_size = {}

        for i in range(len(junctions)):
            circuit = find_circuit(i)
            if circuit not in circuits_size:
                circuits_size[circuit] = 1
            else:
                circuits_size[circuit] += 1

        result = 1
        sizes = list(circuits_size.values())
        sizes.sort(reverse=True)

        for size in sizes[:3]:
            result *= size

        return result

    for index, connection in enumerate(connections):
        _, j0, j1 = connection

        if not is_same_circuit(j0, j1):
            circuits_count -= 1
            if circuits_count == 1:
                part_two = junctions[j0][0] * junctions[j1][0]
                break
            merge_circuits(j0, j1)

        if index == connections_cutoff - 1:
            part_one = calculate_part_one()

    return part_one, part_two

def parse_input() -> list[tuple[int, int, int]]:
    junctions = []
    for line in sys.stdin:
        if line.strip() == '':
            break
        junctions.append(tuple(map(int, line.split(','))))

    return junctions

def main():
    junctions = parse_input()
    solution = solve(junctions)
    print(solution)

main()
