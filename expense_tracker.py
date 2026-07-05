"""Simple command-line expense tracker backed by a JSON file."""
import json, sys
from datetime import date
from pathlib import Path

DATA_FILE = Path("expenses.json")

def load_expenses():
    return json.loads(DATA_FILE.read_text(encoding="utf-8")) if DATA_FILE.exists() else []

def save_expenses(expenses):
    DATA_FILE.write_text(json.dumps(expenses, indent=2), encoding="utf-8")

def add_expense(description, amount, category="general"):
    expenses = load_expenses()
    expenses.append({"date": date.today().isoformat(), "description": description,
                      "amount": round(float(amount), 2), "category": category})
    save_expenses(expenses)
    print(f"Added: {description} (${amount}) [{category}]")

def list_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return
    for e in expenses:
        print(f"{e['date']}  {e['description']:<25} ${e['amount']:>8.2f}  ({e['category']})")

def delete_expense(index_str):
    """Deletes an expense using its 1-based list index number."""
    expenses = load_expenses()
    try:
        # Convert user's 1-based input to 0-based Python index
        idx = int(index_str) - 1
        if 0 <= idx < len(expenses):
            removed = expenses.pop(idx)
            save_expenses(expenses)
            print(f"Deleted: {removed['description']} (${removed['amount']})")
        else:
            print(f"Error: Number {index_str} is out of range.")
    except ValueError:
        print("Error: Please provide a valid item number.")

def total_expenses():
    print(f"Total spent: ${sum(e['amount'] for e in load_expenses()):.2f}")

def main():
    if len(sys.argv) < 2:
        print("Usage: expense_tracker.py [add|list|total] ...")
        return
    command, args = sys.argv[1], sys.argv[2:]
    if command == "add" and len(args) >= 2:
        add_expense(args[0], args[1], args[2] if len(args) > 2 else "general")
    elif command == "list":
        list_expenses()
    elif command == "total":
        total_expenses()
    else:
        print("Unknown command or missing arguments.")

if __name__ == "__main__":
    main()
