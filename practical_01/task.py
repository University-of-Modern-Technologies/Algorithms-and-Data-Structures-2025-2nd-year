def are_brackets_balanced(s):
    stack = []

    brackets = {
        "(": ")",
        "[": "]",
        "{": "}",
    }

    for char in s:
        # якщо символ є відкриваючим дужкою, додаємо його до стеку
        if char in brackets:
            stack.append(char)
        # якщо символ є закриваючою дужкою, перевіряємо, чи відповідає вона останній відкриваючій дужці
        elif char in brackets.values():
            # якщо стек порожній або остання відкриваюча дужка не відповідає закриваючій, повертаємо False
            if not stack or brackets[stack.pop()] != char:
                return False
    return not stack


if __name__ == "__main__":
    examples = ["( ){[ 1 ]( 1 + 3 )( ){ }}", "( 23 ( 2 - 3);", "( 11 }", "([()])"]
    for example in examples:
        print(
            f"{example}: {'Симетрично' if are_brackets_balanced(example) else 'Несиметрично'}"
        )
