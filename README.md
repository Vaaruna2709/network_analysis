
# Network Analysis

This project provides a platform for performing network analysis using various backend technologies such as Flask and frontend tools like React.js. Follow the steps below to set up the project locally.

## Prerequisites

Ensure the following dependencies are installed before running the project:

- [Python](https://www.python.org/downloads/) (latest version)
- [Node.js and npm](https://nodejs.org/)

### Steps to Run the Code

#### 1. Fork and Clone the Repository

- Fork the repository from [here](https://github.com/Vaaruna2709/network_analysis/) and clone it to your local machine:
  ```bash
  git clone https://github.com/YourUsername/network_analysis.git
  cd network_analysis
### 2.Add Python to Environment Variable (Windows Only)
After installing Python, Node.js, and npm, add Python to your environment variables using the following command:
  $env:Path+=";C:\Users\YourUsername\AppData\Local\Programs\Python\Python313"

### 3. Install Backend Dependencies
Run this command in the command prompt to install the necessary backend Python dependencies:

   C:\Users\YourUsername\AppData\Local\Programs\Python\Python313\python.exe -m pip install flask sympy plotly flask_CORS numpy

### 4. Navigate to the Cloned Repository Directory
  cd path/to/network_analysis

### 5. Split the Terminal
### 6. Start the Backend
In one terminal pane, navigate to the backend directory and start the Flask backend server:
  cd backend
  python app.py
### 7. Start the Frontend
In the other terminal pane, navigate to the frontend directory and start the frontend application:
   cd frontend
   npm install  # Run this once to install frontend dependencies
   npm start    # Start the frontend development server
### 8. Access the Application
After starting both the backend and frontend, the application should be accessible locally:
Frontend: http://localhost:3000
Backend: http://localhost:5000
