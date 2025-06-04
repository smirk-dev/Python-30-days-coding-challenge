import math
import matplotlib.pyplot as plt
import numpy as np
def basic_calculator():
    print("\n🔢 Basic Calculator 🔢")
    while True:
        print("\nMenu:")
        print("1. Addition (+)")
        print("2. Subtraction (-)")
        print("3. Multiplication (*)")
        print("4. Division (/)")
        print("5. Back to Main Menu")
        choice = input("Enter your choice (1-5): ").strip() 
        if choice in ['1', '2', '3', '4']:
            try:
                num1 = float(input("Enter the first number: "))
                num2 = float(input("Enter the second number: "))
                if choice == '1':
                    print(f"The result of {num1} + {num2} is: {num1 + num2}")
                elif choice == '2':
                    print(f"The result of {num1} - {num2} is: {num1 - num2}")
                elif choice == '3':
                    print(f"The result of {num1} * {num2} is: {num1 * num2}")
                elif choice == '4':
                    if num2 != 0:
                        print(f"The result of {num1} / {num2} is: {num1 / num2}")
                    else:
                        print("Error! Division by zero.")
            except ValueError:
                print("Invalid input! Please enter numeric values only.")
        elif choice == '5':
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice! Please select a valid option from the menu.")
def advanced_calculator():
    print("\n⚙️ Advanced Calculator ⚙️")
    while True:
        print("\nMenu:")
        print("1. Trigonometric Functions (sin, cos, tan)")
        print("2. Exponential Function (e^x)")
        print("3. Logarithmic Functions (log base 10 and natural log)")
        print("4. Square Root")
        print("5. Power (x^y)")
        print("6. Back to Main Menu")
        choice = input("Enter your choice (1-6): ").strip()
        if choice == '1':
            print("\nTrigonometric Functions:")
            print("a. Sine (sin)")
            print("b. Cosine (cos)")
            print("c. Tangent (tan)")
            sub_choice = input("Choose a function (a/b/c): ").strip().lower()
            try:
                angle = float(input("Enter the angle in degrees: "))
                radians = math.radians(angle)
                if sub_choice == 'a':
                    print(f"sin({angle}) = {math.sin(radians):.4f}")
                elif sub_choice == 'b':
                    print(f"cos({angle}) = {math.cos(radians):.4f}")
                elif sub_choice == 'c':
                    print(f"tan({angle}) = {math.tan(radians):.4f}")
                else:
                    print("Invalid choice for trigonometric function!")
            except ValueError:
                print("Invalid input! Please enter a numeric value.")
        elif choice == '2':
            try:
                x = float(input("Enter the value of x: "))
                print(f"e^{x} = {math.exp(x):.4f}")
            except ValueError:
                print("Invalid input! Please enter a numeric value.")
        elif choice == '3':
            print("\nLogarithmic Functions:")
            print("a. Logarithm base 10 (log10)")
            print("b. Natural Logarithm (ln)")
            sub_choice = input("Choose a function (a/b): ").strip().lower()
            try:
                value = float(input("Enter the value: "))
                if value <= 0:
                    print("Logarithm undefined for zero or negative numbers!")
                else:
                    if sub_choice == 'a':
                        print(f"log10({value}) = {math.log10(value):.4f}")
                    elif sub_choice == 'b':
                        print(f"ln({value}) = {math.log(value):.4f}")
                    else:
                        print("Invalid choice for logarithmic function!")
            except ValueError:
                print("Invalid input! Please enter a numeric value.")
        elif choice == '4':
            try:
                value = float(input("Enter the value: "))
                if value < 0:
                    print("Square root undefined for negative numbers!")
                else:
                    print(f"sqrt({value}) = {math.sqrt(value):.4f}")
            except ValueError:
                print("Invalid input! Please enter a numeric value.")
        elif choice == '5':
            try:
                base = float(input("Enter the base (x): "))
                exponent = float(input("Enter the exponent (y): "))
                print(f"{base}^{exponent} = {math.pow(base, exponent):.4f}")
            except ValueError:
                print("Invalid input! Please enter numeric values.")
        elif choice == '6':
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice! Please select a valid option from the menu.")
def graphing_calculator():
    print("\n📈 Graphing Calculator 📈")
    while True:
        print("\nMenu:")
        print("1. Plot y = x^2")
        print("2. Plot y = sin(x)")
        print("3. Plot y = cos(x)")
        print("4. Back to Main Menu")
        choice = input("Enter your choice (1-4): ").strip()
        if choice in ['1', '2', '3']:
            x = np.linspace(-10, 10, 1000)
            if choice == '1':
                y = x**2
                title = "y = x^2"
            elif choice == '2':
                y = np.sin(x)
                title = "y = sin(x)"
            elif choice == '3':
                y = np.cos(x)
                title = "y = cos(x)"
            plt.figure(figsize=(8, 5))
            plt.plot(x, y, label=title, color="blue")
            plt.title(title)
            plt.xlabel("x")
            plt.ylabel("y")
            plt.axhline(0, color="black",linewidth=0.5)
            plt.axvline(0, color="black",linewidth=0.5)
            plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
            plt.legend()
            plt.show()
        elif choice == '4':
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice! Please select a valid option from the menu.")
def unit_converter():
    print("\n📏 Unit Converter 📏")
    while True:
        print("\nMenu:")
        print("1. Kilometers to Miles")
        print("2. Celsius to Fahrenheit")
        print("3. Kilograms to Pounds")
        print("4. Back to Main Menu")
        choice = input("Enter your choice (1-4): ").strip()
        if choice == '1':
            try:
                km = float(input("Enter distance in kilometers: "))
                miles = km * 0.621371
                print(f"{km} km is equal to {miles:.2f} miles.")
            except ValueError:
                print("Invalid input! Please enter a numeric value.")
        elif choice == '2':
            try:
                celsius = float(input("Enter temperature in Celsius: "))
                fahrenheit = (celsius * 9/5) + 32
                print(f"{celsius}°C is equal to {fahrenheit:.2f}°F.")
            except ValueError:
                print("Invalid input! Please enter a numeric value.")
        elif choice == '3':
            try:
                kg = float(input("Enter weight in kilograms: "))
                pounds = kg * 2.20462
                print(f"{kg} kg is equal to {pounds:.2f} lbs.")
            except ValueError:
                print("Invalid input! Please enter a numeric value.")
        elif choice == '4':
            print("Returning to Main Menu...")
            break
        else:
            print("Invalid choice! Please select a valid option from the menu.")
def main():
    print("🌟 Welcome to the Multi-Mode Calculator 🌟")
    while True:
        print("\nMain Menu:")
        print("1. Basic Calculator")
        print("2. Advanced Calculator")
        print("3. Graphing Calculator")
        print("4. Unit Converter")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ").strip()
        if choice == '1':
            basic_calculator()
        elif choice == '2':
            advanced_calculator()
        elif choice == '3':
            graphing_calculator()
        elif choice == '4':
            unit_converter()
        elif choice == '5':
            print("Thank you for using the Multi-Mode Calculator. Goodbye!")
            break
        else:
            print("Invalid choice! Please select a valid option from the menu.")
if __name__ == "__main__":
    main()