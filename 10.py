import sys

# DFS Traversal -> Branching factor is number of buttons
# Goal to obtain correct lights state represented by a list of booleans.
# e.g. [True, False, True] 1st and 3rd lights on.
# To manage branching, we can prune if we encounter a previously encountered state -> store remembered states as tuples in set.

# Returns min number of button presses to start the machine.

def start_machine(desired_state: list[bool], buttons: list[list[int]]) -> int:
    seen = set()
    desired_state_tuple = tuple(desired_state)
    starting_state = [False] * len(desired_state)
    queue = [(starting_state, 0)] # (state, number of presses to reach state)

    while len(queue) > 0:
        current_state, presses = queue.pop(0)
        seen.add(tuple(current_state))

        for button in buttons:
            next_state = current_state.copy()
            for light in button:
                next_state[light] = not current_state[light]

            next_state_tuple = tuple(next_state)
            if next_state_tuple in seen:
                continue

            # If we found the desired state return the number of presses.
            if next_state_tuple == desired_state_tuple:
                return presses + 1

            queue.append((next_state, presses + 1))

    # This should not happen.
    return -1

def solve(machines: list[tuple[list[bool], list[list[int]]]]):
    part_one = 0
    for machine in machines:
        desired_state, buttons = machine
        part_one += start_machine(desired_state, buttons)

    return part_one

def parse_input():

    machines = []

    for line in sys.stdin:
        if line.strip() == '':
            continue

        desired_state = None
        buttons = []

        elements = line.split(' ')

        for el in elements:
            if el[0] == '[':
                desired_state = list(map(lambda chr: chr == '#', list(el[1:-1])))
                continue

            if el[0] == '(':
                buttons.append(list(map(int, el[1:-1].split(','))))
                continue

            # TODO: Process Jottage.

        machines.append((desired_state, buttons))

    return machines

def main():
    machines = parse_input()
    result = solve(machines)
    print(result)

main()
