



import './styles/signup.css'

function Signup(){



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

                <div className='Submit'>
                    <button type="submit">Free Tier</button>
                    <button type="submit">Pro Tier</button>
                    <button type="submit">Enterprise</button>
                </div>

            </form>

        </div>
    )





}

export default Signup;
