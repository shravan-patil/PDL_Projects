import pandas as pd
import numpy as np

class Stock:
    def __init__(self, ticker, name, price):
        self.ticker = ticker
        self.name = name
        self.current_price = price

    def refresh_price(self):
        change = np.random.uniform(-0.1, 0.1)
        self.current_price = round(self.current_price * (1 + change), 2)

class Portfolio:
    def __init__(self, initial_cash=15000):
        self.balance = initial_cash
        self.stocks_owned = {}    
        self.available_stocks = {} 
    
    def add_stock(self, stock):
        self.available_stocks[stock.ticker] = stock

    def buy_stock(self, ticker, quantity):
        if ticker not in self.available_stocks:
            print("Invalid stock number.")
            return
        if quantity <= 0:
            print("Quantity must be positive.")
            return
        stock = self.available_stocks[ticker]
        cost = stock.current_price * quantity
        if cost > self.balance:
            print("Not enough balance.")
            return
        self.balance -= cost
        self.stocks_owned[ticker] = self.stocks_owned.get(ticker, 0) + quantity
        print(f"Bought {quantity} shares of {stock.name} for {round(cost,2)}")

    def sell_stock(self, ticker, quantity):
        if ticker not in self.stocks_owned or self.stocks_owned[ticker] < quantity:
            print("Not enough shares to sell.")
            return
        if quantity <= 0:
            print("Quantity must be positive.")
            return
        stock = self.available_stocks[ticker]
        revenue = stock.current_price * quantity
        self.balance += revenue
        self.stocks_owned[ticker] -= quantity
        if self.stocks_owned[ticker] == 0:
            del self.stocks_owned[ticker]
        print(f"Sold {quantity} shares of {stock.name} for {round(revenue,2)}")

    def refresh_prices(self):
        for stock in self.available_stocks.values():
            stock.refresh_price()
        print("\nAll stock prices updated.")
        self.show_current_prices()
        self.save_prices_to_csv()  

    def view_portfolio(self):
        data = []
        total_value = 0
        for ticker, qty in self.stocks_owned.items():
            stock = self.available_stocks[ticker]
            value = stock.current_price * qty
            total_value += value
            data.append({
                'Stock No.': ticker,
                'Name': stock.name,
                'Quantity': qty,
                'Current Price': stock.current_price,
                'Value': value
            })
        df = pd.DataFrame(data)
        print("\nPortfolio Summary:")
        if df.empty:
            print("No stocks owned yet.")
        else:
            print(df.to_string(index=False))
        print(f"\nBank Balance: {round(self.balance , 2)}")
        print(f"Portfolio Value: {round(total_value, 2)}")
        print(f"Total Worth: {round(self.balance + total_value, 2)}\n")

    def show_current_prices(self):
        print("\nCurrent Stock Prices:")
        for ticker, stock in self.available_stocks.items():
            print(f"{ticker}: {stock.name} (Price: {stock.current_price})")

    def save_prices_to_csv(self, filename='stock_prices.csv'):
        data = {stock.name: [stock.current_price] for stock in self.available_stocks.values()}
        df_existing = pd.read_csv(filename)
        df_new = pd.DataFrame(data)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_csv(filename, index=False)

    def load_prices_from_csv(self, filename='stock_prices.csv'):
        df = pd.read_csv(filename)
        last_row = df.iloc[-1]
        for i, stock in enumerate(self.available_stocks.values()):
            stock.current_price = last_row.iloc[i] 

if __name__ == "__main__":
    stock_names = ['INFOSYS', 'TCS', 'RELIANCE', 'FLIPKART', 'COALIND', 'BIRLA', 'TCL']
    portfolio = Portfolio(initial_cash=15000)
    for i, name in enumerate(stock_names, start=1):
        stock = Stock(ticker=i, name=name, price=0)
        portfolio.add_stock(stock)

    portfolio.load_prices_from_csv()  
    print("Available Stocks:")
    portfolio.show_current_prices()
    print(f"Initial Bank Balance: {portfolio.balance}")

    while True:
        print("\nStock Market Menu")
        print("1. View Portfolio")
        print("2. Buy Stock")
        print("3. Sell Stock")
        print("4. Refresh Prices")
        print("5. Show Current Prices")
        print("6. Exit")
        choice = input("Enter choice (1-6): ").strip()

        if choice == '1':
            portfolio.view_portfolio()
        elif choice == '2':
            try:
                ticker = int(input("Enter stock number to buy: "))
                qty = int(input("Enter quantity: "))
                portfolio.buy_stock(ticker, qty)
            except ValueError:
                print("Invalid input.")
        elif choice == '3':
            try:
                ticker = int(input("Enter stock number to sell: "))
                qty = int(input("Enter quantity: "))
                portfolio.sell_stock(ticker, qty)
            except ValueError:
                print("Invalid input.")
        elif choice == '4':
            portfolio.refresh_prices()
        elif choice == '5':
            portfolio.show_current_prices()
        elif choice == '6':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice.")
