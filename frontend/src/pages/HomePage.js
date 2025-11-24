import { useContext, useEffect, useState } from 'react';
import axios from 'axios';
import { UserContext } from '../App';
import LogoutButton from '../components/buttons/LogoutButton';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Stack from '@mui/material/Stack';
import SignupForm from '../components/forms/SignupForm';
import Typography from '@mui/material/Typography';
import Diversity3RoundedIcon from '@mui/icons-material/Diversity3Rounded';
import NotesRoundedIcon from '@mui/icons-material/NotesRounded';
import SaveRoundedIcon from '@mui/icons-material/SaveRounded';

const theme = createTheme({
    palette: {
        background: {
            default: '#faf7ffff'
        }
    }
})

const HomeContent = () => {
    return (
        <CssBaseline>
        <Stack sx={{ flexDirection: 'column', alignSelf: 'center', gap: 2 }}>
            <Typography variant='h4'><strong>NoteTogether</strong></Typography>
            <Stack direction='row' sx={{ gap: 1 }}>
                <NotesRoundedIcon/>
                <Typography sx={{ color: 'text.secondary' }}>Easy-to-use creation and editing of notes</Typography>
            </Stack>
            <Stack direction='row' sx={{ gap: 1 }}>
                <SaveRoundedIcon/>
                <Typography sx={{ color: 'text.secondary' }}>Keep notes up-to-date with auto-save</Typography>
            </Stack>
            <Stack direction='row' sx={{ gap: 1 }}>
                <Diversity3RoundedIcon/>
                <Typography sx={{ color: 'text.secondary' }}>Create notes with your friends and edit together</Typography>
            </Stack>
        </Stack>
        </CssBaseline>
    )
}

export default function HomePage() {
    const [apiData, setApiData] = useState('');
    const {user, setUser} = useContext(UserContext);

    useEffect(() => {
        const getData = async () => {
            console.log(process.env.REACT_APP_BACKEND_URL)
            const response = await axios.get(process.env.REACT_APP_BACKEND_URL);
            setApiData(response.data.message);
        }

        getData();
    }, []);

    return (
        <ThemeProvider theme={theme}>
            <div>
            <CssBaseline/>
                <Stack 
                    direction="column"
                    component="main"
                    sx={{
                        justifyContent: 'center',
                        height: 'calc((1 - var(--template-frame-height, 0)) * 100%)',
                        marginTop: 'max(40px - var(--template-frame-height, 0px), 0px)',
                        minHeight: '100%',
                    }}
                >
                    <Stack direction={{ xs: 'column-reverse', md: 'row' }} sx={{
                        justifyContent: 'center',
                        gap: { xs: 6, sm: 12 },
                        p: 2,
                        mx: 'auto',}}
                    >
                        <Stack direction={{ xs: 'column-reverse', md: 'row' }} sx={{ 
                            justifyContent: 'center', 
                            m: 'auto', 
                            gap: { xs: 6, sm: 12 }, 
                            p: { xs: 2, sm: 4 } }}
                        >
                            <HomeContent />
                            <SignupForm />
                        </Stack>
                    </Stack>
                </Stack>
            </div>
        </ThemeProvider>
    );
}