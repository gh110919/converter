from typing import Dict
import aiohttp
import asyncio

# URL API для получения текущих курсов валют относительно USD
API_URL: str = "https://v6.exchangerate-api.com/v6/64d487d3afd57079bfc6e376/latest/USD"


# Асинхронная функция для получения данных о курсах валют
async def fetch_currency_rates() -> Dict[str, float]:
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as response:
            data = await response.json()
            return data["conversion_rates"]


# Приветственное сообщение для пользователя
def print_welcome_message() -> None:
    print("\n\nДобро пожаловать в ламповый консольный конвертер валют\n\n")
    print("""Наша программа поможет вам конвертировать валюту.
- Выбор имеющейся валюты.
- Выбор валюты конвертации.
- Ввод суммы имеющейся валюты.\n\n""")


# Запрос у пользователя, хочет ли он увидеть список доступных валют
def ask_to_show_currencies() -> str:
    question = "Хотите увидеть список доступных валют? (y/n): "
    return input(question).strip().lower()


# Функция для проверки ввода пользователя на корректность валюты
def get_valid_currency(prompt: str, rates: Dict[str, float]) -> str:
    while True:
        user_currency: str = input(prompt).upper()
        if user_currency in rates:
            return user_currency
        print("Такая валюта отсутствует. Попробуйте ещё раз.")


# Асинхронная функция для конвертации валюты
async def convert_currency(source: str, target: str, amount: float, rates: Dict[str, float]) -> float:
    # Получаем курс исходной валюты относительно USD
    source_rate: float = rates[source]
    # Получаем курс целевой валюты относительно USD
    target_rate: float = rates[target]
    # Конвертируем сумму из исходной валюты в целевую
    return (amount / source_rate) * target_rate


# Основная асинхронная функция
async def main() -> None:
    # Получаем курсы валют
    rates: Dict[str, float] = await fetch_currency_rates()

    # Приветственное сообщение
    print_welcome_message()

    # Запрос на показ списка валют
    show_currencies: str = ask_to_show_currencies()
    if show_currencies in ["yes", "y"]:
        print("\nСписок доступных валют:")
        for index, currency_code in enumerate(rates):
            print(f"{index + 1}. {currency_code}")
        print("\n")

    # Получаем валюту для конвертации
    source: str = get_valid_currency("\n\nВведите имеющуюся валюту:\n", rates)
    amount: float = float(input("\n\nВведите количество вашей валюты:\n"))
    target: str = get_valid_currency(
        "\n\nВведите валюту для конвертации:\n", rates)

    # Конвертируем валюту
    converted: float = await convert_currency(source, target, amount, rates)
    print(f"\n\nИтого:\n{round(converted, 2)} {target}")
