from flask import Flask, request, jsonify
from sympy import symbols, exp, sqrt, latex, cos, sin
from sympy.abc import t
from flask_cors import CORS
import numpy as np
import plotly.graph_objects as go

app = Flask(__name__)
CORS(app)


@app.route('/solve/<type>', methods=['POST'])
def solve_ode(type):
   
    data = request.json
    try:
        R_value = data.get('R')
        L_value = float(data.get('L', 1))  
        C_value = float(data.get('C', 1))  

       
        if R_value == "infinite":
            if type == "parallel":
                R_value = float('inf') 
            else:
               
                return jsonify({'error': "R can be 'infinite' only for parallel circuits."}), 400
        else:
            R_value = float(R_value)

      
        if R_value < 0 or L_value <= 0 or C_value <= 0:
           
            return jsonify({'error': 'R must be non-negative, and L, C must be positive.'}), 400
       

    except (ValueError, TypeError) as e:
       
        return jsonify({'error': 'Invalid R, L, or C values provided.'}), 400

    C1, C2 = symbols('C1 C2')

   
    if type == "series":
        if R_value == 0:
            damping_condition = "Undamped"
            hom_solution = C1 * cos(sqrt(1 / (L_value * C_value)) * t) + C2 * sin(sqrt(1 / (L_value * C_value)) * t)
        else:
            alpha = -R_value / (2 * L_value)
            beta = sqrt(abs(alpha**2 - (1 / (L_value * C_value))))
            discriminant = R_value**2 - 4 * L_value * (1 / C_value)
            alpha = round(alpha, 2)
            beta = round(beta, 2)
          
    elif type == "parallel":
        if R_value == float('inf'):
            damping_condition = "Undamped"
            hom_solution = C1 * cos(sqrt(1 / (L_value * C_value)) * t) + C2 * sin(sqrt(1 / (L_value * C_value)) * t)
        else:
            alpha = -1 / (2 * R_value * C_value)
            beta = sqrt(abs(alpha**2 - (1 / (L_value * C_value))))
            alpha = round(alpha, 2)
            beta = round(beta, 2)
            discriminant = (1 / (R_value**2)) - (4 * C_value / L_value)
           
    else:
       
        return jsonify({'error': 'Invalid circuit type specified. Use "series" or "parallel".'}), 400

   
  
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

   
    solution_latex = latex(hom_solution)
    C1_value, C2_value = 1, 1
   
    time_values = np.linspace(0, 10, 100) 
    hom_solution_values = [
    float(hom_solution.subs({C1: C1_value, C2: C2_value, t: time_val}).evalf()) 
    for time_val in time_values
    ]
   
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

    
    graph_json = fig.to_json()

    
    damping_explanations = {
        "Overdamped": "The system is overdamped, meaning it returns to equilibrium without oscillating, but slower than in the critically damped case.",
        "Underdamped": "The system is underdamped, meaning it oscillates as it returns to equilibrium, but with a gradually decreasing amplitude.",
        "Critically Damped": "The system is critically damped, meaning it returns to equilibrium as quickly as possible without oscillating.",
        "Undamped": "The system is undamped, meaning it oscillates indefinitely with constant amplitude."
    }

   
    return jsonify({
        'graph_json': graph_json, 
        'damping_condition': damping_condition, 
        'solution': solution_latex,
        'damping_explanation': damping_explanations[damping_condition]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)

