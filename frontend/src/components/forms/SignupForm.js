import { useContext, useState } from "react";
import axios from "axios";
import { Navigate, useNavigate } from 'react-router-dom';
import { UserContext } from "../../App";

export default function SignupForm() {
    const [username, setUsername] = useState(''); 
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const {user, setUser} = useContext(UserContext);
    const nav = useNavigate();


    const postSignup = async () => {        
        try {
            const res = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/signup`, {
                    'username': username,
                    'password': password,
                    'email': email,
            });
            const {access_token, session_id, user_id, confirmedUsername} = res.data.message
        
            setUser({ 'user_id': user_id, 'username': username });
            localStorage.setItem('accessToken', access_token);
            localStorage.setItem('sessionId', session_id);

            nav('/');
        } catch (e) {
            console.log(e);
        };
    };

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