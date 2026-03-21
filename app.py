from flask import Flask, request, jsonify
from flask_cors import CORS
import math
import re

app = Flask(__name__)
CORS(app)

# ---------------- CALCULATE FUNCTION ----------------

def calculate_expression(expr):

    try:

        expr = expr.lower()

        # basic math words
        expr = expr.replace("plus", "+")
        expr = expr.replace("add", "+")
        expr = expr.replace("minus", "-")
        expr = expr.replace("subtract", "-")
        expr = expr.replace("times", "*")
        expr = expr.replace("multiply", "*")
        expr = expr.replace("divide", "/")
        expr = expr.replace("power", "**")

        # scientific conversions
        expr = re.sub(r"log (\d+)", r"math.log10(\1)", expr)
        expr = re.sub(r"sqrt (\d+)", r"math.sqrt(\1)", expr)
        expr = re.sub(r"square root (\d+)", r"math.sqrt(\1)", expr)

        expr = re.sub(r"sin (\d+)", r"math.sin(math.radians(\1))", expr)
        expr = re.sub(r"cos (\d+)", r"math.cos(math.radians(\1))", expr)
        expr = re.sub(r"tan (\d+)", r"math.tan(math.radians(\1))", expr)

        expr = re.sub(r"factorial (\d+)", r"math.factorial(\1)", expr)

        print("Converted Expression:", expr)

        result = eval(expr, {"math": math})

        return result

    except Exception as e:

        print("ERROR:", e)

        return "Invalid Expression"


# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return "Voice Scientific Calculator Backend Running"


@app.route("/calculate", methods=["POST"])
def calculate():

    data = request.json
    text = data.get("text")

    print("Received:", text)

    result = calculate_expression(text)

    return jsonify({
        "result": result
    })


# ---------------- START SERVER ----------------

if __name__ == "__main__":
    app.run(debug=True)``