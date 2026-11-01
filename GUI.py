import base64
import sympy
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

from flask import Flask, request, render_template, session
from matplotlib.figure import Figure

def solve_equation(equation):
    angle_unit = session.get("angle_unit", "radians")
    if angle_unit == "degrees":
        trig_functions = {
            "sin": lambda x: sympy.sin(x * sympy.pi / 180),
            "cos": lambda x: sympy.cos(x * sympy.pi / 180),
            "tan": lambda x: sympy.tan(x * sympy.pi / 180),
            "ctan": lambda x: sympy.cot(x * sympy.pi / 180)
            }
    else:
        trig_functions = {
            "sin": sympy.sin, 
            "cos": sympy.cos, 
            "tan": sympy.tan, 
            "ctan": sympy.cot
            }
        
    expression = sympy.sympify(equation, locals=trig_functions)
    evaluated_expression = expression.evalf()    
    return str(evaluated_expression)


def retrieve_equation():
    unsolved_equation = request.form.get("equation", "")
    return unsolved_equation

def retrieve_graph():
    graph_equation = request.form.get("graph_equation", "")
    return graph_equation

GUI = Flask(__name__)
GUI.secret_key = "Calc-short-for-calculator"
@GUI.route("/", methods=["GET", "POST"])

def return_equation():
    solved_equation = ""
    angle_unit = session.get("angle_unit", "radians")
    plot_url = ""
    if request.method == "POST":
        unsolved_equation = retrieve_equation()
        
    #for solved equation
        if unsolved_equation != "":
            solved_equation = solve_equation(unsolved_equation)
            
    #for angle unit switch
        if request.form.get("angle_unit") == "pressed":
            if angle_unit == "radians":
                angle_unit = "degrees"
            else:
                angle_unit = "radians"
        
            session["angle_unit"] = angle_unit
        
        if request.form.get("graph") == "activated":
            y = retrieve_graph()
            plot_url = graph(y)
    
    return render_template("flask_test.html", solved_equation=solved_equation, angle_unit=angle_unit, plot_url=plot_url), angle_unit
               
def graph(graph_equation):
    # Create the graph
    fig = Figure()
    ax = fig.subplots()
    
    try: 
        #detect x symbols in equation
        x = sympy.symbols("x")
        y = sympy.sympify(graph_equation)
        
        #create a list for range of graph from 0.0 to 10.0 with step 0.1
        x_values = np.arange(0.0, 10.0, 0.1)
        #substitute equation for each x value
        y_values = [float(y.subs(x, value)) for value in x_values]
        errorType = ""
    
    except NameError:
        errorType = "Name error"
    except SyntaxError:
        errorType = "Syntax error"
    except TypeError:
        errorType = "Type error"
    except:
        errorType = "Something went wrong :("
    
    if errorType != None:
        print(errorType)
        return errorType
            
        
    ax.plot(x_values, y_values)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")

    # Convert the graph into a PNG image
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")

    # Encode the image so it can be embedded in HTML
    data = base64.b64encode(buf.getvalue()).decode("ascii")
    # Graph image url to use in HTML file
    plot_url = f"data:image/png;base64,{data}"

    return plot_url


if __name__ == "__main__":
    GUI.run(debug=True)

