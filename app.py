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

    remove_words = [
        "calculate", "what is", "find", "please",
        "the", "value"
    ]

    for w in remove_words:
        text = text.replace(w, "")

    return text.strip()


# ---------------- AI NORMALIZER ----------------

def normalize_sentence(expr):

    expr = expr.lower()

    # ---------------- REMOVE AI WORDS ----------------
    remove_words = [
        "what is", "calculate", "find", "please",
        "give me", "result of", "answer of"
    ]

    for w in remove_words:
        expr = expr.replace(w, "")

    # ---------------- OPERATORS ----------------
    expr = expr.replace("plus", "+")
    expr = expr.replace("minus", "-")
    expr = expr.replace("times", "*")
    expr = expr.replace("multiplied by", "*")
    expr = expr.replace("into", "*")
    expr = expr.replace("divided by", "/")
    expr = expr.replace("over", "/")

    # ---------------- BRACKETS ----------------
    expr = expr.replace("open bracket", "(")
    expr = expr.replace("close bracket", ")")

    # ---------------- POWER NLP ----------------
    expr = expr.replace("to the power of", " power ")
    expr = expr.replace("raised to", " power ")

    # ---------------- FUNCTION NLP ----------------
    expr = expr.replace("sin of", "sin ")
    expr = expr.replace("cos of", "cos ")
    expr = expr.replace("tan of", "tan ")

    expr = expr.replace("log of", "log ")
    expr = expr.replace("ln of", "ln ")

    expr = expr.replace("square root of", "sqrt ")

    # ---------------- PERMUTATION / COMBINATION NLP ----------------
    expr = expr.replace("permutation of", " p ")
    expr = expr.replace("combination of", " c ")

    # ---------------- PERCENT NLP ----------------
    expr = expr.replace("percent of", "% of")
    expr = expr.replace("percent", "%")

    return expr.strip()

def conversational_parser(expr):

    expr = expr.lower()

    # remove filler words
    fillers = ["then", "first", "next", "after that", "and then", "please"]
    for f in fillers:
        expr = expr.replace(f, "")

    tokens = expr.split()

    result_expr = ""
    current_number = None

    i = 0
    while i < len(tokens):

        word = tokens[i]

        # number detection
        if word.isdigit():
            current_number = word
            result_expr += word

        # ADD
        elif word in ["add", "plus"]:
            if i+1 < len(tokens):
                result_expr += "+" + tokens[i+1]
                i += 1

        # SUBTRACT
        elif word in ["subtract", "minus"]:
            if i+1 < len(tokens):
                result_expr += "-" + tokens[i+1]
                i += 1

        # MULTIPLY
        elif word in ["multiply", "times"]:
            if i+1 < len(tokens):
                result_expr += "*" + tokens[i+1]
                i += 1

        # DIVIDE
        elif word in ["divide"]:
            if i+1 < len(tokens):
                result_expr += "/" + tokens[i+1]
                i += 1

        # SQUARE
        elif word == "square":
            result_expr = f"({result_expr})**2"

        # CUBE
        elif word == "cube":
            result_expr = f"({result_expr})**3"

        # PERCENT
        elif word == "percent":
            result_expr = f"({result_expr}/100)"

        i += 1

    return result_expr

def ai_brain_parser(expr):

    expr = expr.lower()

    # remove filler words
    fillers = [
        "what is", "calculate", "find", "please",
        "if i", "i", "take", "value", "the"
    ]

    for f in fillers:
        expr = expr.replace(f, "")

    # ---------------- LOGIC HANDLING ----------------

    # sum of a and b → (a+b)
    expr = re.sub(r"sum of (\d+) and (\d+)", r"(\1+\2)", expr)

    # difference of a and b → (a-b)
    expr = re.sub(r"difference of (\d+) and (\d+)", r"(\1-\2)", expr)

    # product of a and b → (a*b)
    expr = re.sub(r"product of (\d+) and (\d+)", r"(\1*\2)", expr)

    # square of (...) → (...)**2
    expr = re.sub(r"square of (.+)", r"(\1)**2", expr)

    # cube of (...) → (...)**3
    expr = re.sub(r"cube of (.+)", r"(\1)**3", expr)

    # increase by % → +%
    expr = re.sub(r"increase (\d+) by (\d+)%", r"\1 + \2%", expr)

    # decrease by % → -%
    expr = re.sub(r"decrease (\d+) by (\d+)%", r"\1 - \2%", expr)

    return expr


# ---------------- PROCESS EXPRESSION ----------------
def process_expression(expr):
    

    expr = normalize_sentence(expr)
    if any(word in expr for word in ["then", "first", "next"]):
        expr = conversational_parser(expr)
        
    if any(word in expr for word in ["sum", "product", "difference", "increase", "decrease"]):
        expr = ai_brain_parser(expr)

    expr = clean_text(expr)
    expr = convert_number_words(expr)

    expr = expr.replace("of", "")
    expr = re.sub(r"\b(and)\b", "+", expr)

    # ---------------- ROOT ----------------
    expr = re.sub(r"square\s*root\s*(\d+(?:\.\d+)?)", r"math.sqrt(\1)", expr)
    expr = re.sub(r"sqrt\s*(\d+(?:\.\d+)?)", r"math.sqrt(\1)", expr)

    # ---------------- AI PHRASES ----------------
    expr = re.sub(r"square of (\d+(?:\.\d+)?)", r"(\1**2)", expr)
    expr = re.sub(r"cube of (\d+(?:\.\d+)?)", r"(\1**3)", expr)
    expr = re.sub(r"log of (\d+(?:\.\d+)?)", r"math.log10(\1)", expr)

    expr = re.sub(r"(\d+)\s*times\s*(\d+)", r"\1*\2", expr)
    expr = re.sub(r"(\d+)\s*plus\s*(\d+)", r"\1+\2", expr)

    # ---------------- SMART NLP ----------------
    expr = re.sub(r"add (\d+(?:\.\d+)?) and (\d+(?:\.\d+)?)", r"\1 + \2", expr)
    expr = re.sub(r"subtract (\d+(?:\.\d+)?) from (\d+(?:\.\d+)?)", r"\2 - \1", expr)
    expr = re.sub(r"multiply (\d+(?:\.\d+)?) and (\d+(?:\.\d+)?)", r"\1 * \2", expr)
    expr = re.sub(r"divide (\d+(?:\.\d+)?) by (\d+(?:\.\d+)?)", r"\1 / \2", expr)

    # ---------------- TRIG ----------------
    expr = re.sub(r"\b(sin|sine)\s*(-?\d+(?:\.\d+)?)", r"math.sin(math.radians(\2))", expr)
    expr = re.sub(r"\b(cos|cosine)\s*(-?\d+(?:\.\d+)?)", r"math.cos(math.radians(\2))", expr)
    expr = re.sub(r"\b(tan|tangent)\s*(-?\d+(?:\.\d+)?)", r"math.tan(math.radians(\2))", expr)

    # ---------------- INVERSE TRIG ----------------
    expr = re.sub(r"asin\s*(\d+(?:\.\d+)?)", r"math.degrees(math.asin(\1))", expr)
    expr = re.sub(r"acos\s*(\d+(?:\.\d+)?)", r"math.degrees(math.acos(\1))", expr)
    expr = re.sub(r"atan\s*(\d+(?:\.\d+)?)", r"math.degrees(math.atan(\1))", expr)

    # ---------------- LOG ----------------
    expr = re.sub(r"\blog\s*(\d+(?:\.\d+)?)", r"math.log10(\1)", expr)
    expr = re.sub(r"\bln\s*(\d+(?:\.\d+)?)", r"math.log(\1)", expr)

    # ---------------- EXP ----------------
    expr = re.sub(r"e\s*power\s*(\d+(?:\.\d+)?)", r"math.exp(\1)", expr)
    expr = re.sub(r"exp\s*(\d+(?:\.\d+)?)", r"math.exp(\1)", expr)

    # ---------------- FACTORIAL ----------------
    expr = re.sub(r"(\d+)\s*factorial", r"math.factorial(\1)", expr)    

    # ---------------- POWER ----------------
    expr = re.sub(r"(\d+(?:\.\d+)?)\s*power\s*(\d+(?:\.\d+)?)", r"(\1**\2)", expr)
    expr = re.sub(r"(\d+(?:\.\d+)?)\s*to the power of\s*(\d+(?:\.\d+)?)", r"(\1**\2)", expr)

    expr = re.sub(r"\bsquare\s*(\d+(?:\.\d+)?)", r"(\1**2)", expr)
    expr = re.sub(r"(\d+(?:\.\d+)?)\s*square\b", r"(\1**2)", expr)

    expr = re.sub(r"\bcube\s*(\d+(?:\.\d+)?)", r"(\1**3)", expr)
    expr = re.sub(r"(\d+(?:\.\d+)?)\s*cube\b", r"(\1**3)", expr)

    # ---------------- MODULUS ----------------
    expr = re.sub(r"(\d+(?:\.\d+)?)\s*(mod|modulus)\s*(\d+(?:\.\d+)?)", r"(\1%\3)", expr)
    expr = re.sub(r"(\d+(?:\.\d+)?)\s*%\s*(\d+(?:\.\d+)?)", r"(\1%\2)", expr)

    # ---------------- PERCENTAGE ----------------
    # 1. x% of y  → (x/100) * y
    expr = re.sub(r"(\d+(?:\.\d+)?)\s*%\s*of\s*(\d+(?:\.\d+)?)",r"((\1/100)*\2)",expr)

    # 2. a + b%  → a + (a*b/100)
    expr = re.sub(r"(\d+(?:\.\d+)?)\s*\+\s*(\d+(?:\.\d+)?)%",r"(\1 + (\1*\2/100))",expr)

    # 3. a - b%  → a - (a*b/100)
    expr = re.sub(r"(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)%",r"(\1 - (\1*\2/100))",expr)

    # 4. a * b%  → a * (b/100)
    expr = re.sub(r"(\d+(?:\.\d+)?)\s*\*\s*(\d+(?:\.\d+)?)%",r"(\1 * (\2/100))",expr)    
    # 5. a / b%  → a / (b/100)
    expr = re.sub(r"(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)%",r"(\1 / (\2/100))",expr)

    # 6. standalone → b% = b/100
    expr = re.sub(r"(\d+(?:\.\d+)?)%",r"(\1/100)",expr)
    expr = expr.replace("%", "/100")  # catch any remaining %


    # ---------------- ABS ----------------
    expr = re.sub(r"absolute\s*(-?\d+(?:\.\d+)?)", r"abs(\1)", expr)
    expr = re.sub(r"abs\s*(-?\d+(?:\.\d+)?)", r"abs(\1)", expr)

    # ---------------- CONSTANT MULTIPLY ----------------
    expr = re.sub(r"(\d+)\s*pi", r"(\1*math.pi)", expr)
    expr = re.sub(r"(\d+)\s*e", r"(\1*math.e)", expr)

    # ---------------- IMPLICIT MULTIPLICATION ----------------
    expr = re.sub(r"(\d)\(", r"\1*(", expr)           
    expr = re.sub(r"\)(\d)", r")*\1", expr)           
    expr = re.sub(r"\)\(", r")*(", expr)              

    # function multiply: 2sin30 → 2*sin30
    expr = re.sub(r"(\d)(math\.)", r"\1*\2", expr)

    # ---------------- OPERATORS ----------------
    expr = expr.replace(" x ", " * ")
    expr = expr.replace("over", "/")

    # ---------------- CONSTANTS ----------------
    expr = expr.replace("pi", str(math.pi))
    expr = expr.replace("e", str(math.e))
    
    # ---------------- PERMUTATION & COMBINATION ----------------

    # nPr → permutation
    expr = re.sub(r"(\d+)\s*p\s*(\d+)",r"(math.factorial(\1)//math.factorial(\1-\2))",expr)

    expr = re.sub(
        r"(\d+)\s*permutation\s*(\d+)",r"(math.factorial(\1)//math.factorial(\1-\2))",expr)

    # nCr → combination
    expr = re.sub(r"(\d+)\s*c\s*(\d+)",r"(math.factorial(\1)//(math.factorial(\2)*math.factorial(\1-\2)))",expr)

    expr = re.sub(r"(\d+)\s*combination\s*(\d+)",r"(math.factorial(\1)//(math.factorial(\2)*math.factorial(\1-\2)))",expr)

    # clean spaces
    expr = re.sub(r"\s+", " ", expr)

    return expr

# ---------------- CALCULATE ----------------

def calculate_expression(expr):

    try:
        expr = expr.lower()

        expr = process_expression(expr)

        print("Converted Expression:", expr)

        result = eval(expr, {"__builtins__": None}, {"math": math, "abs": abs})

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