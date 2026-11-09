from statistics import mean
import csv
import os

expences = []
budget = 1000

if os.path.exists("expences.csv"):
    with open("expences.csv", "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            expences.append({"category": row["category"], "name": row["name"], "cost": float(row["cost"])})

def main():
    print("\n\nWellcome back!")
    get_choice()
   
def get_choice():
    valid_choices = ["new", "summary", "expences", "done", "budget"]
    
    while True:
        print("\n><><><><><><><><><><><"
                "\nWhat would you like to do today?")
        
        total = sum(item["cost"] for item in expences)
        budget_usg = total/budget
        if total > budget:
            print("------------------"
                "\nYOUR BUDGET HAS BEEN EXCEEDED!")
        elif total == budget:
            print("------------------"
                f"\nWARNING! Your budget is at it's full capacity")
        elif total >= 0.9*budget:
            print("------------------"
                f"\nBe careful! Your budget is over 90% capacity (currently at {budget_usg*100:.2f}%)")

        
        choice = input("------------------\n"
                        "(type NEW to enter new expence)\n"
                        "(type EXPENCES to get a list of your expences)\n"
                        "(type SUMMARY to get basic info about your expences)\n"
                        "(type BUDGET to change your current budget)\n"
                        "(type DONE to finish)\n"
                        "------------------\n"
        ).lower().strip()
        
        if choice not in valid_choices:
            print("Type one of the given options above")
            continue

        if choice == "new":
            get_expence()

        elif choice == "expences":
            show_expences()

        elif choice == "summary":
            show_summary()
        
        elif choice == "budget":
            change_budget()          
        else:
            print("See you later!")
            exit()


def get_expence():
    while True:
        print("\n\n--- NEW EXPENCE ---")
        category = input("Category (or DONE to finish): ").strip().capitalize()
        if not category:
            print("Please enter a category of the expence")
            continue
        elif category.lower() == "done":
            break        

        name = input("Expence name: ").strip().capitalize()
        if not name:
            print("Please enter a name of the expence")
            continue
        elif name.lower() == "done":
            print("\nCancelled new expence")
            break
        
        cost_input = input("Cost: ").strip()
        if not cost_input:
            print("Please enter a cost of the expence")
            continue
        elif cost_input.lower() == "done":
            print("\nCancelled new expence")
            break
        else:
            try:
                cost = float(cost_input)
            except ValueError:
                print("Please enter a valid number for the cost")
                continue
            if cost < 0:
                print("The cost cannot be negative")
                continue

        total = sum(item["cost"] for item in expences) 
        if total + cost > budget:
            print("\n---"
                    "\nWARNING! With this expence you will exceed your budget"
                    f"\nCurrent total: {total}"
                    f"\nYour budget: {budget}"
                    "\n---")
            if input("Are you sure to add this expence?"
                        "\n(type YES or NO) ").strip().lower() != "yes":
                print("\nCancelled new expence")
                continue
           
        expences.append({"category": category, "name": name, "cost": cost})
        file_exists = os.path.exists("expences.csv") and os.path.getsize("expences.csv") > 0
        with open("expences.csv", "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["category", "name", "cost"])
            if not file_exists:
                writer.writeheader()
            writer.writerow({"category": category, "name": name, "cost": cost})
        
        print(f"\nAdded [{category}] {name}: {cost:.2f} PLN")

def show_expences():
    while True:
        print("\n\n--- YOUR EXPENCES ---")
        if not expences:
            print("\nNo expences recorded yet")
        else:
            for item in expences:
                print(f"- [{item['category']}] {item['name']}: {item['cost']:.2f} PLN")
            print("---------------------")
        if input("\n(type DONE to finish) ").strip().lower() == "done":
            break
        else:
            print("\nPlease enter DONE to finish")


def expences_summary():
    if not expences:
        costs = 0.00
    else:
        costs = [float(item["cost"]) for item in expences]
    total = sum(costs)
    average = mean(costs) 
    largest = max(costs)
    budget_usage = (total/budget)*100

    return total, average, largest, budget_usage


def show_summary():
    while True:
        print(f"\n\n--- SUMMARY ---")
        if not expences:
            print("\nNo expences recorded yet")
        else:
            total, average, largest, budget_usage = expences_summary()
            print(f"Total: {total:.2f} PLN\nAverage: {average:.2f} PLN\nLargest: {largest:.2f} PLN")
            print("---------------")
            if total > budget:
                print("YOUR BUDGET HAS BEEN EXCEEDED!")
            elif total == budget:
                print(f"WARNING! Your budget is at is full capacity")
            elif total >= 0.9*budget:
                print(f"Be careful! Your budget is over 90% capacity (currently at {budget_usage:.2f}%)")
            else:
                print(f"Your budget is currently at {budget_usage:.2f}% capacity")
            print("---------------")
        if input("\n(type DONE to finish) ").strip().lower() == "done":
            break
        else:
            print("\nPlease enter DONE to finish")
            

def change_budget():
    global budget

    while True:
        if not expences:
            budget_usage = 0.00
        else:
            _, _, _, budget_usage = expences_summary()
            
        print("\n\n--- BUDGET ---")
        print(f"Your current budget: {budget:.2f} PLN")
        print(f"Your budget is currently at {budget_usage:.2f}% capacity")
        print("--------------")

        budget_choice = input("\n(type CHANGE to establish a new budget or DONE to finish) ").strip()
        if budget_choice.lower() == "done":
            break
        elif budget_choice.lower() == "change":
            try:
                new_budget = float(input("\nEnter your new budget: ").strip())
            except ValueError:
                print("Please enter a valid nuber for the budget")
                continue
            if new_budget < 0:
                print("Budget cannot be negative")
                continue
            budget = new_budget
            print("\n---"
                f"\nYour budget has been set to: {budget:.2f}"
                "\n---"
                )
        else:
            print("\nPlease enter CHANGE or DONE")

if __name__ == "__main__":
    main()