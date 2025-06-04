import matplotlib.pyplot as plt
import timeit
def factorial_recursive(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial_recursive(n - 1)
def factorial_iterative(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result
def visualize_factorial_growth(max_num=10):
    numbers = list(range(max_num + 1))
    factorials = [factorial_iterative(n) for n in numbers]
    plt.figure(figsize=(10, 6))
    plt.plot(numbers, factorials, marker='o', color='teal', label='Factorial Growth')
    plt.title("Factorial Growth Rate", fontsize=16)
    plt.xlabel("Number", fontsize=14)
    plt.ylabel("Factorial Value", fontsize=14)
    plt.yscale("log")  # Log scale for better visibility
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend(fontsize=12)
    plt.show()
def compare_execution_times(n):
    recursive_time = timeit.timeit(lambda: factorial_recursive(n), number=1000)
    iterative_time = timeit.timeit(lambda: factorial_iterative(n), number=1000)
    print(f"\n⏱ Execution Time for n = {n}:")
    print(f"   Recursive Method: {recursive_time:.6f} seconds")
    print(f"   Iterative Method: {iterative_time:.6f} seconds")
def factorial_finder():
    print("\n🎯 Welcome to the Factorial Finder 🎯")
    print("=" * 50)
    while True:
        print("\nChoose a method or feature:")
        print("1. Recursive Method")
        print("2. Iterative Method")
        print("3. Compare Both Methods")
        print("4. Visualize Factorial Growth (Matplotlib)")
        print("5. Compare Execution Times (Timeit)")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()
        if choice in ['1', '2', '3', '4', '5']:
            try:
                if choice in ['1', '2', '3']:
                    num = int(input("Enter a non-negative integer: "))
                    if num < 0:
                        print("⚠️ Factorial is only defined for non-negative integers. Please try again.")
                        continue
                if choice == '1':
                    result = factorial_recursive(num)
                    print(f"\n📐 Factorial of {num} (Recursive): {result}")
                elif choice == '2':
                    result = factorial_iterative(num)
                    print(f"\n📐 Factorial of {num} (Iterative): {result}")
                elif choice == '3':
                    recursive_result = factorial_recursive(num)
                    iterative_result = factorial_iterative(num)
                    print(f"\n📊 Comparison:")
                    print(f"   Recursive Result: {recursive_result}")
                    print(f"   Iterative Result: {iterative_result}")
                elif choice == '4':
                    max_num = int(input("Enter the maximum number for visualization: "))
                    if max_num < 0:
                        print("⚠️ Visualization is only defined for non-negative integers. Please try again.")
                        continue
                    visualize_factorial_growth(max_num)
                elif choice == '5':
                    num = int(input("Enter a number to compare execution times: "))
                    if num < 0:
                        print("⚠️ Comparison is only defined for non-negative integers. Please try again.")
                        continue
                    compare_execution_times(num)
            except ValueError:
                print("⚠️ Invalid input. Please enter a valid non-negative integer.")
        elif choice == '6':
            print("\nThank you for using the Factorial Finder! Goodbye! 🧮")
            break
        else:
            print("⚠️ Invalid choice. Please select 1, 2, 3, 4, 5, or 6.")
if __name__ == "__main__":
    factorial_finder()