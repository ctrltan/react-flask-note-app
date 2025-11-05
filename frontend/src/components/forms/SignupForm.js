import { useState } from "react";
import axios from "axios";

const postSignup = async (formData) => {
    const username = formData.get('username');
    const password = formData.get('password');
    const email = formData.get('email');

    try {
        const res = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/signup`, {
            data: {
                'username': username,
                'password': password,
                'email': email,
            }
        });
        console.log(res.data)
    } catch (e) {
        console.log(e);
    };
}

const SignupForm = () => {
    const [username, setUsername] = useState(''); 
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');


    return (
        <div>
            <h2>Sign Up</h2>
            <form action={postSignup}>
                <label> Username
                    <input 
                        type="text"
                        name="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </label>
                <label> Email
                    <input 
                        type="text"
                        name="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </label>
                <label> Password
                    <input 
                        type="password"
                        name="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </label>
                <button type="submit">Sign Up</button>
            </form>
        </div>
    );
}

export default SignupForm;