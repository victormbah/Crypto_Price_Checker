from flask import Flask, render_template, request
import requests
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# List of 20 cryptocurrencies
cryptos = [
    "BTC", "ETH", "BNB", "XRP", "ADA", "DOGE", "SOL", "DOT", "LTC", "BCH",
    "XLM", "LINK", "UNI", "AVAX", "MATIC", "TRX", "ETC", "NEO", "EOS", "XMR"
]

# List of 20 currencies (including NGN)
currencies = [
    "USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "INR", "SGD",
    "NGN", "ZAR", "HKD", "BRL", "KRW", "SEK", "NZD", "MXN", "MYR", "RUB"
]

# Function to get crypto price
def get_crypto_price(crypto, currency):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto.lower()}&vs_currencies={currency.lower()}"
    response = requests.get(url)
    data = response.json()
    
    return data.get(crypto.lower(), {}).get(currency.lower(), "Invalid Symbol")

# Function to generate a simple price chart
def generate_chart(crypto, currency):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto.lower()}/market_chart?vs_currency={currency.lower()}&days=7"
    response = requests.get(url)
    
    if response.status_code != 200:
        return None

    data = response.json()
    prices = [entry[1] for entry in data.get("prices", [])]
    days = list(range(1, len(prices) + 1))

    plt.figure(figsize=(6, 3))
    plt.plot(days, prices, marker="o", linestyle="-", color="cyan", markersize=5)
    plt.title(f"{crypto.upper()} Price in {currency.upper()} (Last 7 Days)")
    plt.xlabel("Days")
    plt.ylabel(f"Price in {currency.upper()}")
    plt.grid(True)
    plt.tight_layout()

    # Save the chart to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png", transparent=True)
    buf.seek(0)
    chart_data = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close()
    
    return chart_data

@app.route("/", methods=["GET", "POST"])
def index():
    price = None
    chart = None
    selected_crypto = "BTC"
    selected_currency = "USD"

    if request.method == "POST":
        selected_crypto = request.form.get("crypto", "BTC")
        selected_currency = request.form.get("currency", "USD")

        price = get_crypto_price(selected_crypto, selected_currency)
        chart = generate_chart(selected_crypto, selected_currency)

    return render_template(
        "index.html",
        price=price,
        chart=chart,
        cryptos=cryptos,
        currencies=currencies,
        selected_crypto=selected_crypto,
        selected_currency=selected_currency
    )

if __name__ == "__main__":
    app.run(debug=True)
