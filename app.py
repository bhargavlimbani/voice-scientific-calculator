from flask import Flask, request, jsonify
from flask_cors import CORS
import math
import re

app = Flask(__name__)
CORS(app)

# ---------------- NUMBER WORDS ----------------

number_words = {
    "zero":0,"one":1,"two":2,"three":3,"four":4,
    "five":5,"six":6,"seven":7,"eight":8,"nine":9,
    "ten":10,"eleven":11,"twelve":12,"thirteen":13,
    "fourteen":14,"fifteen":15,"sixteen":16,
    "seventeen":17,"eighteen":18,"nineteen":19,
    "twenty":20,"thirty":30,"forty":40,
    "fifty":50,"sixty":60,"seventy":70,
    "eighty":80,"ninety":90
}

def convert_number_words(text):
    for word, num in number_words.items():
        text = text.replace(word, str(num))
    return text


# ---------------- CLEAN INPUT ----------------

def clean_text(text):

    text = text.lower()

    # remove unnecessary words
    remove_words = [
        "calculate", "what is", "find", "of", "the", "please"
    ]

    for w in remove_words:
        text = text.replace(w, "")

    return text.strip()


# ---------------- PROCESS EXPRESSION ----------------

def process_expression(expr):

    expr = clean_text(expr)
    expr = convert_number_words(expr)

    # ---------------- SMART NLP (NEW AI LOGIC) ----------------

    # add five and ten → 5 + 10
    expr = re.sub(r"add (\d+) and (\d+)", r"\1 + \2", expr)

    # subtract 5 from 10 → 10 - 5
    expr = re.sub(r"subtract (\d+) from (\d+)", r"\2 - \1", expr)

    # multiply 5 and 3 → 5 * 3
    expr = re.sub(r"multiply (\d+) and (\d+)", r"\1 * \2", expr)

    # divide 10 by 2 → 10 / 2
    expr = re.sub(r"divide (\d+) by (\d+)", r"\1 / \2", expr)

    # ---------------- BASIC OPERATORS ----------------

    expr = expr.replace("plus", "+")
    expr = expr.replace("add", "+")
    expr = expr.replace("minus", "-")
    expr = expr.replace("subtract", "-")

    expr = expr.replace("multiplied by", "*")
    expr = expr.replace("multiply", "*")
    expr = expr.replace("times", "*")
    expr = expr.replace("into", "*")
    expr = expr.replace("x", "*")

    expr = expr.replace("divided by", "/")
    expr = expr.replace("divide", "/")
    expr = expr.replace("over", "/")

    # ---------------- CONSTANTS ----------------

    expr = expr.replace("pi", str(math.pi))
    expr = expr.replace("e", str(math.e))

    # ---------------- SCIENTIFIC ----------------

    expr = re.sub(r"sin (\d+)", r"math.sin(math.radians(\1))", expr)
    expr = re.sub(r"sine (\d+)", r"math.sin(math.radians(\1))", expr)

    expr = re.sub(r"cos (\d+)", r"math.cos(math.radians(\1))", expr)
    expr = re.sub(r"cosine (\d+)", r"math.cos(math.radians(\1))", expr)

    expr = re.sub(r"tan (\d+)", r"math.tan(math.radians(\1))", expr)

    expr = re.sub(r"log (\d+)", r"math.log10(\1)", expr)
    expr = re.sub(r"ln (\d+)", r"math.log(\1)", expr)

    expr = re.sub(r"sqrt (\d+)", r"math.sqrt(\1)", expr)
    expr = re.sub(r"square root (\d+)", r"math.sqrt(\1)", expr)

    expr = re.sub(r"(\d+) factorial", r"math.factorial(\1)", expr)

    # ---------------- POWER ----------------

    expr = re.sub(r"(\d+)\s*power\s*(\d+)", r"(\1**\2)", expr)

    expr = re.sub(r"(\d+) square (\d+)", r"(\1**\2)", expr)
    expr = re.sub(r"square (\d+)", r"(\1**2)", expr)
    expr = re.sub(r"cube (\d+)", r"(\1**3)", expr)

    return expr


# ---------------- CALCULATE ----------------

def calculate_expression(expr):

    try:
        expr = expr.lower()

        # remove extra words
        expr = expr.replace("calculate", "")
        expr = expr.replace("what is", "")
        expr = expr.replace("find", "")
        expr = expr.replace("of", "")

        # power fix (IMPORTANT)
        expr = re.sub(r"(\d+)\s*power\s*(\d+)", r"(\1**\2)", expr)
        expr = process_expression(expr)

        print("Converted Expression:", expr)

        result = eval(expr, {"math": math})

        return result

    except Exception as e:
        print("ERROR:", e)
        return "Invalid Expression"

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return "AI Voice Scientific Calculator Running"


@app.route("/calculate", methods=["POST"])
def calculate():

    data = request.json
    text = data.get("text")

    print("Received:", text)

    result = calculate_expression(text)

    return jsonify({
        "result": result
    })


# ---------------- RUN SERVER ----------------

if __name__ == "__main__":
    app.run(debug=True)