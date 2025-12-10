import axios from "axios";
import { useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { UserContext } from "../App";

export default function Logout() {
    const {user, setUser} = useContext(UserContext);
    const nav = useNavigate();

    useEffect(() => {
        const postLogout = async () => {
            try {
                const res = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/logout`, null, { withCredentials: true });

                setUser(null);
                localStorage.removeItem('user');
            } catch (e) {
                console.log(e);
            }

            nav('/');
        }
        postLogout();
    })

    return;
}