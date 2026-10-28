"""
expression_tree.py - Pure Python Expression Tree Engine
-------------------------------------------------------
Handles tokenization, recursive-descent parsing, expression tree generation,
tree traversals (Prefix, Infix, Postfix), step-by-step evaluation, tree statistics,
and server-side SVG/ASCII tree visualization without external libraries.
"""

import html
import math
from typing import List, Optional, Tuple, Dict, Any


class ExpressionError(Exception):
    """Custom exception for all mathematical and parsing expression errors."""
    def __init__(self, message: str, position: Optional[int] = None):
        super().__init__(message)
        self.message = message
        self.position = position

    def __str__(self):
        if self.position is not None:
            return f"{self.message} (at character {self.position + 1})"
        return self.message


class TokenType:
    NUMBER = "NUMBER"
    OP_ADD = "+"
    OP_SUB = "-"
    OP_MUL = "*"
    OP_DIV = "/"
    OP_FLOORDIV = "//"
    OP_MOD = "%"
    OP_POW = "**"
    LPAREN = "("
    RPAREN = ")"
    EOF = "EOF"


class Token:
    def __init__(self, token_type: str, value: Any, position: int):
        self.type = token_type
        self.value = value
        self.position = position

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, pos={self.position})"


class Tokenizer:
    """
    Lexical analyzer that converts a raw mathematical string into a stream of tokens.
    Supports integers, floating point numbers, multi-character operators (//, **),
    single-character operators (+, -, *, /, %), parentheses, and position tracking.
    """
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.length = len(text)

    def _peek(self, offset: int = 0) -> Optional[str]:
        idx = self.pos + offset
        if idx < self.length:
            return self.text[idx]
        return None

    def _advance(self) -> str:
        ch = self.text[self.pos]
        self.pos += 1
        return ch

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []

        while self.pos < self.length:
            ch = self.text[self.pos]

            # Skip whitespace
            if ch.isspace():
                self.pos += 1
                continue

            # Number (integer or decimal)
            if ch.isdigit() or (ch == '.' and self._peek(1) and self._peek(1).isdigit()):
                start_pos = self.pos
                num_str = ""
                has_dot = False

                while self.pos < self.length:
                    curr = self.text[self.pos]
                    if curr.isdigit():
                        num_str += curr
                        self.pos += 1
                    elif curr == '.':
                        if has_dot:
                            raise ExpressionError(
                                f"Invalid number with multiple decimal points: '{num_str}.'",
                                self.pos
                            )
                        has_dot = True
                        num_str += curr
                        self.pos += 1
                    else:
                        break

                val = float(num_str) if has_dot else int(num_str)
                tokens.append(Token(TokenType.NUMBER, val, start_pos))
                continue

            # Two-character operators: ** and //
            if ch == '*' and self._peek(1) == '*':
                tokens.append(Token(TokenType.OP_POW, "**", self.pos))
                self.pos += 2
                continue

            if ch == '/' and self._peek(1) == '/':
                tokens.append(Token(TokenType.OP_FLOORDIV, "//", self.pos))
                self.pos += 2
                continue

            # Single-character operators and parentheses
            if ch == '+':
                tokens.append(Token(TokenType.OP_ADD, "+", self.pos))
                self.pos += 1
            elif ch == '-':
                tokens.append(Token(TokenType.OP_SUB, "-", self.pos))
                self.pos += 1
            elif ch == '*':
                tokens.append(Token(TokenType.OP_MUL, "*", self.pos))
                self.pos += 1
            elif ch == '/':
                tokens.append(Token(TokenType.OP_DIV, "/", self.pos))
                self.pos += 1
            elif ch == '%':
                tokens.append(Token(TokenType.OP_MOD, "%", self.pos))
                self.pos += 1
            elif ch == '(':
                tokens.append(Token(TokenType.LPAREN, "(", self.pos))
                self.pos += 1
            elif ch == ')':
                tokens.append(Token(TokenType.RPAREN, ")", self.pos))
                self.pos += 1
            else:
                raise ExpressionError(f"Unsupported character '{ch}'", self.pos)

        tokens.append(Token(TokenType.EOF, "EOF", self.pos))
        return tokens


class TreeNode:
    """
    Binary Expression Tree Node.
    - Operands are leaf nodes (left=None, right=None).
    - Binary operators have both left and right children.
    - Unary operators have left=None and right=child (with is_unary=True).
    """
    _counter = 0

    def __init__(self, value: Any, left: Optional['TreeNode'] = None,
                 right: Optional['TreeNode'] = None, is_unary: bool = False):
        self.value = value
        self.left = left
        self.right = right
        self.is_unary = is_unary
        TreeNode._counter += 1
        self.id = TreeNode._counter

    def is_leaf(self) -> bool:
        return self.left is None and self.right is None

    def is_operator(self) -> bool:
        return not self.is_leaf() or isinstance(self.value, str) and self.value in {
            '+', '-', '*', '/', '//', '%', '**'
        }

    def format_value(self) -> str:
        if isinstance(self.value, float):
            return str(int(self.value)) if self.value.is_integer() else f"{self.value:.6g}"
        return str(self.value)

    def __repr__(self):
        if self.is_leaf():
            return f"Node({self.format_value()})"
        if self.is_unary:
            return f"UnaryNode({self.value}, right={self.right})"
        return f"Node({self.value}, left={self.left}, right={self.right})"


class ExpressionParser:
    """
    Recursive-descent parser implementing mathematical operator precedence and associativity:
      Precedence Level 1: '+' and '-' (binary, left-associative)
      Precedence Level 2: '*', '/', '//', '%' (binary, left-associative)
      Precedence Level 3: Unary '+' and '-' (prefix, right-associative)
      Precedence Level 4: '**' (binary, right-associative)
      Precedence Level 5: Primary (numbers, parenthesized expressions)
    """
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def _curr(self) -> Token:
        return self.tokens[self.pos]

    def _peek_type(self) -> str:
        return self.tokens[self.pos].type

    def _advance(self) -> Token:
        token = self.tokens[self.pos]
        if token.type != TokenType.EOF:
            self.pos += 1
        return token

    def parse(self) -> TreeNode:
        if self._peek_type() == TokenType.EOF:
            raise ExpressionError("Expression is empty. Please enter a valid mathematical expression.")

        root = self._parse_addition_subtraction()

        if self._peek_type() != TokenType.EOF:
            unexpected = self._curr()
            if unexpected.type == TokenType.RPAREN:
                raise ExpressionError("Unmatched closing parenthesis ')'", unexpected.position)
            raise ExpressionError(f"Unexpected token '{unexpected.value}'", unexpected.position)

        return root

    def _parse_addition_subtraction(self) -> TreeNode:
        node = self._parse_multiplication_division()

        while self._peek_type() in (TokenType.OP_ADD, TokenType.OP_SUB):
            op_token = self._advance()
            right = self._parse_multiplication_division()
            node = TreeNode(value=op_token.value, left=node, right=right, is_unary=False)

        return node

    def _parse_multiplication_division(self) -> TreeNode:
        node = self._parse_unary()

        while self._peek_type() in (TokenType.OP_MUL, TokenType.OP_DIV, TokenType.OP_FLOORDIV, TokenType.OP_MOD):
            op_token = self._advance()
            right = self._parse_unary()
            node = TreeNode(value=op_token.value, left=node, right=right, is_unary=False)

        return node

    def _parse_unary(self) -> TreeNode:
        # Unary + or -
        if self._peek_type() in (TokenType.OP_ADD, TokenType.OP_SUB):
            op_token = self._advance()
            operand = self._parse_unary()
            # If unary plus, we can either keep or fold, but keeping it represents the tree faithfully
            return TreeNode(value=op_token.value, left=None, right=operand, is_unary=True)

        return self._parse_exponentiation()

    def _parse_exponentiation(self) -> TreeNode:
        node = self._parse_primary()

        # Exponentiation is right-associative: 2 ** 3 ** 2 == 2 ** (3 ** 2)
        if self._peek_type() == TokenType.OP_POW:
            op_token = self._advance()
            # Notice recursive call to _parse_unary() / _parse_exponentiation() maintains right-associativity
            right = self._parse_unary()
            return TreeNode(value=op_token.value, left=node, right=right, is_unary=False)

        return node

    def _parse_primary(self) -> TreeNode:
        token = self._curr()

        if token.type == TokenType.NUMBER:
            self._advance()
            return TreeNode(value=token.value)

        if token.type == TokenType.LPAREN:
            self._advance()
            node = self._parse_addition_subtraction()
            if self._peek_type() != TokenType.RPAREN:
                raise ExpressionError("Missing closing parenthesis ')'", self._curr().position)
            self._advance()  # Consume ')'
            return node

        if token.type == TokenType.EOF:
            raise ExpressionError("Expression ended unexpectedly. Expected an operand or number.", token.position)

        if token.type == TokenType.RPAREN:
            raise ExpressionError("Unexpected closing parenthesis ')'", token.position)

        raise ExpressionError(f"Unexpected operator or symbol '{token.value}' where operand was expected.", token.position)


class Evaluator:
    """
    Safely evaluates the Expression Tree and records each step in post-order execution order.
    Does NOT use eval() or exec().
    """
    MAX_EXPONENT = 1000
    MAX_RESULT_DIGITS = 1000

    @classmethod
    def evaluate(cls, root: TreeNode, return_node_values: bool = False) -> Any:
        steps: List[str] = []
        node_values: Dict[int, Any] = {}

        def _format(val: Any) -> str:
            if isinstance(val, float):
                if val.is_integer() and not math.isinf(val):
                    return str(int(val))
                return f"{val:.6g}"
            return str(val)

        def _post_order(node: TreeNode) -> Any:
            if node.is_leaf():
                node_values[node.id] = node.value
                return node.value

            if node.is_unary:
                val = _post_order(node.right)
                if node.value == '-':
                    res = -val
                    steps.append(f"Evaluate -({_format(val)}) = {_format(res)}")
                elif node.value == '+':
                    res = +val
                    steps.append(f"Evaluate +({_format(val)}) = {_format(res)}")
                else:
                    raise ExpressionError(f"Unknown unary operator '{node.value}'")

                if isinstance(res, float) and res.is_integer() and not math.isinf(res):
                    res = int(res)
                node_values[node.id] = res
                return res

            # Binary operator: post-order evaluates left then right
            left_val = _post_order(node.left)
            right_val = _post_order(node.right)
            op = node.value

            try:
                if op == '+':
                    res = left_val + right_val
                elif op == '-':
                    res = left_val - right_val
                elif op == '*':
                    res = left_val * right_val
                elif op == '/':
                    if right_val == 0:
                        raise ExpressionError("Division by zero error: cannot divide by 0.")
                    res = left_val / right_val
                elif op == '//':
                    if right_val == 0:
                        raise ExpressionError("Floor division by zero error: cannot divide by 0.")
                    res = left_val // right_val
                elif op == '%':
                    if right_val == 0:
                        raise ExpressionError("Modulo by zero error: cannot modulo by 0.")
                    res = left_val % right_val
                elif op == '**':
                    # Guard against astronomical exponentiation attacks
                    if abs(right_val) > cls.MAX_EXPONENT:
                        raise ExpressionError(
                            f"Exponent too large to evaluate safely (maximum allowed power is {cls.MAX_EXPONENT})."
                        )
                    if isinstance(right_val, float) and not right_val.is_integer() and left_val < 0:
                        raise ExpressionError("Negative number cannot be raised to a non-integer power.")
                    res = left_val ** right_val
                else:
                    raise ExpressionError(f"Unsupported operator '{op}'.")

            except OverflowError:
                raise ExpressionError("Arithmetic overflow: numerical result is too large to represent.")
            except ZeroDivisionError:
                raise ExpressionError("Division by zero error: denominator cannot be 0.")

            # Format whole float results cleanly
            if isinstance(res, float) and res.is_integer() and not math.isinf(res):
                res = int(res)

            node_values[node.id] = res
            steps.append(f"Evaluate {_format(left_val)} {op} {_format(right_val)} = {_format(res)}")
            return res

        final_res = _post_order(root)
        if return_node_values:
            return final_res, steps, node_values
        return final_res, steps


class Traversals:
    """Implements Prefix, Infix, and Postfix tree traversals."""

    @staticmethod
    def prefix(node: Optional[TreeNode]) -> List[str]:
        """Root -> Left -> Right"""
        if node is None:
            return []
        if node.is_leaf():
            return [node.format_value()]
        if node.is_unary:
            return [str(node.value)] + Traversals.prefix(node.right)
        return [str(node.value)] + Traversals.prefix(node.left) + Traversals.prefix(node.right)

    @staticmethod
    def postfix(node: Optional[TreeNode]) -> List[str]:
        """Left -> Right -> Root"""
        if node is None:
            return []
        if node.is_leaf():
            return [node.format_value()]
        if node.is_unary:
            return Traversals.postfix(node.right) + [f"u{node.value}"]
        return Traversals.postfix(node.left) + Traversals.postfix(node.right) + [str(node.value)]

    @staticmethod
    def infix(node: Optional[TreeNode]) -> str:
        """
        Left -> Root -> Right with clean parentheses based on operator precedence.
        """
        if node is None:
            return ""

        prec_map = {
            '+': 1, '-': 1,
            '*': 2, '/': 2, '//': 2, '%': 2,
            '**': 4,
        }

        def _to_infix_helper(curr: TreeNode) -> Tuple[str, int]:
            if curr.is_leaf():
                return curr.format_value(), 10

            if curr.is_unary:
                sub_str, sub_prec = _to_infix_helper(curr.right)
                # Unary minus has precedence 3
                if sub_prec < 3:
                    return f"{curr.value}({sub_str})", 3
                return f"{curr.value}{sub_str}", 3

            curr_prec = prec_map.get(curr.value, 0)
            left_str, left_prec = _to_infix_helper(curr.left)
            right_str, right_prec = _to_infix_helper(curr.right)

            # Left child needs parens if lower precedence
            if left_prec < curr_prec:
                left_str = f"({left_str})"

            # Right child needs parens if lower precedence or same precedence for non-associative ops
            if curr.value == '**':
                # Right associative: left needs parens if equal precedence
                if left_prec == curr_prec:
                    left_str = f"({left_str})"
            else:
                # Left associative: right needs parens if equal precedence in subtraction, division, modulo
                if right_prec < curr_prec or (right_prec == curr_prec and curr.value in ('-', '/', '//', '%')):
                    right_str = f"({right_str})"

            return f"{left_str} {curr.value} {right_str}", curr_prec

        res_str, _ = _to_infix_helper(node)
        return res_str


class TreeStatistics:
    """Calculates metadata and properties of the Expression Tree."""
    @staticmethod
    def get_stats(root: TreeNode) -> Dict[str, int]:
        total_nodes = 0
        operators = 0
        operands = 0

        def _count(node: Optional[TreeNode]) -> None:
            nonlocal total_nodes, operators, operands
            if node is None:
                return
            total_nodes += 1
            if node.is_leaf():
                operands += 1
            else:
                operators += 1
            _count(node.left)
            _count(node.right)

        def _height(node: Optional[TreeNode]) -> int:
            if node is None:
                return 0
            return 1 + max(_height(node.left), _height(node.right))

        _count(root)
        height = _height(root)

        return {
            "total_nodes": total_nodes,
            "height": height,
            "operator_count": operators,
            "operand_count": operands
        }


class TreeVisualizer:
    """
    Generates pure Python SVG and ASCII diagrams for the Expression Tree.
    Requires zero JavaScript charting libraries!
    """

    @classmethod
    def generate_svg(cls, root: TreeNode) -> str:
        """
        Calculates non-overlapping (x, y) coordinates for each node using an in-order
        and width-balanced tree layout, then renders a beautiful SVG diagram with
        gradient nodes, smooth curved connectors, drop shadows, and responsive viewBox.
        """
        # Step 1: Assign positions
        # We compute the horizontal spacing needed for each subtree.
        node_positions: Dict[int, Tuple[float, float]] = {}
        node_objects: Dict[int, TreeNode] = {}

        v_spacing = 95.0
        min_node_gap = 64.0

        def _calc_subtree_width(node: Optional[TreeNode]) -> float:
            if node is None:
                return 0.0
            if node.is_leaf():
                return min_node_gap
            if node.is_unary:
                return _calc_subtree_width(node.right) + 20.0
            left_w = _calc_subtree_width(node.left)
            right_w = _calc_subtree_width(node.right)
            return left_w + right_w

        def _layout(node: TreeNode, x_left: float, depth: int) -> float:
            node_objects[node.id] = node
            y = 55.0 + depth * v_spacing

            if node.is_leaf():
                x = x_left + min_node_gap / 2.0
                node_positions[node.id] = (x, y)
                return min_node_gap

            if node.is_unary:
                child_w = _layout(node.right, x_left, depth + 1)
                cx, _ = node_positions[node.right.id]
                node_positions[node.id] = (cx, y)
                return child_w

            left_w = _layout(node.left, x_left, depth + 1)
            right_w = _layout(node.right, x_left + left_w, depth + 1)

            lx, _ = node_positions[node.left.id]
            rx, _ = node_positions[node.right.id]
            node_positions[node.id] = ((lx + rx) / 2.0, y)

            return left_w + right_w

        total_width = max(_layout(root, 30.0, 0) + 60.0, 480.0)

        # Find max y for SVG height
        max_y = max(pos[1] for pos in node_positions.values()) + 65.0

        # Step 2: Build SVG elements
        lines_svg: List[str] = []
        nodes_svg: List[str] = []

        def _render_edges_and_nodes(node: TreeNode) -> None:
            px, py = node_positions[node.id]

            # Connectors to children
            children = []
            if node.left:
                children.append((node.left, "L"))
            if node.right:
                children.append((node.right, "R" if node.left else "U"))

            for child, side in children:
                cx, cy = node_positions[child.id]
                # Smooth cubic bezier curve connector
                mid_y = (py + cy) / 2.0
                lines_svg.append(
                    f'<path id="edge-{node.id}-{child.id}" '
                    f'd="M {px:.1f} {py + 22:.1f} C {px:.1f} {mid_y:.1f}, '
                    f'{cx:.1f} {mid_y:.1f}, {cx:.1f} {cy - 22:.1f}" '
                    f'class="tree-connector" '
                    f'data-parent="{node.id}" data-child="{child.id}" />'
                )
                _render_edges_and_nodes(child)

            # Node appearance
            is_op = not node.is_leaf()
            val_text = html.escape(node.format_value())

            if is_op:
                # Internal / Operator Node: Indigo styling
                nodes_svg.append(
                    f'<g id="node-{node.id}" class="tree-node operator-node" '
                    f'data-node-id="{node.id}" '
                    f'data-node-type="Operator" '
                    f'data-x="{px:.1f}" data-y="{py:.1f}" '
                    f'tabindex="0" role="button" aria-label="Operator {val_text}" '
                    f'transform="translate({px:.1f}, {py:.1f})">'
                    f'  <circle r="22" class="node-circle op-circle" />'
                    f'  <text dy=".35em" class="node-text op-text">{val_text}</text>'
                    f'</g>'
                )
            else:
                # Leaf / Operand Node: Emerald/Teal rounded box
                nodes_svg.append(
                    f'<g id="node-{node.id}" class="tree-node operand-node" '
                    f'data-node-id="{node.id}" '
                    f'data-node-type="Operand" '
                    f'data-x="{px:.1f}" data-y="{py:.1f}" '
                    f'tabindex="0" role="button" aria-label="Operand {val_text}" '
                    f'transform="translate({px:.1f}, {py:.1f})">'
                    f'  <rect x="-26" y="-19" width="52" height="38" rx="10" class="node-rect num-rect" />'
                    f'  <text dy=".35em" class="node-text num-text">{val_text}</text>'
                    f'</g>'
                )

        _render_edges_and_nodes(root)

        svg = f'''<svg viewBox="0 0 {total_width:.1f} {max_y:.1f}"
     width="100%" height="{max_y:.1f}"
     xmlns="http://www.w3.org/2000/svg"
     class="expression-tree-svg select-none">
  <defs>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.12" flood-color="#312e81"/>
    </filter>
  </defs>
  <g class="connectors-group">
    {"".join(lines_svg)}
  </g>
  <g class="nodes-group">
    {"".join(nodes_svg)}
  </g>
</svg>'''
        return svg

    @classmethod
    def generate_ascii(cls, root: TreeNode) -> str:
        """Produces a clean ASCII text representation of the Expression Tree."""
        lines: List[str] = []

        def _build(node: Optional[TreeNode], prefix: str = "", is_tail: bool = True):
            if node is None:
                return
            connector = "└── " if is_tail else "├── "
            val_display = f"[{node.format_value()}]" if not node.is_leaf() else str(node.format_value())
            if node.is_unary:
                val_display += " (unary)"
            lines.append(prefix + connector + val_display)

            children = []
            if node.left:
                children.append((node.left, "Left"))
            if node.right:
                children.append((node.right, "Right"))

            for i, (child, _) in enumerate(children):
                new_is_tail = (i == len(children) - 1)
                new_prefix = prefix + ("    " if is_tail else "│   ")
                _build(child, new_prefix, new_is_tail)

        lines.append(f"Root: [{root.format_value()}]")
        children = []
        if root.left:
            children.append((root.left, "Left"))
        if root.right:
            children.append((root.right, "Right"))

        for i, (child, _) in enumerate(children):
            _build(child, "", i == len(children) - 1)

        return "\n".join(lines)


def compute_interactive_metadata(root: TreeNode, node_values: Dict[int, Any]) -> Dict[str, Any]:
    """
    Computes exact calculation details, sub-expressions, operand roles,
    and connectivity metadata for every node in the expression tree.
    Provides data for the interactive Hover-to-Calculate effect and Calculation Inspector.
    """
    parent_map: Dict[int, TreeNode] = {}
    all_nodes: List[TreeNode] = []

    def _traverse(node: TreeNode):
        all_nodes.append(node)
        if node.left:
            parent_map[node.left.id] = node
            _traverse(node.left)
        if node.right:
            parent_map[node.right.id] = node
            _traverse(node.right)

    _traverse(root)

    def _format_val(val: Any) -> str:
        if isinstance(val, float):
            if val.is_integer() and not math.isinf(val):
                return str(int(val))
            return f"{val:.6g}"
        return str(val) if val is not None else ""

    op_names = {
        '+': 'Addition',
        '-': 'Subtraction',
        '*': 'Multiplication',
        '/': 'Division',
        '//': 'Floor Division',
        '%': 'Modulo',
        '**': 'Exponentiation'
    }

    metadata: Dict[str, Any] = {}

    for node in all_nodes:
        nid = str(node.id)
        parent = parent_map.get(node.id)
        parent_id = parent.id if parent else None
        is_root = (node.id == root.id)

        if node.is_leaf():
            val_str = node.format_value()
            used_in = Traversals.infix(parent) if parent else val_str
            parent_op = parent.format_value() if parent else None
            parent_op_name = op_names.get(parent_op, "parent operation") if parent_op else "root expression"

            metadata[nid] = {
                "id": node.id,
                "node_type": "Operand",
                "value": val_str,
                "is_unary": False,
                "is_root": is_root,
                "parent_id": parent_id,
                "child_ids": [],
                "edge_ids": [f"edge-{parent_id}-{node.id}"] if parent_id else [],
                "operation_name": "Numeric Operand",
                "left_operand": None,
                "right_operand": None,
                "calculation": f"Value = {val_str}",
                "computed_result": val_str,
                "status": "Operand constant",
                "used_in": used_in,
                "explanation": (
                    f"Constant numeric leaf operand {val_str} utilized in operation '{parent.format_value()}' ({used_in})."
                    if parent else f"Standalone numeric constant with value {val_str}."
                )
            }
        elif node.is_unary:
            computed_val = node_values.get(node.id)
            comp_str = _format_val(computed_val)
            child = node.right
            child_val = node_values.get(child.id)
            child_str = _format_val(child_val)
            child_expr = Traversals.infix(child)
            sub_expr = Traversals.infix(node)
            op_name = "Negation (Unary)" if node.value == '-' else "Unary Plus"

            metadata[nid] = {
                "id": node.id,
                "node_type": "Operator",
                "value": str(node.value),
                "is_unary": True,
                "is_root": is_root,
                "parent_id": parent_id,
                "child_ids": [child.id],
                "edge_ids": [f"edge-{node.id}-{child.id}"],
                "operation_name": op_name,
                "left_operand": None,
                "right_operand": f"{child_expr} = {child_str}" if not child.is_leaf() else child_str,
                "calculation": f"{node.value}({child_str}) = {comp_str}",
                "calculation_full": f"{sub_expr} = {comp_str}",
                "computed_result": comp_str,
                "status": "Calculated successfully",
                "used_in": Traversals.infix(parent) if parent else sub_expr,
                "explanation": (
                    f"Negates the operand value ({child_str}) to yield {comp_str}."
                    if node.value == '-' else f"Applies unary plus to child operand ({child_str})."
                )
            }
        else:
            computed_val = node_values.get(node.id)
            comp_str = _format_val(computed_val)
            left_child = node.left
            right_child = node.right
            left_val = node_values.get(left_child.id)
            right_val = node_values.get(right_child.id)
            left_str = _format_val(left_val)
            right_str = _format_val(right_val)
            left_expr = Traversals.infix(left_child)
            right_expr = Traversals.infix(right_child)
            sub_expr = Traversals.infix(node)
            op_name = op_names.get(node.value, "Binary Operation")

            calc_expr = f"{sub_expr} = {comp_str}"
            immediate_calc = f"{left_str} {node.value} {right_str} = {comp_str}"

            explanations = {
                '+': f"Calculates sum of left ({left_str}) and right ({right_str}) to produce {comp_str}.",
                '-': f"Subtracts right ({right_str}) from left ({left_str}) to produce {comp_str}.",
                '*': f"Multiplies left ({left_str}) by right ({right_str}) to produce {comp_str}.",
                '/': f"Divides left ({left_str}) by right ({right_str}) to produce {comp_str}.",
                '//': f"Calculates integer floor division of left ({left_str}) by right ({right_str}) to produce {comp_str}.",
                '%': f"Calculates modulo remainder of left ({left_str}) divided by right ({right_str}) to produce {comp_str}.",
                '**': f"Raises base ({left_str}) to power ({right_str}) to produce {comp_str}."
            }

            metadata[nid] = {
                "id": node.id,
                "node_type": "Operator",
                "value": str(node.value),
                "is_unary": False,
                "is_root": is_root,
                "parent_id": parent_id,
                "child_ids": [left_child.id, right_child.id],
                "edge_ids": [f"edge-{node.id}-{left_child.id}", f"edge-{node.id}-{right_child.id}"],
                "operation_name": op_name,
                "left_operand": f"{left_expr} = {left_str}" if not left_child.is_leaf() else left_str,
                "right_operand": f"{right_expr} = {right_str}" if not right_child.is_leaf() else right_str,
                "calculation": calc_expr,
                "immediate_calc": immediate_calc,
                "computed_result": comp_str,
                "status": "Calculated successfully",
                "used_in": Traversals.infix(parent) if parent else sub_expr,
                "explanation": explanations.get(node.value, f"Applies operator '{node.value}'.")
            }

    return metadata


def process_expression(expr_str: str) -> Dict[str, Any]:
    """
    Main entry point for processing a mathematical expression:
    1. Validates and tokenizes the input
    2. Constructs the Expression Tree
    3. Evaluates the expression with step-by-step trace and node values
    4. Calculates Traversals (Prefix, Infix, Postfix)
    5. Calculates Tree Statistics (height, node counts)
    6. Generates SVG and ASCII visual representations
    7. Computes interactive node metadata for Hover-to-Calculate inspector
    """
    if not expr_str or not expr_str.strip():
        raise ExpressionError("Expression is empty. Please enter an expression like (3 + 5) * 2 - 4 / 2.")

    # Reset node id counter for clean incremental SVG IDs
    TreeNode._counter = 0

    # Step 1: Tokenize
    tokenizer = Tokenizer(expr_str)
    tokens = tokenizer.tokenize()

    # Step 2: Parse & Build Tree
    parser = ExpressionParser(tokens)
    root = parser.parse()

    # Step 3: Evaluate safely & record steps and intermediate node values
    result, steps, node_values = Evaluator.evaluate(root, return_node_values=True)

    # Step 4: Traversals
    prefix_tokens = Traversals.prefix(root)
    postfix_tokens = Traversals.postfix(root)
    infix_str = Traversals.infix(root)

    # Step 5: Tree Statistics
    stats = TreeStatistics.get_stats(root)

    # Step 6: Visualizations & Calculation Metadata
    svg_tree = TreeVisualizer.generate_svg(root)
    ascii_tree = TreeVisualizer.generate_ascii(root)
    tree_metadata = compute_interactive_metadata(root, node_values)

    # Format result for display
    if isinstance(result, float) and result.is_integer() and not math.isinf(result):
        display_result = str(int(result))
    elif isinstance(result, float):
        display_result = f"{result:.8g}"
    else:
        display_result = str(result)

    return {
        "original_expression": expr_str.strip(),
        "evaluated_result": display_result,
        "raw_result": result,
        "prefix_traversal": " ".join(prefix_tokens),
        "infix_traversal": infix_str,
        "postfix_traversal": " ".join(postfix_tokens),
        "steps": steps,
        "statistics": stats,
        "svg_tree": svg_tree,
        "ascii_tree": ascii_tree,
        "tree_metadata": tree_metadata,
    }
