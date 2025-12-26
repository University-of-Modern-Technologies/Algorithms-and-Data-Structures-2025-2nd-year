def fibonacci(n, memo):
    if n in memo:
        return memo[n]
    if n <= 2:
        return 1
    memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
    return memo[n]


n = 10
memo = {}
fib_number = fibonacci(n, memo)
print(fib_number)  # 55


def fibonacci_bottom_up(n):
    # Base cases
    if n == 0:
        return 0
    elif n == 1:
        return 1

    # Починаємо з базових кейсів і нарощуємо розв'язок
    fib_numbers = [0] * (n + 1)
    fib_numbers[1] = 1

    for i in range(2, n + 1):
        fib_numbers[i] = fib_numbers[i - 1] + fib_numbers[i - 2]

    return fib_numbers[n]


n = 10
fib_number_bottom_up = fibonacci_bottom_up(n)
print(fib_number_bottom_up)  # 55
