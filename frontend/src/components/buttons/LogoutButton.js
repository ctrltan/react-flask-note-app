import { useContext } from "react";
import { UserContext } from "../../App";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import Button from "@mui/material/Button";
import LogoutRoundedIcon from '@mui/icons-material/LogoutRounded';
import Typography from "@mui/material/Typography";
import Stack from "@mui/material/Stack";
import { createTheme } from "@mui/material/styles";
import { ThemeProvider } from "@emotion/react";


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
            <Button onClick={postLogout} variant="text" size="medium">
                <Stack direction='row' sx={{ gap: 1 }}>
                    Logout
                    <LogoutRoundedIcon/>
                </Stack>
            </Button>
        </div>
    );
}