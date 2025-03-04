from flask import Flask, render_template, request
import requests
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# List of cryptocurrencies (CoinGecko IDs)
cryptos = {
    "BTC": "bitcoin", "ETH": "ethereum", "BNB": "binancecoin", "XRP": "ripple",
    "ADA": "cardano", "DOGE": "dogecoin", "SOL": "solana", "DOT": "polkadot",
    "LTC": "litecoin", "BCH": "bitcoin-cash", "XLM": "stellar", "LINK": "chainlink",
    "UNI": "uniswap", "AVAX": "avalanche-2", "MATIC": "matic-network",
    "TRX": "tron", "ETC": "ethereum-classic", "NEO": "neo", "EOS": "eos",
    "XMR": "monero"
}

# List of currencies
currencies = ["USD", "EUR", "GBP", "JPY", "NGN", "CAD", "CHF", "CNY", "INR", "SGD",
              "ZAR", "HKD", "BRL", "KRW", "SEK", "NZD", "MXN", "MYR", "RUB", "AUD"]

# Dictionary to map currency codes to symbols
currency_symbols = {
    "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥", "NGN": "₦", "CAD": "C$", "CHF": "CHF",
    "CNY": "¥", "INR": "₹", "SGD": "S$", "ZAR": "R", "HKD": "HK$", "BRL": "R$", "KRW": "₩",
    "SEK": "kr", "NZD": "NZ$", "MXN": "MX$", "MYR": "RM", "RUB": "₽", "AUD": "A$"
}

# Function to get crypto price with symbol
def get_crypto_price(crypto, currency):
    crypto_id = cryptos.get(crypto.upper())  # Convert symbol to API ID
    if not crypto_id:
        return "Invalid Symbol"
    
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies={currency.lower()}"
    response = requests.get(url)
    data = response.json()
    
    price = data.get(crypto_id, {}).get(currency.lower(), "Invalid Symbol")

    # Get currency symbol
    symbol = currency_symbols.get(currency.upper(), currency)  # Default to currency code if symbol not found

    return f"{symbol}{price}"  # Return formatted price with symbol

# Function to generate price chart
def generate_chart():
    x = ["1D", "1W", "1M", "3M", "1Y"]
    y = [50, 55, 53, 60, 70]  # Sample data
    
    plt.figure(figsize=(6, 3))
    plt.plot(x, y, marker="o", linestyle="-", color="cyan")
    plt.xlabel("Time", fontsize=14)
    plt.ylabel("Price")
    plt.title("Price Trend")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.xticks(fontsize=12)

    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode()
    return f"data:image/png;base64,{chart_url}"

@app.route("/", methods=["GET", "POST"])
def index():
    price = None
    chart = None
    selected_crypto = "BTC"  # Default crypto
    selected_currency = "USD"  # Default currency

    if request.method == "POST":
        selected_crypto = request.form["crypto"]
        selected_currency = request.form["currency"]
        price = get_crypto_price(selected_crypto, selected_currency)
        chart = generate_chart()

    return render_template("index.html", 
                           cryptos=cryptos.keys(), 
                           currencies=currencies, 
                           price=price, 
                           chart=chart, 
                           selected_crypto=selected_crypto, 
                           selected_currency=selected_currency)

if __name__ == "__main__":
    app.run(debug=True)
