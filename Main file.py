import sympy
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
commands = ["exit"]
mode = "radians"

while True:
    print("Welcome to the physics calculator, where you can't write anything useful... yet, muahahhahahahha")
    print(f"The commands are: {commands}")
    while True:
        main_input = input("Enter your equation: ")
        if main_input == "stop":
            break

        if main_input == "radians":
            mode = "radians"
            print("Calculator is now set to radians")
            continue

        if main_input == "degrees":
            mode = "degrees"
            print("Calculator is now set to degrees")
            continue

        try:
            if mode == "degrees":
                trig_functions = {
                    "sin": lambda x: sympy.sin(x * sympy.pi / 180),
                    "cos": lambda x: sympy.cos(x * sympy.pi / 180),
                    "tan": lambda x: sympy.tan(x * sympy.pi / 180),
                    "ctan": lambda x: sympy.cot(x * sympy.pi / 180)
                }
            else:
                trig_functions = {"sin": sympy.sin, "cos": sympy.cos, "tan": sympy.tan, "ctan": sympy.cot}

            expression = sympy.sympify(main_input, locals=trig_functions)
            print(f"Answer: {expression.evalf()}")

        except (NameError, SyntaxError):
            print("ERROR")