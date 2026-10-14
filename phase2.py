def priority(op):
    if op == "+" or op == "-":
        return 1
    elif op == "*" or op == "/":
        return 2
    return 0

def make_tree(values, operators):
    op = operators.pop()
    right = values.pop()
    left = values.pop()
    values.append([op, left, right])

def evaluate(tree):
    if isinstance(tree, int):
        return tree

    left = evaluate(tree[1])
    right = evaluate(tree[2])
    if tree[0] == "+":
        return left + right
    elif tree[0] == "-":
        return left - right
    elif tree[0] == "*":
        return left * right
    elif tree[0] == "/":
        return left / right

def get_depth(tree):
    if isinstance(tree, int):
        return 1

    return 1 + max(get_depth(tree[1]), get_depth(tree[2]))

def print_tree(tree):
    depth = get_depth(tree)

    width = 4 * (2 ** depth)
    height = 2 * depth - 1
    grid = [[" "] * width for _ in range(height)]

    def put_text(x, y, text):
        start = x - len(text) // 2
        for i in range(len(text)):
            if 0 <= start + i < width:
                grid[y][start + i] = text[i]

    def draw(tree, level, x):
        if isinstance(tree, int):
            put_text(x, level * 2, str(tree))
            return

        put_text(x, level * 2, str(tree[0]))
        remaining = depth - level - 1
        if remaining > 0:
            gap = 4 * (2 ** (remaining - 1))
        else:
            gap = 2

        left_x = x - gap
        right_x = x + gap
        branch_y = level * 2 + 1

        if left_x < x:
            branch_x = (x + left_x) // 2
            grid[branch_y][branch_x] = "/"

        if right_x > x:
            branch_x = (x + right_x) // 2
            grid[branch_y][branch_x] = "\\"

        draw(tree[1], level + 1, left_x)
        draw(tree[2], level + 1, right_x)

    draw(tree, 0, width // 2)
    for row in grid:
        print("".join(row).rstrip())

expression = input("Enter expression: ")
values = []
operators = []
i = 0
while i < len(expression):
    if expression[i] == " ":
        i += 1
        continue

    if expression[i].isdigit():
        number = ""
        while i < len(expression) and expression[i].isdigit():
            number += expression[i]
            i += 1

        values.append(int(number))
        continue

    if expression[i] == "(":
        operators.append(expression[i])

    elif expression[i] == ")":
        while operators and operators[-1] != "(":
            make_tree(values, operators)

        if operators:
            operators.pop()

    elif expression[i] in "+-*/":

        while (operators and
               operators[-1] != "(" and
               priority(operators[-1]) >= priority(expression[i])):

            make_tree(values, operators)

        operators.append(expression[i])

    i += 1


while operators:
    make_tree(values, operators)
tree = values[0]
print("\nExpression Tree:")
print_tree(tree)
print("\nResult:", evaluate(tree))