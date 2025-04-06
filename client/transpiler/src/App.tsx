import './App.css';
import Signup from './pages/signup';
import Login from './pages/login';
import { ToastContainer } from 'react-toastify';
import { Routes, Route } from 'react-router-dom'
import 'react-toastify/dist/ReactToastify.css';




function App() {
  return (
    <div className="App">
      <Routes>
        <Route path = "/login" element= {<Login />}/>
        <Route path = "/signup" element= {<Signup />}/>
      </Routes>
      <ToastContainer position="top-center" />
    </div>
  );
}

export default App;
