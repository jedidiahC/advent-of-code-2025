import sys
from scipy.optimize import linprog

# BFS Traversal -> Branching factor is number of buttons
# Goal to obtain correct lights state represented by a list of booleans.
# e.g. [True, False, True] 1st and 3rd lights on.
# To manage branching, we can prune if we encounter a previously encountered state -> store remembered states as tuples in set.

# Returns min number of button presses to start the machine.


def start_machine(desired_lights: list[bool], buttons: list[list[int]]) -> int:
    seen = set()
    desired_lights_tuple = tuple(desired_lights)
    starting_state = [False] * len(desired_lights)
    queue = [(starting_state, 0)]  # (state, number of presses to reach state)

    while len(queue) > 0:
        current_lights, presses = queue.pop(0)
        seen.add(tuple(current_lights))

        for button in buttons:
            next_lights = current_lights.copy()
            for light in button:
                next_lights[light] = not current_lights[light]

            next_lights_tuple = tuple(next_lights)
            if next_lights_tuple in seen:
                continue

            # If we found the desired state return the number of presses.
            if next_lights_tuple == desired_lights_tuple:
                return presses + 1

            queue.append((next_lights, presses + 1))

    # Machine unsolvable: This should not happen.
    return -1


# There's a linear algebra approach to this where
# Desired state is in this form -> aC_0 + bC_1 + cC_2 where a -> number of times counter 0 must be incremented

# Let B_i be the number of times button is pressed and C_i be the desired value of the i-th counter.
# Then we get a series of linear equations in the following format:
# c_0B_0 + c_1B_1 + ... + c_nB_n = C_i where c_i is a constant that represents how much button i increases counter i.
# c_i is always either 1 or 0 depending on whether button i increments counter i or not.

# Example linear equations:
# 1B_0 + 0B_1 + .. + 1B_3 = 10
# ...
# 1B_0 + ... 1B_2 = 6

# We need to solve for the minimum (B_0 + B_1 + ... + B_n) that satisfies this set of linear equations.


# Use linear programming (simplex) to solve min(B_0 + B_1 + ... + B_n) where A.B = b and A = [c_0, ... c_i], B = [B_0, ...]
def configure_jottage(desired_jottages: list[int], buttons: list[list[int]]):
    # Represent the equations in matrix form desired_jottage.length x (buttons.length + 1):
    c = [
        1 for x in range(len(buttons))
    ]  # This represents the linear equation we are optimizing for in this case -> C = 1B_0 + 1B_1 + ... + B_i
    A = [
        [0 for _ in range(len(buttons))] for jottage in range(len(desired_jottages))
    ]  # These are the coefficients for each constraint equation.

    # Fill in each column of the rest of the matrix (A):
    for button_index, button in enumerate(buttons):
        for counter in button:
            A[counter][button_index] = 1

    b = desired_jottages  # This represents the equation constraints.

    result = linprog(c, A_eq=A, b_eq=b, integrality=1).fun
    return result


def solve(machines: list[tuple[list[bool], list[list[int]]]]):
    part_one = 0
    part_two = 0
    for machine in machines:
        desired_state, desired_jottage, buttons = machine
        part_one += start_machine(desired_state, buttons)
        part_two += configure_jottage(desired_jottage, buttons)

    return part_one, part_two


def parse_input():

    machines = []

    for line in sys.stdin:
        if line.strip() == "":
            continue

        desired_state = None
        desired_jottage = None
        buttons = []

        elements = line.split(" ")

        for el in elements:
            if el[0] == "[":
                desired_state = list(map(lambda chr: chr == "#", list(el[1:-1])))
                continue

            if el[0] == "(":
                buttons.append(list(map(int, el[1:-1].split(","))))
                continue

            # TODO: Process Jottage.
            if el[0] == "{":
                desired_jottage = list(map(int, el.strip()[1:-1].split(",")))

        machines.append((desired_state, desired_jottage, buttons))

    return machines


def main():
    machines = parse_input()
    result = solve(machines)
    print(result)


main()
