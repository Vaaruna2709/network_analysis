
import './App.css';
import {BrowserRouter as Router,Routes,Route} from 'react-router-dom'
import Form from './screens/Form';
import Home from './screens/Home';
function App() {
  return (
    <Router>
         <div className="App">
              <Routes>
                <Route path='/' element={<Home/>}/>
               <Route path='/input-values/:type' element={<Form/>}/>
              </Routes>
         </div>
    </Router>
   
  );
}

export default App;
