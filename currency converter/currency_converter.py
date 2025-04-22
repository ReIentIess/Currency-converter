import requests
import os
from colorama import Fore, Style, init
from dotenv import load_dotenv
import time
try:
    from currency_list import currencies
except ModuleNotFoundError:
    print(Fore.RED + f"Currency list file not found, please re-download the program!" + Style.RESET_ALL)
    time.sleep(3)

init()
load_dotenv()

text = Fore.GREEN + """         _____                                                                      _            
        /  __ \\                                                                    | |           
        | /  \\/_   _ _ __ _ __ ___ _ __   ___ _   _    ___ ___  _ ____   _____ _ __| |_ ___ _ __ 
        | |   | | | | '__| '__/ _ \\ '_ \\ / __| | | |  / __/ _ \\| '_ \\ \\ / / _ \\ '__| __/ _ \\ '__|
        | \\__/\\ |_| | |  | | |  __/ | | | (__| |_| | | (_| (_) | | | \\ V /  __/ |  | ||  __/ |   
         \\____/\\__,_|_|  |_|  \\___|_| |_|\\___|\\__, |  \\___\\___/|_| |_|\\_/ \\___|_|   \\__\\___|_|   
                                               __/ |                                             
                                              |___/                                              """ + Style.RESET_ALL

api_key = os.getenv("API_KEY")
if not api_key:
    print(Fore.RED + "API-Key is mising. Please create a .env-File with your API-Key!" + Style.RESET_ALL)
    input(Fore.RED + "Press enter to exit. . . " + Style.RESET_ALL)
    exit()
base_url = f"https://api.freecurrencyapi.com/v1/latest?apikey={api_key}"

def clear_terminal():
    os.system("cls")

def get_input(prompt):
    user_input = input(prompt).strip().upper()
    if user_input == "Q":
        print(Fore.YELLOW + "Exiting the program..." + Style.RESET_ALL)
        exit()
    return user_input


def currency_converter(main_currency, convert_currency):
    url = f"{base_url}&currencies={convert_currency}&base_currency={main_currency}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(Fore.RED + f"Failed to retrieve data {response.status_code}" + Style.RESET_ALL)
        input(Fore.GREEN + "\nPress enter to continue. . .")

def main():
    is_running = True

    while is_running:
        clear_terminal()
        print(f"{text}\n" + Fore.YELLOW + "       ENTER Q ANYTIME TO EXIT" + Style.RESET_ALL)
        print(Fore.GREEN + "\n       Available currencys:" + Style.RESET_ALL)

        for currency, currency_name in currencies.items():
            print(Fore.GREEN + f"       {currency}: {currency_name}" + Style.RESET_ALL)

        get_main_currency = get_input("\n\nEnter the currency you want to convert from: ")

        get_main_currency_amount = get_input("Enter the amount: ")
        try:
            amount = float(get_main_currency_amount)
        except ValueError:
            print(Fore.RED + "Please enter a valid number!" + Style.RESET_ALL)
            time.sleep(1.5)
            continue

        get_convert_currency = get_input("Enter the currency you want to convert to: ").upper()

        if get_main_currency not in currencies or get_convert_currency not in currencies:
            print(Fore.RED + "Please enter a available currency!" + Style.RESET_ALL)
            time.sleep(1.5)
            continue
        else:
            result = currency_converter(get_main_currency, get_convert_currency)
            if result:
                result = float(result['data'][f'{get_convert_currency}'])
                price = result * amount
                print(Fore.GREEN + f"\n{amount} {get_main_currency} = {round(price, 2)} {get_convert_currency}" + Style.RESET_ALL)
                input(Fore.GREEN + "\nPress enter to continue. . .")

if __name__ == "__main__":
    main()