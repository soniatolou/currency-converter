from currencyhandler import CurrencyHandler

def main() -> None:
    h = CurrencyHandler()
    while True:
        print("\nValutaomvandlare – meny:")
        print("[0] - Lista på alla valutor")
        print("[1] - Konvertera USD till valutor")
        print("[2] - Uppdatera fetch valuta data")
        print("[3] - Exportera till JSON")
        print("[4] - Konvertera från en valuta till en annan")
        print("[5] - Hämta historik av växlingskurs")
        print("[6] - Lista historik för en valuta")
        print("[7] - Avsluta programmet")
        choice = input("Välj ett alternativ (0-7): ").strip()

        if choice == "0":
            try:
                currencies = h.list_currencies()
                print("\nAlla tillgängliga valutor:")
                print(", ".join(currencies))
            except Exception as e:
                print("Fel när valutor skulle hämtas:", e)

        elif choice == "1":
            try:
                to_currency = input("Till vilken valuta (t.ex. SEK): ").strip().upper()
                amount_str = input("Belopp i USD: ").strip().replace(",", ".")
                amount = float(amount_str)
                result = h.convert_from_usd(to_currency, amount)
                print(f"{amount} USD = {result} {to_currency}")
            except Exception as e:
                print("Fel vid konvertering:", e)

        elif choice == "2":
            try:
                h.fetch_currency_data()
                print("Valutadata uppdaterad.")
            except Exception as e:
                print("Fel vid uppdatering:", e)

        elif choice == "3":
            try:
                h.export_to_json()
                print("Data exporterad till JSON (kolla data/-mappen).")
            except Exception as e:
                print("Fel vid export:", e) 

        elif choice == "4":
            try:
                from_currency = input("Från valuta (t.ex. SEK): ").strip().upper()
                to_currency = input("Till valuta (t.ex. EUR): ").strip().upper()
                amount_str = input(f"Belopp i {from_currency}: ").strip().replace(",", ".")
                amount = float(amount_str)
                result = h.convert_any_currency(from_currency, to_currency, amount)
                print(f"{amount} {from_currency} = {result} {to_currency}")
            except Exception as e:
                print("Fel vid konvertering:", e)

        elif choice == "5":
            try:
                date = input("Datum (YYYY-MM-DD): ").strip()
                base_input = input("Basvaluta (t.ex. USD): ").strip().upper()
                if not base_input:
                    base_input = "USD"
                data = h.get_historical_rate(date, base_input)

                print(f"Historik för {date} (bas {data.get('base', 'USD')}):")
                show_code = input("Visa kurs för specifik valuta (t.ex. SEK) eller Enter för att hoppa över: ").strip().upper()
                if show_code:
                    rate = data.get("rates", {}).get(show_code)
                    if rate is None:
                        print("Valutakoden finns inte i svaret.")
                    else:
                        base_currency = data.get("base", base_input or "USD")
                        print(f"{show_code} per 1 {base_currency} den {date}: {rate}")
                else:
                    print(f"Antal valutor i svaret: {len(data.get('rates', {}))}")
            except Exception as e:
                print("Fel vid hämtning av historik:", e)

        elif choice == "6":
            try:
                code = input("Valutakod (t.ex. SEK): ").strip().upper()
                days_str = input("Antal dagar bakåt (t.ex. 4): ").strip()
                days = int(days_str)
                series = h.list_historical_rates_for_currency(code, days)
                if not series:
                    print("Ingen historisk data hittades.")
                else:
                    print(f"Historik för {code}:")
                    for date, rate in series:
                        print(f"{date}: {rate}")
            except Exception as e:
                print("Fel vid hämtning av historik:", e)
                
        elif choice == "7":
            print("Programmet avslutas. Hej då!")
            break
        else:
            print("Ogiltigt val. Försök igen.")

if __name__ == "__main__":
    main()