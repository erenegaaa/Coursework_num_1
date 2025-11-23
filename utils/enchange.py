import os
import requests
import dotenv
dotenv.load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY not found. Add it to your .env file.")

url = "https://api.apilayer.com/exchangerates_data/convert"

params = {
    "from": "USD",
    "to": "EUR",
    "amount": 10
}

headers = {
    "apikey": API_KEY
}

response = requests.get(url, params=params, headers=headers)
print(response.json())
