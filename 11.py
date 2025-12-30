# Source Node: You, Destination Node: Out
# Run BFS

import sys


def solve_part_one(adjacency_list: list[dict[str, list[str]]]):
    queue = ["you"]
    result = 0

    while len(queue) > 0:
        device = queue.pop(0)

        # No outputs
        if device not in adjacency_list:
            continue

        for output in adjacency_list[device]:
            if output == "out":
                result += 1
                continue

            queue.append(output)

    return result


def solve_part_two(adjacency_list: list[dict[str, list[str]]]):
    source = "svr"
    traversed = {}  # records the number of paths found by a fully explored node.

    # Optimization -> remember the number of paths from any given source that
    # 1. Encounter 'dac' and reach 'out'.
    # 2. Encounter 'fft' and reach 'out'.
    # 3. Encounter both and reach 'out'. This only increments when we're on a dac or fft node
    # 4. Encounter none and reach 'out'

    # "aaa": {'dac': 2, 'fft': 5, both: 1}
    # (number of paths from aaa to out that encounter dac is 2 and number of path that encounter fft is 5)

    memo = {}

    # DFS
    def traverse(device: str):
        if device in memo:
            return memo[device]

        result = {"dac": 0, "fft": 0, "both": 0, "out": 0}

        # End of path
        if device == "out":
            result["out"] = 1

        if device in adjacency_list:
            for output in adjacency_list[device]:
                paths_found = traverse(output)
                result["dac"] += paths_found["dac"]
                result["fft"] += paths_found["fft"]
                result["out"] += paths_found["out"]

                if device == "dac":
                    result["dac"] += paths_found[
                        "out"
                    ]  # The number of paths passing "dac" reaching "out"
                    result["both"] += paths_found["fft"]
                elif device == "fft":
                    result["fft"] += paths_found["out"]
                    result["both"] += paths_found["dac"]
                else:
                    result["both"] += paths_found["both"]

        memo[device] = result
        return result

    traverse(source)
    return memo["svr"]["both"]


def parse_input():
    adj_list = {}

    for line in sys.stdin:
        if line.strip() == "":
            continue

        splits = line.split(" ")
        device = splits[0][:-1]
        adj_list[device] = []
        for output in splits[1:]:
            adj_list[device].append(output.strip())

    return adj_list


def main():
    adj_list = parse_input()

    part_one = solve_part_one(adj_list)
    print("Part 1:", part_one)

    part_two = solve_part_two(adj_list)
    print("Part 2:", part_two)


main()
