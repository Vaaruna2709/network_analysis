

import React, { useState } from 'react';
import axios from 'axios';
import './Form.css';
import { MathJax, MathJaxContext } from 'better-react-mathjax'; // Make sure to install this package
import { useParams } from 'react-router-dom';
import Plot from 'react-plotly.js';
export default function Form() {
    const { type } = useParams();
    let image = '';
    if (type === 'series') {
        image = '/images/series.png';
    } else {
        image = '/images/parallel.png';
    }

    const [formValues, setFormValues] = useState({ "R": "", "L": "", "C": "" });
    const [solution, setSolution] = useState(null);
    const [condition, setCondition] = useState(null);
    const [graphData, setGraphData] = useState({});
    const [error, setError] = useState(null)
    const [typeCircuit,setTypeCircuit] =useState('')
    const [explanation,setExplanation] = useState('')
    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setFormValues((prevValues) => ({ ...prevValues, [name]: value }));
    };

    const formatLaTeX = (latexString) => {
        return latexString
            .replace(/\\int\s/g, '\\int \\ ')
            .replace(/\\left\(/g, '(')
            .replace(/\\right\)/g, ')')
            .replace(/\\sin/g, '\\sin')
            .replace(/\\cos/g, '\\cos')
            .replace(/C_{(\d)}/g, 'C_{ $1 }')
            .replace(/V\{\\left\(t\\right\)\}/g, 'V(t)')
            .replace(/e\^{/g, 'e^{')
            .replace(/\,/g, ', ')
            .replace(/([0-9]*\.?[0-9]*)\s*\\cdot/g, '$1 \\cdot ')
            .replace(/\\,/, ' ')
            .replace(/\\\(/g, '(')
            .replace(/\\\)/g, ')')
            .replace(/e^{-?(\d+(\.\d+)?) t}/g, 'e^{-$1 t}')
            .replace(/(C_{1}|C_{2})/g, '$1')
            .replace(/dt/g, ' \\, dt');
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post(`http://127.0.0.1:5000/solve/${type}`, formValues);
         
            if (response.data) {
                const formattedSolution = formatLaTeX(response.data.solution);
                // const damping_condition = response.data.damping_condition;
                const { graph_json, damping_condition,damping_explanation } = response.data;
                const parsedGraphData = JSON.parse(graph_json);
                const { data, layout, config } = parsedGraphData;
                // console.log(graphData)
                setGraphData({ data, layout, config });
                console.log(graphData)
                setTypeCircuit(type)
                // console.log(type)
                setSolution(formattedSolution);
                setCondition(damping_condition);
                setExplanation(damping_explanation)
                console.log(solution)
            } else {
                throw new Error('No response data received');
            }
        } catch (error) {
            console.error("Error solving differential equation:", error);
            if (error.response && error.response.data && error.response.data.error) {
                // const formattedMessage = error.response.data.error.replace(/\n/g, '<br />');
                // setSolution(formattedMessage);
                console.log(error.response.data.error)
                setError(error.response.data.error)

            } else {
                setError('An error occurred while solving the equation');
            }
        }
    };

    return (
        <div className="form">
            <div className="form-card">
                <img src={image} alt={type} className="form-image" />
                <form onSubmit={handleSubmit} className="form-content" style={{ height: '100%' }}>
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
            </div>
            {(error || solution) && (
                <div className="solution-card">
                    {error ? (
                        <div className="error-message">
                            <p>{error}</p>
                        </div>
                    ) : (
                        solution && (
                            <MathJaxContext>
                                <div className="solution-content">
                                    <h4>Solution:</h4>
                                    <MathJax inline>{`\\[${typeCircuit === 'series' ? 'i(t) = ' : 'v(t) = '}${solution}\\]`}</MathJax>
                                    <p>{condition}</p>
                                    <p>{explanation}</p>
                                </div>
                            </MathJaxContext>
                        )
                    )}

                    {graphData.data && graphData.layout && (
                        <div className="graph">
                            <Plot
                                data={graphData.data}
                                layout={{
                                    ...graphData.layout,
                                    autosize: true,
                                    width: undefined,
                                    height: undefined
                                }}
                                config={graphData.config}
                                useResizeHandler
                                style={{ width: '90%', height: '100%' }}
                            />
                        </div>
                    )}
                </div>
            )}



        </div>

    );
}
