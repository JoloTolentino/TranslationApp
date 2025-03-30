
export interface Credentials {
    Firstname:string,
    Lastname:string, 
    Username:string,
    Password:string,
    Email:string
}; 


export interface SignupPayload extends Credentials{
    method:string
    headers:string,
}



