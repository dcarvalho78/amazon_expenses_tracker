import re
import time
from datetime import datetime

def validate_password(password):
    if (len(password) < 6 or len(password) > 20 or
        not re.search(r"[A-Z]", password) or
        not re.search(r"[a-z]", password) or
        not re.search(r"[0-9]", password) or
        not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
        return False
    return True

def validate_phone(phone):
    return bool(re.fullmatch(r"\+49[1-9][0-9]{9}", phone))

def validate_date(date_str):
    for fmt in ("%m/%d/%Y", "%m-%d-%Y"):
        try:
            return datetime.strptime(date_str, fmt).strftime("%m/%d/%Y")
        except ValueError:
            pass
    return None

def main():
    users = {}
    purchases = []
    
    # Registration
    username = input("Enter a username: ")
    while True:
        password = input("Enter a password: ")
        if validate_password(password):
            break
        print("Invalid password. Try again.")
    
    while True:
        phone = input("Enter your German phone number (+49...): ")
        if validate_phone(phone):
            break
        print("Invalid phone number. Try again.")
    
    users[username] = password
    print("Registration successful!\n")
    
    # Login
    attempts = 3
    while attempts > 0:
        login_user = input("Enter username: ")
        login_pass = input("Enter password: ")
        if users.get(login_user) == login_pass:
            print(f"Hello, {login_user}! Welcome to the Amazon Expense Tracker!")
            break
        else:
            attempts -= 1
            print(f"Invalid username or password. {attempts} attempts left.")
            if attempts == 0:
                print("Too many failed attempts. Try again in 5 seconds.")
                time.sleep(5)
                return
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Enter a purchase")
        print("2. Generate a report")
        print("3. Quit")
        choice = input("Enter your choice (1/2/3): ")
        
        if choice == "1":
            date = None
            while not date:
                date = validate_date(input("Enter the purchase date (MM/DD/YYYY or MM-DD-YYYY): "))
                if not date:
                    print("Invalid date format. Try again.")
            
            item = ""
            while len(item) < 3:
                item = input("Enter the item purchased: ")
                if len(item) < 3:
                    print("Item name must be at least 3 characters.")
            
            while True:
                try:
                    cost = float(input("Enter the total cost (EUR): "))
                    break
                except ValueError:
                    print("Invalid cost. Try again.")
            
            while True:
                try:
                    weight = float(input("Enter the weight (kg): "))
                    break
                except ValueError:
                    print("Invalid weight. Try again.")
            
            while True:
                try:
                    quantity = int(input("Enter the quantity: "))
                    if quantity >= 1:
                        break
                except ValueError:
                    print("Invalid quantity. Try again.")
            
            purchases.append({"date": date, "item": item, "cost": cost, "weight": weight, "quantity": quantity})
            print("Purchase saved.")
            
        elif choice == "2":
            if not purchases:
                print("No purchases recorded. Enter at least one purchase.")
                continue
            
            print("Generating report...\n")
            time.sleep(2)
            
            total_weight = sum(p["weight"] for p in purchases)
            total_cost = sum(p["cost"] for p in purchases)
            delivery_charges = total_weight * 1  # 1 EUR per kg
            most_expensive = max(purchases, key=lambda x: x["cost"])
            least_expensive = min(purchases, key=lambda x: x["cost"])
            avg_cost = total_cost / len(purchases)
            spending_limit = 500
            
            print("-------------------------")
            print("| Amazon Expense Report |")
            print("-------------------------")
            print(f"User: {login_user}")
            print(f"Phone: {phone[:4]}***{phone[-2:]}")
            print("----------------------------------")
            print(f"DELIVERY CHARGES: {delivery_charges:.2f} EURO")
            print(f"TOTAL ITEM COST: {total_cost:.2f} EURO")
            print("\nMOST EXPENSIVE ITEM")
            print(f"Name: {most_expensive['item']}, Cost: {most_expensive['cost']} EURO")
            print("\nLEAST EXPENSIVE ITEM")
            print(f"Name: {least_expensive['item']}, Cost: {least_expensive['cost']} EURO")
            print(f"\nAVERAGE COST PER ORDER: {avg_cost:.2f} EURO")
            print("-------------------------")
            if total_cost > spending_limit:
                print("Warning: You have exceeded the spending limit of 500 EURO!")
            else:
                print("Note: You have not exceeded the spending limit of 500 EURO.")
            
        elif choice == "3":
            print(f"Thank you for your visit, {login_user}. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")
            
if __name__ == "__main__":
    main()
