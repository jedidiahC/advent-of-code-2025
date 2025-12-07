import sys

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

    return part_one

def parse_input():
    operands_list = []
    operators = []

    lines = []

    max_line_length = 0
    for line in sys.stdin:
        if line.strip() == '':
            break

        # Parse part_one input
        for index, element in enumerate(line.split()):
            # Add operator
            if element == '*' or element == '+':
                operators.append(element)
                continue

            # Add operand
            if len(operands_list) <= index:
                operands_list.append([])

            operands_list[index].append(int(element))

        # Parse part_two input: We store all elements in an array of strings first.
        max_line_length = max(max_line_length, len(line[:-1]))
        lines.append(list(line[:-1]))

    # Now we process the previously parsed part_two input, using the operand position as a guideline.
    # lines[-1] should be the row with the operands.
    part_two_operands = []
    current_set = -1
    for index in range(max_line_length):
        if index < len(lines[-1]):
            char = lines[-1][index]
            if char == '*' or char == '+':
                part_two_operands.append([])
                current_set += 1

        current = 0
        for row in range(len(lines) - 1):
            if index >= len(lines[row]) or lines[row][index] == ' ':
                continue

            current *= 10
            current += int(lines[row][index])

        if current != 0:
            part_two_operands[current_set].append(current)

    return operands_list, part_two_operands, operators

def main():
    operands_list, operands_list_p2, operators = parse_input()
    part_one = solve(operands_list, operators)
    part_two = solve(operands_list_p2, operators)
    print(part_one, part_two)

main()
