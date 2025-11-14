import { useContext } from "react";
import { UserContext } from "../../App";
import axios from "axios";
import { useNavigate } from "react-router-dom";


export default function LogoutButton() {
    const {user, setUser} = useContext(UserContext);
    const nav = useNavigate();
    const accessToken = localStorage.getItem('accessToken');

    const postLogout = async () => {
        try {
            const res = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/logout`, null, { withCredentials: true });

            setUser(null);
            localStorage.clear();
        } catch (e) {
            console.log(e);
        }

        nav('/');
        
    }

    return (
        <div>
            <button onClick={postLogout}>Logout</button>
        </div>
    );
}