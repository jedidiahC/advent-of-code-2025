import sys

def find_best_output(bank: str, x_digits: int) -> int:
    dp = [0] * x_digits # dp[i] - Best power of i digits

    for battery_str in bank:
        battery = int(battery_str)
        new_dp = [0] * x_digits
        for i in range(1, x_digits):
            new_dp[i] = max(dp[i - 1] * 10 + battery, dp[i])

        new_dp[0] = max(dp[0], battery)
        dp = new_dp

    return dp[x_digits - 1]


def solve(banks: list[str]):
    # Brute Force: loop through first digit and second digit until we get the maximum output.
    part_one = 0
    part_two = 0

    for bank in banks:
        part_one += find_best_output(bank, 2)
        part_two += find_best_output(bank, 12)

    return (part_one, part_two)

def parse_input() -> list[str]:
    banks = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        banks.append(line)

    return banks

def main():
    banks = parse_input()
    result = solve(banks)
    print(result)

main()
