import { useContext, useEffect } from "react";
import { UserContext } from "../../App";
import { Navigate, Outlet, useNavigate } from "react-router-dom";
import axios from "axios";


export default function ProtectedRoute() {
    const { user, setUser } = useContext(UserContext);
    const nav = useNavigate();
    
    axios.interceptors.response.use(response => {
        return response; 
    }, async error => {
        const request = error.config;
        if (error.response.status === 401 && !request._retry ) {
            try {
                request._retry = true;
                const res = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/auth/refresh`, { 
                    'user_id': user['userId'],
                    'username': user['username'],
                }, { withCredentials: true });
                return axios(request);
            } catch (refreshError) {
                nav('/logout');
            }
        }

        return Promise.reject(error);
    });

    return (
        user ? <Outlet /> : <Navigate to='/login'/>
    )
}