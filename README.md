
# Network Analysis

This project provides a platform for performing network analysis using various backend technologies such as Flask and frontend tools like React.js. Follow the steps below to set up the project locally.

## Prerequisites

Before running the project, ensure the following dependencies are installed:

- [Python](https://www.python.org/downloads/) (latest version)
- [Node.js and npm](https://nodejs.org/)

## Steps to Run the Code

1. **Fork and Clone the Repository**
   
   First, fork the repository from [here](https://github.com/Vaaruna2709/network_analysis/) and then clone it to your local machine. Open a terminal and run the following commands:
   
   git clone https://github.com/YourUsername/network_analysis.git cd network_analysis
2. **Add Python to Environment Variable (Windows Only)**

If you're using Windows, after installing Python, Node.js, and npm, you will need to add Python to your environment variables. You can do this by running the following command in PowerShell:

  $env+=";C:\Users\YourUsername\AppData\Local\Programs\Python\Python313"


3. **Install Backend Dependencies**

To install the backend dependencies, open a terminal and run the following command to install the required Python libraries:

  C:\Users\YourUsername\AppData\Local\Programs\Python\Python313\python.exe -m pip install flask sympy plotly flask_CORS numpy


4. **Navigate to the Cloned Repository Directory**

Ensure you are inside the `network_analysis` directory which you cloned earlier. If not, run the following command:

  cd path/to/network_analysis


5. **Split the Terminal**

You will need to use two terminal windows for this setup: one for the backend server and another for the frontend application.

6. **Start the Backend**

In one terminal window, navigate to the `backend` directory and start the Flask backend server by running the following commands:

  cd backend
  python app.py


The backend server will start and should be accessible at `http://localhost:5000`.

7. **Start the Frontend**

In the other terminal window, navigate to the `frontend` directory. Install the necessary frontend dependencies and start the React development server by running the following commands:

  cd frontend
  npm install # Run this once to install frontend dependencies 
  npm start # Start the frontend development server

The frontend server will start and should be accessible at `http://localhost:3000`.

8. **Access the Application**

Once both the backend and frontend are running, you can access the application in your browser:

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend: [http://localhost:5000](http://localhost:5000)

You should now be able to interact with the network analysis platform both from the frontend and backend.





