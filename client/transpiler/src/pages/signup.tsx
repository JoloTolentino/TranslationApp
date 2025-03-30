


import { useEffect, useState } from 'react';
import { Credentials,SignupPayload } from '../types/signup'

import './styles/signup.css'

function Signup(){
    const [selected,setSelected] = useState<number>(2); 
    const [credentials,setCredentials] =useState<Credentials>({Firstname:'',
                                                               Lastname:'',
                                                               Username:'',
                                                               Password:'',
                                                               Email:''});

    // async function handleClick(label:string):Promise<void> {
    //     const payload:SignupPayload = {
    //         headers: 'application/json',
    //         method: 'POST',
    //         ...credentials
    //     }};

    //     const response = await fetch();

    //     if(!(response.ok)){

    //     }



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
                            required/>
                </div>

                <div className='Lastname'>
                    <label>Lastname</label>
                    <input type="string" 
                            name="firstname" 
                            required/>
                </div>

                <h3>SIGNUP INFORMATION :</h3>

                <div className='Firstname'>
                    <label>Username<span>*</span></label>
                    <input type="string" 
                            name="username" 
                            required/>
                </div>

                <div className='Lastname'>
                    <label>Password<span>*</span></label>
                    <input type="password" 
                            name="password" 
                            required/>
                </div>

                <div className='Email'>
                    <label>Email<span>*</span></label>
                    <input type="email" 
                            name="firstname" 
                            required/>
                </div>

                {
                    SubmitButtons()
                }

              

            </form>

        </div>
    )





}

export default Signup;
