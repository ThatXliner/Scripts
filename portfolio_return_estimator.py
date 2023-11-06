# /// pyproject
# [run]
# requires-python = ">=3.8"
# dependencies = [
#   "rich",
# ]
# ///
from dataclasses import dataclass
from typing import List

try:
    from rich import print
except ModuleNotFoundError:
    pass
try:
    from rich.prompt import Prompt, Confirm
except ModuleNotFoundError:

    class Prompt:
        @staticmethod
        def ask(msg):
            return input(msg)

    class Confirm:
        @staticmethod
        def ask(msg):
            return input(msg).lower().strip()[0] == "y"


import random


@dataclass
class Stock:
    return_percent: float
    investment: float


def estimate_portfolio_value(stocks: List[Stock], years: int = 15) -> float:
    total_value = 0

    for stock in stocks:
        annual_return = stock.return_percent / 100  # Convert percentage to decimal
        total_value += stock.investment * (1 + annual_return) ** years

    return total_value


def main():
    stocks = []
    years = int(Prompt.ask("How many years"))
    while True:
        try:
            return_percent = float(
                Prompt.ask("Enter average yearly return for a stock (in percentage)")
            )
            investment = float(
                Prompt.ask("Enter the total investment in this stock (in dollars)")
            )
            stocks.append(Stock(return_percent, investment))
            another_stock = Confirm.ask("Add another stock?", default=True)
            if not another_stock:
                break
        except ValueError:
            print("[red]Invalid input. Please enter valid numbers.[/red]")
        except (KeyboardInterrupt, EOFError):
            break

    print(
        f"\n[bold green]Estimated Portfolio Value after {years} years:[/bold green] [blue]${estimate_portfolio_value(stocks):.2f}[/blue]"
    )


if __name__ == "__main__":
    random.seed(42)
    print("[cyan]Stock Portfolio Estimator[/cyan]")
    main()
