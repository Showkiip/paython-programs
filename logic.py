
# Recursive Fibonacci Program
def fibonacci_recursive(n):
    if n <= 1:
        return n
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

# Example usage
print(fibonacci_recursive(10))  # Output: 55



