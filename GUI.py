import base64
import sympy
from io import BytesIO

from flask import Flask, request, render_template, session
from matplotlib.figure import Figure

GUI = Flask(__name__)
def solve_equation(equation):
    expression = sympy.sympify(equation)
    evaluated_expression = expression.evalf()
    return str(evaluated_expression)

def retrieve_equation():
    unsolved_equation = request.form.get("equation", "")
    return unsolved_equation
@GUI.route("/", methods=["GET", "POST"])

def return_equation():
    solved_equation = ""
    if request.method == "POST":
        unsolved_equation = retrieve_equation()
        if unsolved_equation != "":
            solved_equation = solve_equation(unsolved_equation)

    return render_template("flask_test.html", solved_equation=solved_equation)



def hello():
    # Create the graph
    fig = Figure()
    ax = fig.subplots()

    ax.plot([1, 2])
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    # Convert the graph into a PNG image
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")

    # Encode the image so it can be embedded in HTML
    data = base64.b64encode(buf.getvalue()).decode("ascii")
    # Graph image url to use in HTML file
    plot_url = f"data:image/png;base64,{data}"

    # Send the graph to the HTML page
    return render_template("flask_test.html", plot_url=plot_url)


if __name__ == "__main__":
    GUI.run(debug=True)

