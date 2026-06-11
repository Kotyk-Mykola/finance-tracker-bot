import json
from datetime import datetime
import os

DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"budget": 0.0, "expenses": []}
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except:
        return {"budget": 0.0, "expenses": []}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def show_help():
    print("\n--- Доступні команди ---")
    print("1. 'допомога' - Список команд")
    print("2. 'встановити бюджет' - Задати загальний бюджет")
    print("3. 'додати витрату' - Записати нову витрату")
    print("4. 'показати витрати' - Список усіх витрат")
    print("5. 'фільтр витрат' - Пошук витрат за датою або категорією")
    print("6. 'залишок' - Скільки коштів залишилося")
    print("7. 'звіт за категоріями' - Сума витрат по кожній категорії")
    print("8. 'вийти' - Завершення роботи")
    print("------------------------")

def set_budget(data):
    try:
        amount = float(input("Введіть суму бюджету: "))
        if amount < 0:
            print("Бюджет не може бути від'ємним!")
            return
        data["budget"] = amount
        save_data(data)
        print(f"Бюджет успішно встановлено: {amount} грн.")
    except ValueError:
        print("Помилка: введіть числове значення.")

def check_budget_warning(data):
    total_expenses = sum(exp["amount"] for exp in data["expenses"])
    if total_expenses > data["budget"]:
        print(f"⚠️ УВАГА: Ви перевищили встановлений бюджет на {total_expenses - data['budget']} грн!")

def add_expense(data):
    try:
        amount = float(input("Введіть суму витрати: "))
        if amount <= 0:
            print("Сума має бути більшою за нуль.")
            return
        
        category = input("Введіть категорію (наприклад, Їжа, Транспорт): ").strip().capitalize()
        
        date_str = input("Введіть дату у форматі ДД-ММ-РРРР (або натисніть Enter для сьогоднішньої): ").strip()
        if not date_str:
            date_str = datetime.now().strftime("%d-%m-%Y")
        else:
            datetime.strptime(date_str, "%d-%m-%Y")

        comment = input("Додайте короткий коментар (необов'язково): ").strip()

        expense = {
            "amount": amount,
            "category": category,
            "date": date_str,
            "comment": comment
        }
        
        data["expenses"].append(expense)
        save_data(data)
        print("Витрату успішно додано!")
        
        check_budget_warning(data)
        
    except ValueError:
        print("Помилка: неправильний формат суми або дати. Спробуйте ще раз.")

def show_expenses(data, expenses_list=None):
    target_list = expenses_list if expenses_list is not None else data["expenses"]
    
    if not target_list:
        print("Список витрат порожній.")
        return

    print("\n--- Ваші витрати ---")
    for i, exp in enumerate(target_list, 1):
        comment_part = f" ({exp['comment']})" if exp['comment'] else ""
        print(f"{i}. Дата: {exp['date']} | {exp['category']} | Сума: {exp['amount']} грн{comment_part}")
    print("--------------------")

def filter_expenses(data):
    print("\nОберіть тип фільтра:")
    print("1 - За конкретною датою (ДД-ММ-РРРР)")
    print("2 - За категорією")
    choice = input("Ваш вибір: ").strip()

    if choice == "1":
        target_date = input("Введіть дату (ДД-ММ-РРРР): ").strip()
        filtered = [e for e in data["expenses"] if e["date"] == target_date]
        show_expenses(data, filtered)
    
    elif choice == "2":
        target_category = input("Введіть категорію: ").strip().capitalize()
        filtered = [e for e in data["expenses"] if e["category"] == target_category]
        show_expenses(data, filtered)
    else:
        print("Невідомий вибір.")

def show_balance(data):
    total_expenses = sum(exp["amount"] for exp in data["expenses"])
    balance = data["budget"] - total_expenses
    print(f"\nВстановлений бюджет: {data['budget']} грн")
    print(f"Загальні витрати: {total_expenses} грн")
    print(f"Залишок: {balance} грн")

def category_report(data):
    if not data["expenses"]:
        print("Немає даних для звіту.")
        return
        
    report = {}
    for exp in data["expenses"]:
        cat = exp["category"]
        report[cat] = report.get(cat, 0) + exp["amount"]
        
    print("\n--- Звіт за категоріями ---")
    for cat, total in report.items():
        print(f"{cat}: {total} грн")
    print("---------------------------")

def main():
    print("Привіт! Я твій бот 'Фінансовий трекер студента'.")
    data = load_data()
    show_help()

    while True:
        command = input("\nВведіть команду: ").strip().lower()

        if command == "допомога":
            show_help()
        elif command == "встановити бюджет":
            set_budget(data)
        elif command == "додати витрату":
            add_expense(data)
        elif command == "показати витрати":
            show_expenses(data)
        elif command == "фільтр витрат":
            filter_expenses(data)
        elif command == "залишок":
            show_balance(data)
        elif command == "звіт за категоріями":
            category_report(data)
        elif command == "вийти":
            print("Збереження даних... Програму завершено. До зустрічі!")
            break
        else:
            print("Невідома команда. Введіть 'допомога' для списку команд.")

if __name__ == "__main__":
    main()