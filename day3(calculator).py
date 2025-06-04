import math
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
#main fucntion
def main():
    print("🌟 Welcome to the Dual-Mode Calculator 🌟")
    while True:
        print("\nMain Menu:")
        print("1. Basic Calculator")
        print("2. Advanced Calculator")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()
        if choice == '1':
            basic_calculator()
        elif choice == '2':
            advanced_calculator()
        elif choice == '3':
            print("Thank you for using the Dual-Mode Calculator. Goodbye!")
            break
        else:
            print("Invalid choice! Please select a valid option from the menu.")
main()