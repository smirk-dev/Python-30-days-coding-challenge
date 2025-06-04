import matplotlib.pyplot as plt
import numpy as np
import timeit
def fibonacci_iterative(n):
    fib_sequence = []
    a, b = 0, 1
    for _ in range(n):
        fib_sequence.append(a)
        a, b = b, a + b
    return fib_sequence
def fibonacci_recursive(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)
def visualize_fibonacci(n):
    fib_sequence = fibonacci_iterative(n)
    plt.figure(figsize=(10, 6))
    plt.plot(range(n), fib_sequence, marker='o', color='purple', label='Fibonacci Sequence')
    plt.title("Fibonacci Sequence Visualization", fontsize=16)
    plt.xlabel("Index (n)", fontsize=14)
    plt.ylabel("Fibonacci Value", fontsize=14)
    plt.grid(True, linestyle="--", linewidth=0.5)
    plt.legend(fontsize=12)
    plt.show()
def plot_fibonacci_spiral(n):
    fibonacci = fibonacci_iterative(n)
    theta = np.linspace(0, 4 * np.pi, 1000)
    a = 1
    b = 0.2
    r = a * np.exp(b * theta)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    plt.figure(figsize=(6, 6))
    plt.plot(x, y, color='orange', lw=2)
    plt.axhline(0, color='green', lw=0.5)
    plt.axvline(0, color='red', lw=0.5)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title("Fibonacci Inspired Golden Spiral", fontsize=14)
    plt.show()
def compare_execution_times(n):
    if n > 30:
        print("⚠️ Recursive approach is not recommended for large inputs due to inefficiency.")
        return
    recursive_time = timeit.timeit(lambda: [fibonacci_recursive(i) for i in range(n)], number=1)
    iterative_time = timeit.timeit(lambda: fibonacci_iterative(n), number=1)
    print(f"\n⏱ Execution Time for generating {n} terms:")
    print(f"   Recursive Method: {recursive_time:.6f} seconds")
    print(f"   Iterative Method: {iterative_time:.6f} seconds")
def fibonacci_sequence_generator():
    print("\n🌟 Welcome to the Fibonacci Sequence Generator 🌟")
    print("=" * 50)
    while True:
        print("\nChoose an option:")
        print("1. Generate Fibonacci Sequence (Iterative)")
        print("2. Generate Fibonacci Sequence (Recursive)")
        print("3. Visualize Fibonacci Sequence (Line Plot)")
        print("4. Visualize Fibonacci-Inspired Golden Spiral")
        print("5. Compare Execution Times (Recursive vs Iterative)")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()
        if choice in ['1', '2', '3', '4', '5']:
            try:
                if choice in ['1', '2', '3', '5']:
                    num = int(input("Enter the number of terms (n): "))
                    if num <= 0:
                        print("⚠️ Please enter a positive integer.")
                        continue
                if choice == '1':
                    sequence = fibonacci_iterative(num)
                    print(f"\n🔢 Fibonacci Sequence (Iterative): {sequence}")
                elif choice == '2':
                    if num > 30:
                        print("⚠️ Recursive approach is slow for n > 30. Use the iterative method instead.")
                        continue
                    sequence = [fibonacci_recursive(i) for i in range(num)]
                    print(f"\n🔢 Fibonacci Sequence (Recursive): {sequence}")
                elif choice == '3':
                    visualize_fibonacci(num)
                elif choice == '4':
                    num = int(input("Enter the number of terms to use for the spiral: "))
                    if num <= 0:
                        print("⚠️ Please enter a positive integer.")
                        continue
                    plot_fibonacci_spiral(num)
                elif choice == '5':
                    compare_execution_times(num)
            except ValueError:
                print("⚠️ Invalid input. Please enter a valid positive integer.")
        elif choice == '6':
            print("\nThank you for using the Fibonacci Sequence Generator! Goodbye! 🌀")
            break
        else:
            print("⚠️ Invalid choice. Please select 1, 2, 3, 4, 5, or 6.")
if __name__ == "__main__":
    fibonacci_sequence_generator()