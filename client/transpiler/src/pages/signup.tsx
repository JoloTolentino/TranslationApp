


import { useEffect, useState } from 'react';
import { Credentials,SignupPayload } from '../types/signup'

import './styles/signup.css'

function Signup(){
    const [selected,setSelected] = useState<number>(2); 
    const [credentials,setCredentials] =useState<Credentials>({firstname:'',
                                                               lastname:'',
                                                               username:'',
                                                               password:'',
                                                               email:''});


    const SIGNUP_URL= `${import.meta.env.VITE_FLASK_BACKEND}/signup`
    
    function handleChange(e:React.ChangeEvent<HTMLInputElement>){
        const { name,value } = e.target;
        setCredentials((creds)=> ({
            ...creds,
            [name]:value
        }))
    }


    async function handleClick(label: string): Promise<void> {
        const subscription = label;

        const updatedCredentials = {
            ...credentials,
            subscription,
        };

        const payload: SignupPayload = {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedCredentials),
        };

        try {
            const response = await fetch(SIGNUP_URL, payload);
            console.log('response:', response);
            const data = await response.json();
            console.log('response data:', data);
        } catch (err) {
            console.error('Fetch error:', err);
        }
}


    function SubmitButtons(){
        const buttons = ['Free Tier','Pro Tier','Enterprise'];  
        return(
            <div className='Submit'>
                {buttons.map((label,index)=>{
                return (
                    <button key={index} 
                            onMouseEnter= {()=>setSelected(index)} 
                            onClick={() =>handleClick(label)}
                            className= {index ==selected ?"selected_index":"not_selected_index"}>
                                {label}
                    </button>
                )})}
            </div>
        );
        
    }


    return (
        <div className='SignUp'>
            <form className="PersonalInfo">
                <h3>PERSONAL INFORMATION :</h3>
                <div className='Firstname'>
                    <label>Firstname<span>*</span></label>
                    <input type="string" 
                            name="firstname" 
                            value={credentials.firstname}
                            onChange={handleChange}
                            required/>
                </div>
                <div className='Lastname'>
                    <label>Lastname</label>
                    <input type="string" 
                            name="lastname" 
                            value={credentials.lastname}
                            onChange={handleChange}
                            required/>
                </div>

                <h3>SIGNUP INFORMATION :</h3>

                <div className='Username'>
                    <label>Username<span>*</span></label>
                    <input type="string" 
                            name="username" 
                            value={credentials.username}
                            onChange={handleChange}
                            required/>
                </div>

                <div className='Password'>
                    <label>Password<span>*</span></label>
                    <input type="password" 
                            name="password" 
                            value={credentials.password}
                            onChange={handleChange}
                            required/>
                </div>

                <div className='Email'>
                    <label>Email<span>*</span></label>
                    <input type="email" 
                            name="email"
                            value={credentials.email} 
                            onChange={handleChange}
                            required/>
                </div>

                <SubmitButtons/>
                
            </form>

        </div>
    )





}

export default Signup;
