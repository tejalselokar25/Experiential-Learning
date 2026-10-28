"""
app.py - Flask Application for Expression Tree Generator and Evaluator
-----------------------------------------------------------------------
Handles web routes, form submissions, query parameter preloads, input validation,
and renders the Expression Tree interface using server-side templates.
"""

import os

from flask import Flask, render_template, request
from expression_tree import process_expression, ExpressionError

app = Flask(__name__)


def start_server():
    """Start the Flask development server using environment-configurable host and port."""
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', '5000'))
    debug = os.environ.get('DEBUG', 'False').lower() in {'1', 'true', 'yes', 'on'}

    print("===============================================================")
    print(" Starting Expression Tree Generator & Evaluator Server...")
    print(f" Access the application at: http://{host}:{port}")
    print("===============================================================")
    app.run(host=host, port=port, debug=debug)


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Main route supporting both GET and POST requests.
    - GET: Displays the input form. If an 'expr' query parameter is present (e.g. from
      quick-example links), it immediately parses and renders the tree.
    - POST: Receives form submission, validates and processes the mathematical expression,
      and renders the expression tree, traversals, and evaluation trace.
    """
    expression = ""
    error = None
    result = None

    if request.method == 'POST':
        expression = request.form.get('expression', '').strip()
        if not expression:
            error = "Expression is empty. Please enter a valid mathematical expression."
        else:
            try:
                result = process_expression(expression)
            except ExpressionError as e:
                error = str(e)
            except Exception as e:
                # Catch unexpected server errors gracefully without exposing stack traces
                error = f"An unexpected processing error occurred: {str(e)}"

    elif request.method == 'GET':
        # Check if expression passed via query parameter (e.g., from quick-load example links)
        param_expr = request.args.get('expr', '').strip()
        if param_expr:
            expression = param_expr
            try:
                result = process_expression(expression)
            except ExpressionError as e:
                error = str(e)
            except Exception as e:
                error = f"An unexpected processing error occurred: {str(e)}"
        else:
            # Default initial demonstration expression to wow the user on first load
            expression = "(3 + 5) * 2 - 4 / 2"
            try:
                result = process_expression(expression)
            except Exception:
                pass

    return render_template(
        'index.html',
        expression=expression,
        error=error,
        result=result
    )


if __name__ == '__main__':
    start_server()
