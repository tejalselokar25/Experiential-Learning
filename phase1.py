tree = ["*", ["+", 10, 5], 2]

left = tree[1]
right = tree[2]

if left[0] == "+":
    left_result = left[1] + left[2]
elif left[0] == "-":
    left_result = left[1] - left[2]
elif left[0] == "*":
    left_result = left[1] * left[2]
elif left[0] == "/":
    left_result = left[1] / left[2]

if tree[0] == "+":
    result = left_result + right
elif tree[0] == "-":
    result = left_result - right
elif tree[0] == "*":
    result = left_result * right
elif tree[0] == "/":
    result = left_result / right

print("Expression: (10 + 5) * 2")
tree = ["*", ["+", 10, 5], 2]

left = tree[1]
right = tree[2]

if left[0] == "+":
    left_result = left[1] + left[2]
elif left[0] == "-":
    left_result = left[1] - left[2]
elif left[0] == "*":
    left_result = left[1] * left[2]
elif left[0] == "/":
    left_result = left[1] / left[2]

if tree[0] == "+":
    result = left_result + right
elif tree[0] == "-":
    result = left_result - right
elif tree[0] == "*":
    result = left_result * right
elif tree[0] == "/":
    result = left_result / right

print("Result:", result)
