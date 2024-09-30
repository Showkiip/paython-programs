# recursive functions

def foo(n):
    if n <= 5:
        return 12
    return foo(n - 2) * foo(n - 1)

result = foo(8)
print("recursive => ",result)


def factorial(n):
    if n == 0 or n ==1:
        return 1
    else:
        return n * factorial(n-1)

print(factorial(5))