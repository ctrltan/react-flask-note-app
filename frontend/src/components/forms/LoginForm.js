import { useState } from "react";
import axios from "axios";

const postLogin = async (formData) => {
    const username = formData.get("username");
    const password = formData.get("password");

    try {
        const res = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/login`, {
            data: {
                'username': username,
                'password': password
            }
        });
    } catch (e) {
        console.log(e);
    };
}

const LoginForm = () => {
    const [username, setUsername] = useState(''); 
    const [password, setPassword] = useState(''); 


    return (
        <div>
            <h2>Login</h2>
            <form action={postLogin}>
                <label> Username
                    <input 
                        type="text"
                        name="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </label>
                <label> Password
                    <input 
                        type="password"
                        name="username"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </label>
                <button type="submit">Login</button>
            </form>
        </div>
    );
}

export default LoginForm;