// toggle between hiding and showing the dropdown content
function dropdownFunction(dropdownID) {
  document.getElementById(dropdownID).classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
  if (!event.target.closest('.dropdown')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");

    for (let i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];

      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }
  }
}

// for numpad
const numpadBtns = document.querySelectorAll(".num-pad button");
const expressionInput = document.getElementById("expression_input");

numpadBtns.forEach(button => {
  button.addEventListener("click", function() {
      expressionInput.value += this.dataset.value;
  });
});
console.log(numpadBtns);

// for expression
let timeout;

expressionInput.addEventListener("input", async function() {
  clearTimeout(timeout)
  timeout = setTimeout(async function () {
    const expression = expressionInput.value;

    if (expression.trim() === "") {
      document.getElementById("solved_expression").textContent = "";
      return;
    }
    console.log(expression)

    const response = await fetch("/expression_calculator", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({expression: expression})
    });

    const data = await response.json();
    console.log(data.solved_expression);
    document.getElementById("solved_expression").textContent = data.solved_expression;
  }, 300);
});

// for equation
const equationInput = getElementsById("equation_solver_input")
const solveBtn = getElementById("equation_solver_button")
const equationArgs = getElementById("args_for_equation_solver")

solveBtn.addEventListener("click", function() {
  const equation = equationInput.value;
  const args = equationArgs.value;
  if (equation.trim() === "" || args.trim() === "") {
      document.getElementById("solved_equation").textContent = "";
      return;
    }

  const response = fetch("/equation_solver", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({equation: equation, args: args})
  });

  const data = response.json;
  console.log(data.solved_equation);
  document.getElementById("solved_equation").textContent = data.solved_equation;
});
