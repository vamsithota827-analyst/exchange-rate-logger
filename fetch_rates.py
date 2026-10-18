import csv
import json
import os
import urllib.request
from datetime import datetime, timezone

URL = "https://api.frankfurter.dev/v1/latest?base=USD&symbols=INR,EUR,GBP"
LOG_FILE = "data/rates_log.csv"
FIELDS = ["logged_at_utc", "rate_date", "USD_INR", "USD_EUR", "USD_GBP"]


def fetch_rates():
    with urllib.request.urlopen(URL, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def append_to_log(row):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def main():
    data = fetch_rates()
    rates = data["rates"]
    row = {
        "logged_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        "rate_date": data["date"],
        "USD_INR": rates["INR"],
        "USD_EUR": rates["EUR"],
        "USD_GBP": rates["GBP"],
    }
    append_to_log(row)
    print(f"Logged: {row}")


if __name__ == "__main__":
    main()
