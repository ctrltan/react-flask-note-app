import { useContext, useEffect, useState } from "react";
import axios from "axios";
import { UserContext } from "../../App";
import { useNavigate } from "react-router-dom";

export default function LoginForm() {
    const [username, setUsername] = useState(''); 
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState(null);
    const {user, setUser} = useContext(UserContext);
    const nav = useNavigate();

    const postLogin = async () => {
        console.log(user)
        if (user === null) {
            try {
                const res = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/login`, {
                    'username': username,
                    'password': password,
                }, { withCredentials: true });

                if (typeof res.data.message === 'string') {
                    setMessage(res.data.message);
                    return;
                };

                const {user_id, x} = res.data.message;
                
                setUser({ userId: user_id, username: username });

                nav('/');
            } catch (e) {
                console.log(e);
            };
        } else {
            nav('/');
        }
    }

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
                        name="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </label>
                <button type="submit">Login</button>
            </form>
            <p>{message}</p>
        </div>
    );
}