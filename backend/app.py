from flask import Flask, request, jsonify
from sympy import symbols, exp, sqrt, latex, cos, sin
from sympy.abc import t
from flask_cors import CORS
import numpy as np
import plotly.graph_objects as go
import logging

# Initialize the Flask application and enable CORS
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/solve/<type>', methods=['POST'])
def solve_ode(type):
    # Get R, L, C values from the request and convert them to numeric types
    data = request.json
    try:
        R_value = data.get('R')
        L_value = float(data.get('L', 1))  # Default to 1 if not provided
        C_value = float(data.get('C', 1))  # Default to 1 if not provided

        # Interpret "infinite" for R if provided as such
        if R_value == "infinite":
            if type == "parallel":
                R_value = float('inf')  # Represents infinite resistance in parallel circuits
            else:
                logging.error("Invalid 'R = infinite' for series circuit.")
                return jsonify({'error': "R can be 'infinite' only for parallel circuits."}), 400
        else:
            R_value = float(R_value)

        # Validate positive values for L and C
        if R_value < 0 or L_value <= 0 or C_value <= 0:
            logging.error("Invalid values: R, L, and C must be positive. L and C cannot be zero or negative.")
            return jsonify({'error': 'R must be non-negative, and L, C must be positive.'}), 400
        logging.debug(f"Received values - R: {R_value}, L: {L_value}, C: {C_value}")

    except (ValueError, TypeError) as e:
        logging.error(f"Invalid R, L, or C values provided: {e}")
        return jsonify({'error': 'Invalid R, L, or C values provided.'}), 400

    # Define symbolic constants for the solution
    C1, C2 = symbols('C1 C2')

    # Set up alpha and beta based on type and damping conditions
    if type == "series":
        if R_value == 0:
            damping_condition = "Undamped"
            hom_solution = C1 * cos(sqrt(1 / (L_value * C_value)) * t) + C2 * sin(sqrt(1 / (L_value * C_value)) * t)
        else:
            alpha = -R_value / (2 * L_value)
            beta = sqrt(abs(alpha**2 - (1 / (L_value * C_value))))
            discriminant = R_value**2 - 4 * L_value * (1 / C_value)
            logging.debug("Circuit type: Series")
    elif type == "parallel":
        if R_value == float('inf'):
            damping_condition = "Undamped"
            hom_solution = C1 * cos(sqrt(1 / (L_value * C_value)) * t) + C2 * sin(sqrt(1 / (L_value * C_value)) * t)
        else:
            alpha = -1 / (2 * R_value * C_value)
            beta = sqrt(abs(alpha**2 - (1 / (L_value * C_value))))
            discriminant = (1 / (R_value**2)) - (4 * C_value / L_value)
            logging.debug("Circuit type: Parallel")
    else:
        logging.error("Invalid circuit type specified. Use 'series' or 'parallel'.")
        return jsonify({'error': 'Invalid circuit type specified. Use "series" or "parallel".'}), 400

    logging.debug(f"Computed values - Alpha: {alpha if 'alpha' in locals() else 'N/A'}, Beta: {beta if 'beta' in locals() else 'N/A'}, Discriminant: {discriminant if 'discriminant' in locals() else 'N/A'}")

    # Determine damping condition and form of the homogeneous solution
    if 'discriminant' in locals():
        if discriminant > 0:
            damping_condition = "Overdamped"
            hom_solution = C1 * exp((alpha + beta) * t) + C2 * exp((alpha - beta) * t)
        elif discriminant == 0:
            damping_condition = "Critically Damped"
            hom_solution = (C1 + C2 * t) * exp(alpha * t)
        elif alpha == 0:
            damping_condition = "Undamped"
            hom_solution = C1 * cos(beta * t) + C2 * sin(beta * t)
        else:
            damping_condition = "Underdamped"
            hom_solution = exp(alpha * t) * (C1 * cos(beta * t) + C2 * sin(beta * t))

    logging.debug(f"Damping condition: {damping_condition}")
    logging.debug(f"Homogeneous solution (symbolic): {hom_solution}")

    # Convert solution to LaTeX format
    solution_latex = latex(hom_solution)
    C1_value, C2_value = 1, 1
    # Generate solution values over a time range
    time_values = np.linspace(0, 10, 100)  # Time range from 0 to 10 with 100 points
    hom_solution_values = [
    float(hom_solution.subs({C1: C1_value, C2: C2_value, t: time_val}).evalf()) 
    for time_val in time_values
    ]
    # Generate Plotly figure for the homogeneous solution
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=time_values,
        y=hom_solution_values,
        mode='lines+markers',
        name='Homogeneous Solution'
    ))
    fig.update_layout(
        title=f"Homogeneous Solution ({damping_condition})",
        xaxis_title="Time (t)",
        yaxis_title="Solution Value",
        showlegend=True,
        xaxis=dict(range=[0, 10]),
        yaxis=dict(range=[min(hom_solution_values), max(hom_solution_values)])
    )

    # Convert figure to JSON
    graph_json = fig.to_json()

    # Return graph JSON and damping condition
    return jsonify({'graph_json': graph_json, 'damping_condition': damping_condition, 'solution': solution_latex})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
