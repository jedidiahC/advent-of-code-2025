import sys
from unittest import result

def solve(operands_list: list[list[int]], operators: list[str]):
    part_one = 0
    for index, operands in enumerate(operands_list):
        operator = operators[index]
        result = operands[0]

        for operand in operands[1:]:
            if operator == '+':
                result += operand
            elif operator == '*':
                result *= operand

        part_one += result

    part_two = 0
    # We need to interpret the operands differently in this case.
    # Re-process operands to the new format.


    return part_one

def parse_input():
    operands_list = []
    operators = []
    for line in sys.stdin:
        if line.strip() == '':
            break

        for index, element in enumerate(line.split()):
            # Add operator
            if element == '*' or element == '+':
                operators.append(element)
                continue

            # Add operand
            if len(operands_list) <= index:
                operands_list.append([])

            operands_list[index].append(int(element))

    return operands_list, operators

def main():
    operands_list, operators = parse_input()
    result = solve(operands_list, operators)
    print(result)

main()
