import requests
import json
from rich import print, box
from rich.console import Console
from rich.style import Style
from rich.table import Table
from rich.text import Text


class CryptoPortfolio:
    def __init__(self):
        self.sub_portfolios = {}

    def add_sub_portfolio(self, name):
        self.sub_portfolios[name] = {}

    def add_coin(self, sub_portfolio, coin_symbol, quantity):
        self.sub_portfolios[sub_portfolio][coin_symbol] = {
            'symbol': coin_symbol,
            'quantity': quantity,
            'purchase_price': None
        }

    def update_prices(self):
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,dogecoin,litecoin&vs_currencies=usd')
        prices = json.loads(response.text)

        for sub_portfolio in self.sub_portfolios.values():
            for coin in sub_portfolio.values():
                coin_symbol = coin['symbol']
                if coin_symbol in prices:
                    coin['current_price'] = prices[coin_symbol]['usd']
                else:
                    print(f"Price data not found for {coin_symbol}")

    def set_purchase_price(self, sub_portfolio, coin_symbol, purchase_price):
        if coin_symbol in self.sub_portfolios[sub_portfolio]:
            self.sub_portfolios[sub_portfolio][coin_symbol]['purchase_price'] = purchase_price
        else:
            print(f"{coin_symbol} not found in {sub_portfolio}")

    def calculate_profit_loss(self, sub_portfolio):
        total_profit_loss = 0

        for coin in self.sub_portfolios[sub_portfolio].values():
            quantity = coin['quantity']
            purchase_price = coin['purchase_price']
            current_price = coin.get('current_price')

            if purchase_price is not None and current_price is not None:
                profit_loss = (current_price - purchase_price) * quantity
                total_profit_loss += profit_loss

        return total_profit_loss

    def display_portfolio(self):
        table = self.create_portfolio_table()

        for sub_portfolio, coins in self.sub_portfolios.items():
            sub_portfolio_name = f"[reverse bold]{sub_portfolio}[/reverse bold]"
            self.add_sub_portfolio_row(table, sub_portfolio_name)

            sub_portfolio_profit_loss = 0

            for coin_symbol, coin_info in coins.items():
                quantity = coin_info['quantity']
                purchase_price = coin_info['purchase_price']
                current_price = coin_info.get('current_price', 'N/A')

                if purchase_price is not None and current_price != 'N/A':
                    profit_loss = (current_price - purchase_price) * quantity
                    sub_portfolio_profit_loss += profit_loss

                    self.add_coin_row(table, coin_symbol, quantity, purchase_price, current_price, profit_loss)

                elif purchase_price is None:
                    self.add_coin_row(table, coin_symbol, quantity, 'N/A', current_price, 'N/A')

            self.add_sub_portfolio_profit_loss_row(table, sub_portfolio_profit_loss)

        console = Console()
        console.print(table)

    def create_portfolio_table(self):
        table = Table(title=Text("Crypto Portfolio", style="reverse"), box=box.MINIMAL_DOUBLE_HEAD)
        table.add_column("Coin", justify="center", style="cyan", no_wrap=True)
        table.add_column("Quantity", justify="center", style="magenta")
        table.add_column("Purchase Price", justify="center", style="blue")
        table.add_column("Current Price", justify="center", style="green")
        table.add_column("Profit/Loss", justify="center", style="yellow")
        return table

    def add_sub_portfolio_row(self, table, sub_portfolio_name):
        table.add_row(sub_portfolio_name)

    def add_coin_row(self, table, coin_symbol, quantity, purchase_price, current_price, profit_loss):
        profit_loss_style = self.get_profit_loss_style(profit_loss)

        table.add_row(
            coin_symbol,
            Text(str(quantity), justify="center", style="cyan", no_wrap=True),
            Text(str(purchase_price) if purchase_price else 'N/A', justify="center", style="magenta"),
            Text(str(current_price) if current_price else 'N/A', justify="center", style="green"),
            str(profit_loss),
            style=profit_loss_style
        )

    def add_sub_portfolio_profit_loss_row(self, table, sub_portfolio_profit_loss):
        table.add_row("", "", "", "", str(sub_portfolio_profit_loss))

    def get_profit_loss_style(self, profit_loss):
        if profit_loss == 'N/A':
            return Style(color='white')
        elif float(profit_loss) >= 0:
            return Style(color='white')
        else:
            return Style(color='red1')

    def save_portfolio_data(self, file_name):
        with open(file_name, 'w') as file:
            json.dump(self.sub_portfolios, file)

    def load_portfolio_data(self, file_name):
        with open(file_name, 'r') as file:
            self.sub_portfolios = json.load(file)


def main_menu(portfolio):
    while True:
        print("\n[bold cyan]Crypto Portfolio Management[/bold cyan]\n")
        print("1. Add Sub-Portfolio")
        print("2. Add Coin")
        print("3. Set Purchase Price")
        print("4. Update Prices")
        print("5. Calculate Profit/Loss")
        print("6. Display Portfolio")
        print("7. Save Portfolio Data")
        print("8. Load Portfolio Data")
        print("9. Exit")

        choice = input("\nEnter your choice (1-9): ")

        if choice == '1':
            sub_portfolio_name = input("Enter the sub-portfolio name: ")
            portfolio.add_sub_portfolio(sub_portfolio_name)
        elif choice == '2':
            sub_portfolio = input("Enter the sub-portfolio name: ")
            coin_symbol = input("Enter the coin symbol: ")
            quantity = float(input("Enter the quantity: "))
            portfolio.add_coin(sub_portfolio, coin_symbol, quantity)
        elif choice == '3':
            sub_portfolio = input("Enter the sub-portfolio name: ")
            coin_symbol = input("Enter the coin symbol: ")
            purchase_price = float(input("Enter the purchase price: "))
            portfolio.set_purchase_price(sub_portfolio, coin_symbol, purchase_price)
        elif choice == '4':
            portfolio.update_prices()
            print("Prices updated successfully.")
        elif choice == '5':
            sub_portfolio = input("Enter the sub-portfolio name: ")
            profit_loss = portfolio.calculate_profit_loss(sub_portfolio)
            print(f"Profit/Loss for {sub_portfolio}: {profit_loss}")
        elif choice == '6':
            portfolio.display_portfolio()
        elif choice == '7':
            file_name = input("Enter the file name to save the portfolio data (e.g., portfolio_data.json): ")
            portfolio.save_portfolio_data(file_name)
            print("Portfolio data saved successfully.")
        elif choice == '8':
            file_name = input("Enter the file name to load the portfolio data from (e.g., portfolio_data.json): ")
            portfolio.load_portfolio_data(file_name)
            print("Portfolio data loaded successfully.")
        elif choice == '9':
            break
        else:
            print("Invalid choice. Please try again.")


# Example usage
portfolio = CryptoPortfolio()
main_menu(portfolio)
