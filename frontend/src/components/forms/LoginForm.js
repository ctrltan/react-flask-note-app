import { useContext, useEffect, useState } from "react";
import axios from "axios";
import { UserContext } from "../../App";
import { useNavigate } from "react-router-dom";

export default function LoginForm() {
    const [username, setUsername] = useState(''); 
    const [password, setPassword] = useState('');
    const {user, setUser} = useContext(UserContext);
    const nav = useNavigate();

    const postLogin = async () => {
        if (!user) {
            try {
                const res = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/login`, {
                    'username': username,
                    'password': password,
                });
                const {access_token, session_id, user_id, confirmedUsername} = res.data.message;

                setUser({ user_id: user_id, username: username });
                localStorage.setItem('accessToken', access_token);
                localStorage.setItem('sessionId', session_id);

                nav('/');
            } catch (e) {
                console.log(e);
            };
        } else {
            console.log('already in');
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
        </div>
    );
}