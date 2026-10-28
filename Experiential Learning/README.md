# Expression Tree Generator and Evaluator

A comprehensive, college-level computer science project that builds, visualizes, and evaluates mathematical **Binary Expression Trees** from infix arithmetic expressions.

Built with **Pure Python (Flask)** on the backend and **HTML5 + Tailwind CSS** on the frontend. No external JavaScript charting libraries or dangerous `eval()` functions are used.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/tejalselokar25/Experiential-Learning)

---

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Theoretical Concepts](#theoretical-concepts)
  - [What is an Expression Tree?](#what-is-an-expression-tree)
  - [Parsing Algorithm: Recursive Descent vs Shunting Yard](#parsing-algorithm-recursive-descent-vs-shunting-yard)
  - [Operator Precedence & Associativity](#operator-precedence--associativity)
  - [Tree Traversals](#tree-traversals)
  - [Step-by-Step Evaluation via Post-Order Traversal](#step-by-step-evaluation-via-post-order-traversal)
- [Supported Syntax & Operators](#supported-syntax--operators)
- [Sample Test Cases](#sample-test-cases)
- [Project Structure](#project-structure)
- [Installation and Execution Instructions](#installation-and-execution-instructions)
- [Security Considerations](#security-considerations)
- [Viva Questions & Answers for 2nd Year CSE](#viva-questions--answers-for-2nd-year-cse)

---

## 🎯 Project Overview

In Computer Science and Compiler Design, an **Expression Tree** is an Abstract Syntax Tree (AST) representing a mathematical or logical expression. Internal nodes represent operators, and leaf nodes represent operands.

This project delivers:
1. **Mathematical Expression Parsing**: Converts human-typed arithmetic expressions into structured syntactic tokens.
2. **Binary Tree Generation**: Builds a strictly typed hierarchical tree adhering to algebraic precedence and associativity.
3. **Pure Python Tree Visualization**: Generates scalable vector graphics (SVG) diagrams server-side with zero external JavaScript dependencies.
4. **Tree Traversals**: Generates Prefix (Polish notation), Infix (standard arithmetic), and Postfix (Reverse Polish notation) representations.
5. **Step-by-Step Execution Trace**: Evaluates the tree from the bottom up in post-order execution order, showing sub-expression reductions.
6. **Graceful Error Handling**: Detects syntax errors, unbalanced parentheses, invalid operators, division by zero, and numerical overflows with human-readable error banners.

---

## ✨ Key Features

- **Pure Python Tree Engine**: Zero external mathematical or graph parsing packages.
- **Strict Security**: Completely avoids Python's built-in `eval()`, `exec()`, and unrestricted `ast.literal_eval()`.
- **Interactive Hover-to-Calculate Effect**:
  - **Operator Nodes**: Hovering over any operator (`+`, `-`, `*`, `/`, etc.) highlights the node, its direct children, and connecting edges, displaying an instant tooltip with the operation type, calculation equation, and result.
  - **Operand Nodes**: Hovering over a numeric leaf highlights the operand and its connecting parent edge, displaying its value and the parent subtree expression in which it participates.
  - **Calculation Inspector**: A dedicated sticky side-panel updating live with detailed node type, subtrees, immediate reductions, computed values, and explanations.
- **Interactive SVG Tree Rendering**: Pure Python dynamically calculates non-overlapping (x, y) coordinates and draws smooth cubic Bezier connectors, circular operator nodes, and rounded operand chips. Static layout with zero auto-playing animations.
- **Dynamic Step-by-Step Trace**: Real-time post-order reduction trace showing each sub-expression evaluation.
- **Comprehensive Operator Support**:
  - Binary: `+`, `-`, `*`, `/`, `//` (integer division), `%` (modulo), `**` (exponentiation).
  - Unary: `+`, `-` (e.g. `-5 + 3`, `4 * -2`, `-(3 + 5)`).
  - Parentheses: `(`, `)`.
  - Floating point / decimal numbers (`3.5 + 2.5`).
- **Academic Modern UI**: Responsive layout styled with Tailwind CSS, supporting desktop, tablet, and mobile browsers.

---

## 🏗️ System Architecture

```text
[ User Input Expression ]
           │
           ▼
     [ Tokenizer ] ───────► Converts string into typed Tokens (NUMBER, OP, LPAREN, RPAREN)
           │
           ▼
 [ Recursive Descent ] ───► Applies Grammar, Precedence & Associativity Rules
           │
           ▼
    [ TreeNode AST ] ─────► Root of Binary Expression Tree
           │
     ┌─────┼─────────────────────────┬────────────────────────┐
     ▼     ▼                         ▼                        ▼
[Evaluator] [Traversals]      [Tree Statistics]       [Tree Visualizer]
  - Safe post-order - Prefix (Pre-order)    - Total Node Count      - Pure Python SVG
  - Division by zero- Infix (In-order)      - Tree Height (Depth)   - ASCII Tree View
  - Step trace      - Postfix (Post-order)  - Ops & Operands Count
```

---

## 📚 Theoretical Concepts

### What is an Expression Tree?
An Expression Tree is a binary tree where:
- Every **leaf node** represents an operand (constant number).
- Every **internal node** represents an operator.
- Subtrees rooted at any operator node represent valid sub-expressions.

### Parsing Algorithm: Recursive Descent vs Shunting Yard
This project implements a **Recursive-Descent Parser** based on a formal context-free grammar:

```ebnf
expression     ::= term ( ('+' | '-') term )*
term           ::= unary ( ('*' | '/' | '//' | '%') unary )*
unary          ::= ('+' | '-') unary | exponentiation
exponentiation ::= primary ( '**' unary )?      (* Right-Associative *)
primary        ::= NUMBER | '(' expression ')'
```

#### Why Recursive Descent?
- Directly generates tree nodes without secondary stack translation passes.
- Provides character-exact syntax error positions (e.g., unmatched parentheses or missing operands).
- Naturally mirrors algebraic operator hierarchy.

### Operator Precedence & Associativity

| Precedence | Operator | Description | Associativity |
|:---:|:---:|:---:|:---:|
| **5 (Highest)** | `( )` | Grouping parentheses | N/A |
| **4** | `**` | Exponentiation / Power | **Right-to-Left** |
| **3** | Unary `+`, `-` | Positive / Negation | **Right-to-Left** |
| **2** | `*`, `/`, `//`, `%` | Multiplication, Division, Modulo | **Left-to-Right** |
| **1 (Lowest)** | `+`, `-` | Addition, Subtraction | **Left-to-Right** |

Notice that exponentiation is **right-associative**:
`2 ** 3 ** 2` evaluates as `2 ** (3 ** 2) = 2 ** 9 = 512`, not `(2 ** 3) ** 2 = 64`.

### Tree Traversals

1. **Prefix Traversal (Pre-Order): `Root → Left → Right`**
   - Yields **Polish Notation**.
   - Example for `(3 + 5) * 2 - 4 / 2`: `- * + 3 5 2 / 4 2`
2. **Infix Traversal (In-Order): `Left → Root → Right`**
   - Yields standard human-readable algebraic notation with parentheses where needed to prevent ambiguity.
   - Example: `(3 + 5) * 2 - 4 / 2`
3. **Postfix Traversal (Post-Order): `Left → Right → Root`**
   - Yields **Reverse Polish Notation (RPN)**.
   - Used by stack-based virtual machines (like JVM and Python bytecode) and Hewlett-Packard scientific calculators.
   - Example: `3 5 + 2 * 4 2 / -`

### Step-by-Step Evaluation via Post-Order Traversal
To evaluate `(3 + 5) * 2 - 4 / 2`:
1. Bottom-up post-order visits left subtree: `3 + 5 = 8`.
2. Visits parent `*`: `8 * 2 = 16`.
3. Visits right subtree: `4 / 2 = 2`.
4. Visits root `-`: `16 - 2 = 14`.
Each step is recorded and displayed dynamically in a numbered list.

---

## 🧪 Sample Test Cases

| Expression | Expected Result | Prefix | Postfix |
|---|:---:|---|---|
| `3 + 5` | `8` | `+ 3 5` | `3 5 +` |
| `(3 + 5) * 2` | `16` | `* + 3 5 2` | `3 5 + 2 *` |
| `10 - 2 * 3` | `4` | `- 10 * 2 3` | `10 2 3 * -` |
| `20 / 4 + 3` | `8` | `+ / 20 4 3` | `20 4 / 3 +` |
| `2 ** 3 ** 2` | `512` | `** 2 ** 3 2` | `2 3 2 ** **` |
| `17 % 5` | `2` | `% 17 5` | `17 5 %` |
| `17 // 5` | `3` | `// 17 5` | `17 5 //` |
| `-5 + 3` | `-2` | `+ - 5 3` | `5 u- 3 +` |
| `4 * -2` | `-8` | `* 4 - 2` | `4 2 u- *` |
| `-(3 + 5) * 2` | `-16` | `* - + 3 5 2` | `3 5 + u- 2 *` |
| `3.5 + 2.5` | `6` | `+ 3.5 2.5` | `3.5 2.5 +` |
| `10 / 0` | *Division by zero error* | - | - |

---

## 📁 Project Structure

```text
expression-tree-project/
│
├── app.py                  # Flask web application and routing
├── expression_tree.py      # Core pure-Python expression parsing & AST engine
├── test_engine.py          # Automated verification test suite
├── requirements.txt        # Minimal Python dependencies (Flask)
├── README.md               # Complete documentation and viva guide
│
├── templates/
│   └── index.html          # Responsive HTML5 + Tailwind CSS UI
│
└── static/
    └── style.css           # Custom CSS for SVG diagram styling and animations
```

---

## 🚀 Installation and Execution Instructions

### Prerequisites
- Python 3.8 or higher installed on your computer.

### Step 1: Open Terminal / PowerShell
Open PowerShell or Command Prompt in the project folder:

```bash
cd "c:\Users\ADMIN\OneDrive\Desktop\New folder"
```

### Step 2: (Optional but Recommended) Create a Virtual Environment
```bash
python -m venv venv
```

Activate the virtual environment:
- On Windows PowerShell:
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- On Windows Command Prompt (CMD):
  ```cmd
  venv\Scripts\activate.bat
  ```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Automated Tests
```bash
python test_engine.py
```

### Step 5: Start the Flask Web Application
```bash
python app.py
```

### Step 6: Access in Browser
Open your browser and navigate to:
```text
http://127.0.0.1:5000
```

---

## 🔒 Security Considerations

- **No Code Injection (`eval`/`exec`)**: Standard Python `eval()` can execute arbitrary operating system commands (e.g. `__import__('os').system('...')`). This application uses a custom lexical scanner that allows only numbers and arithmetic operators.
- **DoS Defense (Exponent Limit)**: Extremely large exponentiations like `99999 ** 99999` can freeze CPU cycles or consume excessive memory. The evaluation engine enforces an exponent threshold to prevent Denial of Service.
- **Safe HTML Escaping**: All user inputs and node strings are strictly escaped before rendering in HTML templates or SVGs.

---

## 🎓 Viva Questions & Answers for 2nd Year CSE

### Q1: What is an Expression Tree and what are its properties?
**Answer:** An Expression Tree is a binary tree used to represent arithmetic expressions. Its key properties are:
1. All **leaf nodes** are operands (numbers or variables).
2. All **internal nodes** are operators (`+`, `-`, `*`, `/`, etc.).
3. An in-order traversal of an expression tree produces the original infix expression, a pre-order traversal produces the prefix expression (Polish notation), and a post-order traversal produces the postfix expression (Reverse Polish notation).
4. For a full binary tree with $N$ operands, there are exactly $N - 1$ binary operators, resulting in $2N - 1$ total nodes.

### Q2: Why is Post-Order traversal used to evaluate an Expression Tree?
**Answer:** Post-order traversal follows the sequence `Left Subtree → Right Subtree → Root`. In arithmetic evaluation, an operator cannot be computed until both its left and right operands have been fully resolved. Evaluating in post-order ensures that child sub-expressions are evaluated bottom-up before applying the parent operator, perfectly matching how stack-based computers and calculators process instructions.

### Q3: How is operator associativity handled in parsing, especially for exponentiation?
**Answer:** Most arithmetic operators (`+`, `-`, `*`, `/`) are **left-associative**, meaning `a - b - c` is grouped as `(a - b) - c`. In recursive-descent parsing, left-associative operators are consumed in a loop (`while` loop). 
Conversely, exponentiation (`**`) is **right-associative**, meaning `a ** b ** c` is grouped as `a ** (b ** c)`. To implement right-associativity in recursive descent, the parser calls the exponentiation rule recursively for the right child instead of in a flat loop.

### Q4: How does this project handle Unary Operators (like `-5` or `-(3 + 5)`)?
**Answer:** A unary operator takes only one operand. In the tokenizer/parser, a `+` or `-` is identified as unary if it appears at the beginning of an expression, directly following an opening parenthesis `(`, or directly following another operator (e.g. `4 * -2`). In the tree, a unary node is represented with `left = None`, `right = child`, and a flag `is_unary = True`. During evaluation, it applies the sign directly to its single right child.

### Q5: Why is building a custom parser safer than using Python's `eval()` function?
**Answer:** Python's built-in `eval()` function evaluates arbitrary Python code with the privileges of the running server. A malicious user could input `__import__('os').remove('app.py')` or extract sensitive environment variables. A custom tokenizer and parser only recognize predefined mathematical tokens (digits, basic operators, and parentheses), making arbitrary code execution impossible by design.
