import numpy as np
import matplotlib.pyplot as plt
def simple_interest(principal, rate, time):
    """Calculate simple interest."""
    return (principal * rate * time) / 100
def compound_interest(principal, rate, time, n=1):
    """Calculate compound interest."""
    amount = principal * (1 + (rate / (n * 100))) ** (n * time)
    return amount - principal
def plot_interest_growth(principal, rate, time):
    """Plot interest growth over time for both Simple and Compound Interest."""
    years = np.arange(1, time + 1)
    simple_interests = np.array([simple_interest(principal, rate, t) for t in years])
    compound_interests = np.array([compound_interest(principal, rate, t) for t in years])
#graph plotting
    plt.figure(figsize=(10, 6))
    plt.plot(years, simple_interests, label="Simple Interest", marker='o', linestyle='--', color='blue')
    plt.plot(years, compound_interests, label="Compound Interest", marker='s', linestyle='-', color='green')

    plt.title("Interest Growth Over Time", fontsize=16)
    plt.xlabel("Time (Years)", fontsize=12)
    plt.ylabel("Interest (₹)", fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True)
    plt.show()
def interest_calculator():
    print("\n💰 Welcome to the Enhanced Interest Calculator 💰")
    print("=" * 50)
    while True:
        print("\nChoose the type of interest calculation:")
        print("1. Simple Interest")
        print("2. Compound Interest")
        print("3. Visualize Interest Growth")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()
        if choice in ['1', '2', '3']:
            try:
                principal = float(input("Enter the principal amount (₹): "))
                rate = float(input("Enter the annual interest rate (%): "))
                time = int(input("Enter the time in years: "))
                if principal <= 0 or rate <= 0 or time <= 0:
                    print("⚠️ All values must be positive numbers. Please try again.")
                    continue
                if choice == '1':
#simple interest calc
                    interest = simple_interest(principal, rate, time)
                    print(f"\n📝 Simple Interest: ₹{interest:.2f}")
                elif choice == '2':
#compound interest calc
                    n = int(input("Enter the number of times interest is compounded per year: "))
                    if n <= 0:
                        print("⚠️ Compounding frequency must be a positive integer. Please try again.")
                        continue
                    interest = compound_interest(principal, rate, time, n)
                    print(f"\n📝 Compound Interest: ₹{interest:.2f}")
                elif choice == '3':
#plot interest growth
                    plot_interest_growth(principal, rate, time)
            except ValueError:
                print("⚠️ Invalid input. Please enter numeric values only.")
        elif choice == '4':
            print("\nThank you for using the Enhanced Interest Calculator! Goodbye! 💸")
            break
        else:
            print("⚠️ Invalid choice. Please select 1, 2, 3, or 4.")
if __name__ == "__main__":
    interest_calculator()