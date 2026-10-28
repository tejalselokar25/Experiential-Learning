"""
test_engine.py - Verification script for expression_tree engine
"""
import sys
from expression_tree import process_expression, ExpressionError

def run_tests():
    test_cases = [
        ("3 + 5", "8"),
        ("(3 + 5) * 2", "16"),
        ("10 - 2 * 3", "4"),
        ("20 / 4 + 3", "8"),
        ("2 ** 3 ** 2", "512"),
        ("17 % 5", "2"),
        ("17 // 5", "3"),
        ("-5 + 3", "-2"),
        ("4 * -2", "-8"),
        ("-(3 + 5) * 2", "-16"),
        ("3.5 + 2.5", "6"),
        ("(3 + 5) * 2 - 4 / 2", "14")
    ]

    print("=== RUNNING TEST SUITE ===")
    all_passed = True
    for expr, expected in test_cases:
        try:
            res = process_expression(expr)
            passed = str(res["evaluated_result"]) == expected
            status = "PASS" if passed else "FAIL"
            print(f"[{status}] {expr:24} = {res['evaluated_result']} (expected: {expected})")
            print(f"       Prefix:  {res['prefix_traversal']}")
            print(f"       Infix:   {res['infix_traversal']}")
            print(f"       Postfix: {res['postfix_traversal']}")
            print(f"       Steps:   {res['steps']}")
            print(f"       Stats:   {res['statistics']}")
            if not passed:
                all_passed = False
        except Exception as e:
            print(f"[ERROR] {expr}: {e}")
            all_passed = False

    # Verify interactive hover calculation metadata
    print("\n--- Testing Hover Calculation Metadata ---")
    try:
        sample_res = process_expression("(3 + 5) * 2")
        meta = sample_res.get("tree_metadata", {})
        assert meta, "tree_metadata is empty"

        # Verify operator nodes
        plus_nodes = [n for n in meta.values() if n["value"] == "+"]
        assert len(plus_nodes) == 1, "Expected 1 '+' node"
        plus = plus_nodes[0]
        assert plus["operation_name"] == "Addition"
        assert plus["calculation"] == "3 + 5 = 8"
        assert plus["status"] == "Calculated successfully"
        assert len(plus["child_ids"]) == 2
        assert len(plus["edge_ids"]) == 2
        print(f"[PASS] '+' node calculation metadata: {plus['calculation']} (Status: {plus['status']})")

        mul_nodes = [n for n in meta.values() if n["value"] == "*"]
        assert len(mul_nodes) == 1, "Expected 1 '*' node"
        mul = mul_nodes[0]
        assert mul["operation_name"] == "Multiplication"
        assert mul["calculation"] == "(3 + 5) * 2 = 16"
        assert mul["is_root"] is True
        assert mul["computed_result"] == "16"
        print(f"[PASS] '*' root calculation metadata: {mul['calculation']} (Root Result: {mul['computed_result']})")

        # Verify operand node
        five_nodes = [n for n in meta.values() if n["value"] == "5"]
        assert len(five_nodes) == 1, "Expected 1 '5' node"
        five = five_nodes[0]
        assert five["node_type"] == "Operand"
        assert five["used_in"] == "3 + 5"
        print(f"[PASS] '5' operand metadata: Value {five['value']}, Used in '{five['used_in']}'")

    except Exception as e:
        print(f"[FAIL] Hover metadata verification failed: {e}")
        all_passed = False

    # Check division by zero
    print("\n--- Testing Division by Zero ---")
    try:
        process_expression("10 / 0")
        print("[FAIL] 10 / 0 did not raise ExpressionError")
        all_passed = False
    except ExpressionError as e:
        print(f"[PASS] 10 / 0 correctly caught: {e}")

    # Check malformed expressions
    error_cases = [
        ("", "Empty"),
        ("3 +", "Trailing operator"),
        ("3 + * 5", "Consecutive operators"),
        ("(3 + 5", "Unmatched ("),
        ("3 + 5)", "Unmatched )"),
        ("3 @ 5", "Invalid character"),
        ("3.5.2 + 1", "Invalid float")
    ]

    print("\n--- Testing Error Cases ---")
    for err_expr, desc in error_cases:
        try:
            process_expression(err_expr)
            print(f"[FAIL] {desc} ('{err_expr}') did not raise error")
            all_passed = False
        except ExpressionError as e:
            print(f"[PASS] {desc:24} -> caught: {e}")

    if all_passed:
        print("\n>>> ALL TESTS PASSED! <<<")
    else:
        print("\n>>> SOME TESTS FAILED! <<<")
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
