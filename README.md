# Experiential Learning - Expression Tree Generator and Evaluator

A comprehensive computer science project that builds, visualizes, and evaluates mathematical **Binary Expression Trees** from infix arithmetic expressions.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/tejalselokar25/Experiential-Learning)

All project source files, tests, and documentation are organized inside the [**Experiential Learning**](./Experiential%20Learning/) folder.

---

## ?? Repository Structure

`	ext
Experiential-Learning/
+-- Experiential Learning/        # Main project folder
¦   +-- app.py                   # Flask web application and HTTP routes
¦   +-- expression_tree.py       # Core pure-Python expression parsing & AST engine
¦   +-- test_engine.py           # Automated test suite for expression tree engine
¦   +-- test_http_routes.py      # HTTP route integration test suite
¦   +-- requirements.txt         # Python dependencies (Flask, gunicorn)
¦   +-- render.yaml              # Render web service configuration
¦   +-- README.md                # Full documentation, concepts, and viva guide
¦   +-- static/
¦   ¦   +-- style.css            # Stylesheet for UI and SVG expression trees
¦   +-- templates/
¦       +-- index.html           # Interactive HTML5 + Tailwind CSS web interface
+-- render.yaml                  # Root Render blueprint (points to Experiential Learning)
+-- README.md                    # Project overview & navigation guide
`

---

## ?? Quick Start

To run the application locally:

`ash
# 1. Navigate to the project directory
cd "Experiential Learning"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the Flask server
python app.py
`

Then open http://127.0.0.1:5000 in your web browser.

---

## ?? Running Tests

To run all automated test suites:

`ash
python -m pytest "Experiential Learning"
`

For detailed theoretical concepts (ASTs, operator precedence, traversals, bottom-up post-order evaluation) and viva questions, please refer to [**Experiential Learning/README.md**](./Experiential%20Learning/README.md).
