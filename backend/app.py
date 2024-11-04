from flask import Flask, request, jsonify
from sympy import symbols, exp, sqrt, latex, cos, sin
from sympy.abc import t
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/solve/<type>', methods=['POST'])
def solve_ode(type):
    # Get R, L, C values from the request and convert them to numeric types
    data = request.json
    try:
        R_value = float(data.get('R', 1))  # Default to 1 if not provided
        L_value = float(data.get('L', 1))  # Default to 1 if not provided
        C_value = float(data.get('C', 1))  # Default to 1 if not provided
    except (ValueError, TypeError) as e:
        return jsonify({'error': 'Invalid R, L, or C values provided.'}), 400

    # Define symbolic constants for the solution
    C1, C2 = symbols('C1 C2')

    # Determine the damping condition based on the discriminant
   
   
    # Set up alpha and beta depending on the circuit type (series or parallel)
    if type == "series":
        alpha = R_value / (2 * L_value)
        beta = sqrt(abs(alpha**2 - (1 / (L_value * C_value))))
        discriminant = R_value**2 - 4 * L_value * (1 / C_value)
    elif type == "parallel":
        alpha = -1 / (2 * R_value * C_value)
        beta = sqrt(abs(alpha**2 - (1 / (L_value * C_value))))
        discriminant = (1/R_value)**2 - 4 * C_value * (1 / L_value)
    else:
        return jsonify({'error': 'Invalid circuit type specified. Use "series" or "parallel".'}), 400

    # Round alpha and beta to two decimal places for clarity
    alpha_approx = round(alpha, 2)
    beta_approx = round(beta, 2)

    # Determine the form of the homogeneous solution based on the discriminant
    if discriminant > 0:
        damping_condition = "Overdamped"
        hom_solution = C1 * exp((alpha_approx + beta_approx) * t) + C2 * exp((alpha_approx - beta_approx) * t)
    elif discriminant == 0:
        damping_condition = "Critically Damped"
        hom_solution = (C1 + C2 * t) * exp(alpha_approx * t)
    else:
        damping_condition = "Underdamped"
        hom_solution = exp(alpha_approx * t) * (C1 * cos(beta_approx * t) + C2 * sin(beta_approx * t))

    # Convert the solution to LaTeX format for rendering
    solution_latex = latex(hom_solution)

    # Return the LaTeX string and damping condition in JSON format
    return jsonify({'solution': solution_latex, 'damping_condition': damping_condition})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
# print(type)