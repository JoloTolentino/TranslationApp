import './App.css';
import Signup from './pages/signup';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {
  return (
    <div className="App">
      <Signup />
      <ToastContainer position="top-center" autoClose={3000} />
    </div>
  );
}

export default App;
