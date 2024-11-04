


import React, { useState } from 'react';
import axios from 'axios';
import './Form.css';
import { MathJax, MathJaxContext } from 'better-react-mathjax'; // Make sure to install this package
import { useParams } from 'react-router-dom';

export default function Form() {
    const {type} = useParams()
    let image='';
    if(type=='series'){
        image = '/images/series.png'
    }else{
        image = '/images/parallel.png'
    }
    const [formValues, setFormValues] = useState({ R: "", L: "", C: "" });
    const [solution, setSolution] = useState(null);
    const [condition, setCondition] = useState(null)
    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setFormValues((prevValues) => ({ ...prevValues, [name]: value }));
    };



    const formatLaTeX = (latexString) => {
        return latexString
            .replace(/\\int\s/g, '\\int \\ ') // Ensure space before the integrals
            .replace(/\\left\(/g, '(') // Remove \left and \right for cleaner output
            .replace(/\\right\)/g, ')')
            .replace(/\\sin/g, '\\sin') // Properly format sin
            .replace(/\\cos/g, '\\cos') // Properly format cos
            .replace(/C_{(\d)}/g, 'C_{ $1 }') // Format C1 and C2 correctly
            .replace(/V\{\\left\(t\\right\)\}/g, 'V(t)') // Format V(t)
            .replace(/e\^{/g, 'e^{') // Fix exponent formatting
            .replace(/\,/g, ', ') // Add space after commas
            .replace(/([0-9]*\.?[0-9]*)\s*\\cdot/g, '$1 \\cdot ') // Format dot multiplication with space
            .replace(/\\,/, ' ') // Replace \, with space for better readability
            .replace(/\\\(/g, '(') // Remove unnecessary escape for parenthesis
            .replace(/\\\)/g, ')') // Remove unnecessary escape for parenthesis
            .replace(/e^{-?(\d+(\.\d+)?) t}/g, 'e^{-$1 t}') // Format exponentials
            .replace(/(C_{1}|C_{2})/g, '$1') // Ensure C1 and C2 are treated as subscripts
            .replace(/dt/g, ' \\, dt'); // Format differential terms with space
    };


    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post(`http://127.0.0.1:5000/solve/${type}`, formValues);
            const formattedSolution = formatLaTeX(response.data.solution);
            const damping_condition = response.data.damping_condition;
            setSolution(formattedSolution);
            setCondition(damping_condition);
            console.log(formattedSolution)
        } catch (error) {
            console.error("Error solving differential equation:", error);
            setSolution("Error in solving equation.");
        }
    };

    return (
      
        <div className="form">
                   <div className="form-card">
                <img src={image} alt={type} className="form-image" />
                <form onSubmit={handleSubmit} className="form-content">
                    <div className="form-input-group">
                        <div className="form-inputs">
                            <label htmlFor='R' className="form-label">R :</label>
                            <input value={formValues.R} name='R' type="text" onChange={handleInputChange} id='R' className='form-input' />
                        </div>
                        <div className="form-inputs">
                            <label htmlFor='L' className="form-label">L :</label>
                            <input value={formValues.L} name='L' type="text" onChange={handleInputChange} id='L' className='form-input' />
                        </div>
                        <div className="form-inputs">
                            <label htmlFor='C' className="form-label">C :</label>
                            <input value={formValues.C} name='C' type="text" onChange={handleInputChange} id='C' className='form-input' />
                        </div>
                    </div>
                    <button type="submit" className="form-button">Submit</button>
                </form>
                {solution && (
                    <MathJaxContext>
                        <div className='sol' style={{display:'flex',flexDirection:'column',justifyContent:'center',alignItems:'center',width:'100%'}} >
                            <h4 style={{ color: '#262626' }}>Solution:</h4>
                            <MathJax inline style={{ color: '#262626' }}>{`\\[${solution}\\]`}</MathJax>
                            <p style={{ color: '#262626' }}>{condition}</p>
                        </div>
                    </MathJaxContext>
                )}
            </div>
        </div>
           
        

    );
}
