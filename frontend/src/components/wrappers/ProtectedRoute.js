import { useContext, useEffect, useState } from "react";
import { UserContext } from "../../App";
import { Navigate, Outlet, useNavigate, useOutletContext } from "react-router-dom";
import axios from "axios";

export const protectedClient = axios.create({withCredentials: true});

export default function ProtectedRoute() {
    const { user, setUser } = useContext(UserContext);
    const [auth, setAuth] = useState(true);
    const nav = useNavigate();

    console.log('checking...');

    const refreshRetry = async () => {
        const res = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/auth/refresh`, { 
            'user_id': user['userId'],
            'username': user['username'],
        }, { withCredentials: true });
    }

    protectedClient.interceptors.response.use(response => {
        return response;
    }, error => {
        const request = error.config;
        if (error.response.status === 401 && !request._retry) {
            try {
                request._true = true;
                refreshRetry();
                return axios(request);
            } catch (e) {
                nav('/logout');
            }
        }

        Promise.reject(error);
    });

    return (
        user ? <Outlet /> : <Navigate to='/login'/>
    )
}