import os
import json
import time
import requests
from dotenv import load_dotenv
from typing import Any
from datetime import datetime, timedelta
load_dotenv()

class CurrencyHandler:
    def __init__(self, base_currency: str = "usd"):
        self.app_id = os.getenv("APP_ID")
        if not self.app_id:
            raise ValueError ("APP_ID saknas! Kontrollera att den finns i .env-filen.")
        self.base_currency = base_currency.lower()
        self.data = {}
        self.rates = {}
        self.cache_dir = "data"
        self.latest_path = os.path.join(self.cache_dir, "latest.json")
        self.cache_ttl_seconds = 3600  
        os.makedirs(self.cache_dir, exist_ok=True)
        self.load_currency_data()

    

    def fetch_currency_data(self) -> dict[str, Any]:
        if not self.app_id:
            raise ValueError("APP_ID saknas! Kontrollera att den finns i .env-filen.")
        url = f"https://openexchangerates.org/api/latest.json?app_id={self.app_id}"
        headers = {"accept": "application/json"}

        try:
            resp = requests.get(url, headers=headers, timeout=10)
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Kunde inte nå API: {e}") from e

        if resp.status_code != 200:
            try:
                err = resp.json()
            except Exception:
                err = {"message": resp.text}
            raise RuntimeError(f"API-fel ({resp.status_code}): {err.get('message', err)}")
        try:
            data = resp.json()
        except ValueError as e:
            raise ValueError("Ogiltigt JSON från API") from e
        if "rates" not in data or not isinstance(data["rates"], dict):
            raise ValueError ("API-svaret saknar 'rates' eller har fel format")
        
        data["fetched_at"] = int(time.time())
        self.data = data
        self.rates = data["rates"]
        
        try:
            os.makedirs(self.cache_dir, exist_ok=True)
            with open(self.latest_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            raise IOError(f"Kunde inte skriva cache till {self.latest_path}: {e}")
        return self.data
    
    def convert_from_usd(self, to_currency: str, amount: float) -> float:
        if amount < 0:
          raise ValueError("Beloppet kan inte vara negativt.")
        to_currency = to_currency.upper()
        if to_currency not in self.rates:
          raise ValueError(f"Ogiltig valutakod: {to_currency}")
        rate = self.rates[to_currency]
        converted_amount = amount * rate
        return round(converted_amount, 2)

    def convert_any_currency(self, from_currency: str, to_currency: str, amount: float) -> float:
        if amount < 0:
            raise ValueError("Beloppet kan inte vara negativt.")
        from_currency = from_currency.upper()
        to_currency = to_currency.upper()
        if from_currency == to_currency:
            return round(float(amount), 2)
        if not self.rates:
            raise ValueError("Inga valutakurser laddade ännu, kör fetch_currency_data() först.")
        
        if from_currency not in self.rates:
            raise ValueError(f"Ogiltig valutakod: {from_currency}")
        if to_currency not in self.rates:
            raise ValueError(f"Ogiltig valutakod: {to_currency}")
    
        rate_from = self.rates[from_currency]
        rate_to = self.rates[to_currency]
        if rate_from == 0:
            raise ValueError(f"Ogiltig kurs för {from_currency} (0).")
        usd_amount = amount / rate_from
        converted_amount = usd_amount * rate_to
        
        return round(converted_amount, 2)

    def list_currencies(self) -> list[str]:
        if not self.rates:
            raise ValueError("Inga valutakurser laddade ännu, kör fetch_currency_data() först.")
        currencies = sorted(self.rates.keys())
        return currencies

    def load_currency_data(self) -> dict[str, Any]:
        try:
            if os.path.exists(self.latest_path):
                with open(self.latest_path, "r", encoding="utf-8") as f:
                    cached = json.load(f)
    
                fetched_at = cached.get("fetched_at") or cached.get("timestamp", 0)
                if (time.time() - float(fetched_at)) < self.cache_ttl_seconds:
                    self.data = cached
                    self.rates = cached.get("rates", {})
                    return self.data
                else:
                    return self.fetch_currency_data()
            else:
                return self.fetch_currency_data()
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            return self.fetch_currency_data()

    def export_to_json(self) -> None:
        if not self.data:
            raise IOError("Det finns ingen data att exportera. Hämta först med fetch_currency_data().")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_path = os.path.join(self.cache_dir, f"export_latest_{ts}.json")
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            raise IOError(f"Kunde inte skriva till fil: {e}")

    def get_historical_rate(self, date: str, base_currency: str) -> dict[str, Any]:
       
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Fel datumformat. Använd YYYY-MM-DD, tex 2025-10-12")
        
        if not self.app_id:
            raise ValueError("APP_ID saknas - lägg till den i .env.")
        url = f"https://openexchangerates.org/api/historical/{date}.json?app_id={self.app_id}"
        headers = {"accept": "application/json"}

        try:
            resp = requests.get(url, headers=headers, timeout=10)
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"kunde inte nå API: [{e}]") from e

        if resp.status_code != 200:
            try:
                err = resp.json()
            except Exception:
                err = {"message": resp.text}
            raise RuntimeError(f"API-fel ({resp.status_code}): {err.get('message', err)}")

        try:
            data = resp.json()
        except ValueError as e:
            raise ValueError("Ogiltig JSON-svar från API") from e 
        
        if "rates" not in data or not isinstance(data["rates"], dict):
            raise ValueError("API-svaret saknar 'rates' eller har fel format.")
        
        data["request_date"] = date
        data["fetched_at"] = int(time.time())

        try:
            hist_dir = os.path.join(self.cache_dir, "history")
            os.makedirs(hist_dir, exist_ok=True)
            out_path = os.path.join(hist_dir, f"{date}.json")
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
          
            pass
        
        return data 


    def list_historical_rates_for_currency(self, currency: str, days: int) -> list[tuple[str, float]]:
        currency = currency.upper()
        if days <= 0:
            raise ValueError("Antalet dagar måste vara större än 0.")

        result: list[tuple[str, float]] = []
        today = datetime.now().date()

        for i in range(days):
            date_obj = today - timedelta(days=i)
            date_str = date_obj.strftime("%Y-%m-%d")
            try:
                data = self.get_historical_rate(date_str, "USD")
                rate = data["rates"].get(currency)
                if rate is not None:
                    result.append((date_str, rate))
            except Exception:
                
                pass

        result.sort(key=lambda x: x[0]) 
        return result