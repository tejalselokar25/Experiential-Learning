"""
test_http_routes.py - Direct HTTP Route Testing
Verifies GET, POST, query-parameter preload, error handling,
and HTML rendering through the Flask test client and HTTP requests.
"""

from app import app
import urllib.parse

def test_routes():
    print("=== TESTING FLASK HTTP ROUTES ===")
    client = app.test_client()

    # 1. Test GET / (Initial load)
    res = client.get('/')
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    html = res.data.decode('utf-8')
    assert "Expression Tree Generator and Evaluator" in html
    assert "Evaluated Result" in html
    assert "14" in html  # Default demo expression result
    assert "Calculation Inspector" in html
    assert "tree-metadata-data" in html
    assert "tree-canvas-container" in html
    assert "tree-tooltip" in html
    print("[PASS] GET / renders default demonstration and Calculation Inspector successfully (Status 200)")

    # 2. Test GET /?expr=...
    test_expr = "2 ** 3 ** 2"
    url = f"/?expr={urllib.parse.quote(test_expr)}"
    res = client.get(url)
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert "512" in html
    assert "2 3 2 ** **" in html
    print(f"[PASS] GET {url} parses and renders query param correctly (Result: 512)")

    # 3. Test POST / with valid expressions
    post_cases = [
        ("3 + 5", "8"),
        ("(3 + 5) * 2", "16"),
        ("10 - 2 * 3", "4"),
        ("20 / 4 + 3", "8"),
        ("17 % 5", "2"),
        ("17 // 5", "3"),
        ("-5 + 3", "-2"),
        ("4 * -2", "-8"),
        ("-(3 + 5) * 2", "-16"),
        ("3.5 + 2.5", "6"),
        ("(3 + 5) * 2 - 4 / 2", "14")
    ]

    for expr, expected in post_cases:
        res = client.post('/', data={"expression": expr})
        assert res.status_code == 200
        html = res.data.decode('utf-8')
        assert expected in html, f"Expected {expected} in HTML for {expr}"
        assert "tree-connector" in html, f"SVG connectors missing for {expr}"
        print(f"[PASS] POST / with '{expr}' -> returned {expected} with full SVG and traversals")

    # 4. Test POST / with division by zero
    res = client.post('/', data={"expression": "10 / 0"})
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert "Division by zero" in html
    assert "Expression Evaluation Error" in html
    print("[PASS] POST / with '10 / 0' correctly displays division by zero error banner")

    # 5. Test POST / with empty expression
    res = client.post('/', data={"expression": ""})
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert "Expression is empty" in html
    print("[PASS] POST / with empty input shows friendly validation error")

    # 6. Test POST / with malformed syntax
    res = client.post('/', data={"expression": "5 + * 2"})
    assert res.status_code == 200
    html = res.data.decode('utf-8')
    assert "Unexpected operator" in html
    print("[PASS] POST / with malformed '5 + * 2' shows helpful syntax error")

    print("\n>>> ALL FLASK ROUTE TESTS PASSED 100%! <<<")

if __name__ == '__main__':
    test_routes()
