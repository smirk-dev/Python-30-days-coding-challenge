def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32
def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9
print("🌡️ Welcome to the Temperature Converter! 🌡️")
print("Choose an option from the menu to start:\n")
while True:
    print("Menu:")
    print("1. Convert Celsius to Fahrenheit")
    print("2. Convert Fahrenheit to Celsius")
    print("3. Exit")
    choice = input("Enter your choice (1, 2, or 3): ").strip()
    if choice == '1':
        try:
            celsius = float(input("Enter temperature in Celsius: "))
            converted_temp = celsius_to_fahrenheit(celsius)
            print(f"{celsius}°C is equivalent to {converted_temp:.2f}°F\n")
        except ValueError:
            print("Invalid input! Please enter a numerical value.\n")
    elif choice == '2':
        try:
            fahrenheit = float(input("Enter temperature in Fahrenheit: "))
            converted_temp = fahrenheit_to_celsius(fahrenheit)
            print(f"{fahrenheit}°F is equivalent to {converted_temp:.2f}°C\n")
        except ValueError:
            print("Invalid input! Please enter a numerical value.\n")
    elif choice == '3':
        print("Thank you for using the Temperature Converter. Goodbye!")
        break
    else:
        print("Invalid choice! Please select option 1, 2, or 3.\n")