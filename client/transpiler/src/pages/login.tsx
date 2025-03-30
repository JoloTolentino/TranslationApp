
import React from 'react'
import { useState } from 'react';
import './styles/login.css';

function Login () :React.JSX.Element{

    const [credentials,setCredentials] = useState({
        username:'',
        password:'',
        cache: false
    })

    const [missing, setMissing] = useState<string[]>([]);


    function handleChange(e:React.ChangeEvent<HTMLInputElement>){
        const { name,value } = e.target;
        if (name === 'cache'){
            setCredentials( prev=> ({
                ...prev,
                cache: !prev.cache
            }));
        }
        else {
            setCredentials(prev => ({
                ...prev,
                [name]:value
            }));
        }
    }

    async function handleSubmit(e:React.FormEvent){
        e.preventDefault();
        const missingFields = Object.entries(credentials).filter(
            ([k,v]) => {
                if (k === 'cache') return false;
                return !v
            } 
        ).map(([key])=> key);
                
        if (missingFields.length > 0){
            setMissing(missingFields);
            setTimeout(() => setMissing([]),4000);
            return 
        };
        alert('Login successful');
        return;        
    }
    
    return (
        <div className='LoginContainer'>
          <h2>Welcome Back!</h2>

          <div className="error">
            {missing.length > 0 && 
                (<>
                    Missing fields: <span>{missing.join(', ')}</span>
                </>)
            }
            </div>
          <form>
            <div className='Credentials'>
                <div>
                <label>Username: </label>
                <input type="string" name="username" 
                        value={credentials.username}
                        onChange={handleChange} required/>
                </div>
                <div>
                <label>Password: </label>
                <input type="password" name="password"
                       value={credentials.password}
                       onChange={handleChange}
                       required/>
                </div>
            </div>
            <div className='form-actions'>
                <div className='cache'>
                    <label htmlFor="radio">Remember Me:</label>
                    <input type='radio' name ='cache'></input>
                </div>
                <button type="submit" onClick={handleSubmit}>Login</button>
                <div className='Redirect'>
                    <span>Forgot your <a>password?</a></span>
                    <span>Create account <a>here.</a></span>
                </div>
                </div>
          </form>
        </div>
      );
}

export default Login;
