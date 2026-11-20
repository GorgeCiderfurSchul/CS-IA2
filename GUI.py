import sympy
import matplotlib.pyplot as plt
import numpy as np
import sys
import io
import base64
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application, convert_xor, parse_expr
print("Python interpreter:", sys.executable)
print("SymPy version:", sympy.__version__)

from flask import Flask, request, render_template, session, jsonify
from matplotlib.figure import Figure

trig_functions_degrees = {
    "sin": lambda x: sympy.sin(x * sympy.pi / 180),
    "cos": lambda x: sympy.cos(x * sympy.pi / 180),
    "tan": lambda x: sympy.tan(x * sympy.pi / 180),
    "ctan": lambda x: sympy.cot(x * sympy.pi / 180)
}

trig_functions = {
    "sin": sympy.sin,
    "cos": sympy.cos,
    "tan": sympy.tan,
    "ctan": sympy.cot
                }
transformations = (standard_transformations + (implicit_multiplication_application,) + (convert_xor,))


def solve_expression(unsolved_expression):
    angle_unit = session.get("angle_unit", "radians")
    try:
        if angle_unit == "degrees":
            expression = parse_expr(unsolved_expression, local_dict=trig_functions_degrees, transformations=transformations)
        else:
            expression = parse_expr(unsolved_expression, local_dict=trig_functions, transformations=transformations)

        return str(expression.evalf())

    except (SyntaxError, NameError) as error:
        print(error)


def retrieve_expression():
    unsolved_expression = request.form.get("expression", "")
    return unsolved_expression


def retrieve_graph():
    graph_equation = request.form.get("graph_equation", "")
    try:
        graph_equation = parse_expr(graph_equation, transformations=transformations)
    except (SyntaxError, NameError, TypeError) as error:
        print(error)
    x_label = request.form.get("x_label_input") or "X"
    y_label = request.form.get("y_label_input") or "Y"
    x_range = request.form.get("x_range_input") or "-10.0, 10.0"
    step = request.form.get("x_step_input") or "0.1"
    color = request.form.get("color_select)") or "Blue"
    return graph_equation, x_label, y_label, x_range, step, color


def retrieve_equation():
    unsolved_equation = request.form.get("input_equation_solver", "")
    try:
        transformed_equation = parse_expr(unsolved_equation, transformations=transformations)
    except (SyntaxError, NameError) as error:
        print(error)
    arguments = request.form.get("arg_input", "")
    return transformed_equation, arguments


def solve_equation(unsolved_equation, args):
    # clean_args = args.replace(",", "")
    sympy_args = sympy.symbols(args)
    solved_equation = sympy.solve(sympy.sympify(unsolved_equation), sympy_args)
    # testing block
    print(args)
    print(sympy_args)
    print(solved_equation)
    print(str(solved_equation))
    return str(solved_equation)


GUI = Flask(__name__)
GUI.secret_key = "Calc-short-for-calculator"


@GUI.route("/", methods=["GET", "POST"])
def return_equation():
    solved_expression = ""
    angle_unit = session.get("angle_unit", "radians")
    plot_url = ""
    solved_equation = ""
    # for all requests
    if request.method == "POST":

        # for solved expression
        if request.form.get("expression_button") == "default_expression_request":
            unsolved_expression = retrieve_expression()
            if unsolved_expression != "":
                solved_expression = solve_expression(unsolved_expression)

        # for angle unit switch
        if request.form.get("angle_unit") == "angle_unit_request":
            print("Before:", session.get("angle_unit", "radians"))
            if angle_unit == "radians":
                angle_unit = "degrees"
            else:
                angle_unit = "radians"

            session["angle_unit"] = angle_unit
            print("After:", session.get("angle_unit", "radians"))
        # for graph
        if request.form.get("graph") == "graph_request":
            graph_equation, x_label, y_label, x_range, step, color = retrieve_graph()

            if graph_equation != "":
                plot_url = graph(graph_equation, x_label, y_label, x_range, step, color)
        # for equation solver
        if request.form.get("equation_solver_button") == "equation_solver_request":
            unsolved_equation, args = retrieve_equation()

            if unsolved_equation != "":
                solved_equation = solve_equation(unsolved_equation, args)

    return render_template("flask_test.html",
                           solved_expression=solved_expression,
                           angle_unit=angle_unit,
                           plot_url=plot_url,
                           solved_equation=solved_equation)


def graph(graph_equation, x_label, y_label, x_range, step, color):
    # Create the graph
    fig = Figure()
    ax = fig.subplots()

    x_range_start = float(x_range.split(",")[0])
    x_range_stop = float(x_range.split(",")[1])
    try:
        # detect x symbols in equation
        x = sympy.symbols("x")
        y = sympy.sympify(graph_equation)

        # create a list for range of graph from 0.0 to 10.0 with step 0.1
        x_values = np.arange(x_range_start, x_range_stop + float(step), float(step))
        # substitute equation for each x value
        y_values = [float(y.subs(x, value)) for value in x_values]
        error_type = ""

    except (ValueError, NameError, SyntaxError, TypeError, sympy.SympifyError) as error:
        error_type = error
    except:
        error_type = "Something went wrong, and I don't know what :("

    if error_type != "":
        print(error_type)
        return error_type

    ax.plot(x_values, y_values, color)

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    # horizontal axis (y-axis)
    ax.axhline(y=0, color="black", linewidth=1)
    # vertical axis (x-axis)
    ax.axvline(x=0, color="black", linewidth=1)

    ax.grid(True)
    # Creating buffer in memory that can store strings of svg formulas for graph
    image_buffer = io.StringIO()

    # Converting image into SVG format
    fig.savefig(image_buffer, format="svg", bbox_inches="tight")

    # Retrieving the data of image from memory and saving it as a string into data
    data = base64.b64encode(image_buffer.getvalue().encode("utf-8")).decode("ascii")

    # Embedding image into url to use in HTML file
    plot_url = f"data:image/svg+xml;base64,{data}"
    return plot_url


@GUI.route("/expression_calculator", methods=["POST"])
def expression_calculator():
    try:
        expression = (request.get_json()).get("expression", "") or ""
        solved_expression = solve_expression(expression)
        print(solved_expression)
        print(type(solved_expression))
        return jsonify({"solved_expression": str(solved_expression)})

    except (KeyError, TypeError, ValueError) as error:
        print(error)
        return jsonify({"solved_expression": str(error)})

@GUI.route("/equation_solver", methods=["POST"])
def equation_solver():
    try:
        equation = (request.get_json()).get("equation", "") or ""
        solved_equation = solve_equation(equation)
        return jsonify({"solved_equation": str(solved_equation)})

    except (KeyError, TypeError, ValueError) as error:
        print(error)
        return jsonify({"solved_equation": str(error)})

@GUI.route("/graph", methods=["POST"])
def graph():
    try:
        graph_equation = (request.get_json()).get("graph", "") or ""

    except (KeyError, TypeError, ValueError) as error:
        print(error)
        return jsonify({"graph_equation": str(error)})

if __name__ == "__main__":
    GUI.run(debug=True)
