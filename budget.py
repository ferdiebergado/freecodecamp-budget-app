from typing import List
import math


class Category:
    def __init__(self, name: str) -> None:
        self.name = name
        self.ledger = []

    def deposit(self, amount: float, description: str = "") -> None:
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount: float, description: str = "") -> bool:
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True

        return False

    def get_balance(self) -> float:
        return sum([entry["amount"] for entry in self.ledger], 0)

    def check_funds(self, amount: float) -> bool:
        return self.get_balance() >= amount

    def transfer(self, amount: float, other_category) -> bool:
        if self.withdraw(amount, f"Transfer to {other_category.name}"):
            other_category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def __str__(self) -> str:
        s = f"{self.name:*^30}\n"

        for entry in self.ledger:
            s += f'{entry["description"][:23]:<23}{entry["amount"]:>7.2f}\n'

        s += f"Total: {self.get_balance()}"

        return s


def create_spend_chart(categories: List[Category]):

    total_withdrawals = 0
    withdrawals_dict = {}

    for category in categories:
        withdrawals = abs(
            sum([entry["amount"] for entry in category.ledger if entry["amount"] < 0])
        )

        total_withdrawals += withdrawals

        withdrawals_dict[category.name] = withdrawals

    chart = "Percentage spent by category\n"

    for percentile in reversed(range(0, 110, 10)):

        chart += f"{percentile:>3}|"

        for c in categories:
            p = withdrawals_dict[c.name] / total_withdrawals * 100

            rounded = math.floor(p)
            # print(c.name, p, rounded)

            if rounded >= percentile:
                chart += " o "
            else:
                chart += " " * 3

        chart += " \n"

    chart += " " * 4 + "-" * 10 + "\n"

    longest_category = max([c.name for c in categories], key=len)

    for i in range(len(longest_category)):

        chart += f"{' '  * 4}"

        for c in categories:

            try:
                chart += f" {c.name[i]} "
            except IndexError:
                chart += f"{' ' * 3}"

        if i < (len(longest_category) - 1):
            chart += " \n"
        else:
            chart += " "

    return chart
