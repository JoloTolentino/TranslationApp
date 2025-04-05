
export interface Credentials {
    firstname:string,
    lastname:string, 
    username:string,
    password:string,
    email:string
}; 


export interface SignupPayload {
    method: string;
    headers: { [key: string]: string };
    body: string;
  }


