import requests
import pandas as pd
import schedule
import time
# Define the Function to Fetch Data

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": False
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        fields = ["name", "symbol", "current_price", "market_cap", "total_volume", "price_change_percentage_24h"]
        return pd.DataFrame(data, columns=fields)
    else:
        print(f"Error fetching data: {response.status_code}")
        return pd.DataFrame()
# Define the Data Analysis Function

def analyze_data(df):
    if df.empty:
        print("No data to analyze.")
        return None
    
    top_5 = df.nlargest(5, "market_cap")
    avg_price = df["current_price"].mean()
    highest_change = df["price_change_percentage_24h"].max()
    lowest_change = df["price_change_percentage_24h"].min()
    
    print("\nTop 5 Cryptocurrencies by Market Cap:")
    print(top_5[["name", "market_cap"]])
    
    print(f"\nAverage Price: ${avg_price:.2f}")
    print(f"Highest 24h Change: {highest_change:.2f}%")
    print(f"Lowest 24h Change: {lowest_change:.2f}%")
    
    return top_5, avg_price, highest_change, lowest_change
# Define the Function to Export Data to Excel
def export_to_excel(df, filename="crypto_data.xlsx"):
    with pd.ExcelWriter(filename, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, index=False, sheet_name="Cryptocurrency Data")
    print(f"Data exported to {filename}.")

def job():
    print("\nFetching and updating data...")
    df = fetch_crypto_data()
    if not df.empty:
        export_to_excel(df)
        analyze_data(df)

schedule.every(5).minutes.do(job)

# Initial run
job()
# Continuous Execution

while True:
    schedule.run_pending()
    time.sleep(1)