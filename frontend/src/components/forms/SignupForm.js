import { useContext, useState } from "react";
import axios from "axios";
import { Navigate, useNavigate } from 'react-router-dom';
import { UserContext } from "../../App";

export default function SignupForm() {
    const [username, setUsername] = useState(''); 
    const [password, setPassword] = useState('');
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState(null);
    const {user, setUser} = useContext(UserContext);
    const nav = useNavigate();


    const postSignup = async () => {        
        try {
            const res = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/signup`, {
                    'username': username,
                    'password': password,
                    'email': email,
            }, { withCredentials: true });

            if (typeof res.data.message === 'string') {
                setMessage(res.data.message);
                return;
            };

            const {user_id, x} = res.data.message
        
            setUser({ userId: user_id, username: username });

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
            <p>{message}</p>
        </div>
    );
}