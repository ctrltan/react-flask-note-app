import { useContext, useEffect, useState } from "react";
import axios from "axios";
import { UserContext } from "../../App";
import { useNavigate } from "react-router-dom";
import { createTheme, styled, ThemeProvider } from "@mui/material/styles";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";
import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import MuiCard from '@mui/material/Card';
import Typography from "@mui/material/Typography";
import Link from "@mui/material/Link";

const LoginContainer = styled(Stack)(({ theme }) => ({
  height: 'calc((1 - var(--template-frame-height, 0)) * 100dvh)',
  minHeight: '100%',
  padding: theme.spacing(2),
  [theme.breakpoints.up('sm')]: {
    padding: theme.spacing(4),
  },
  '&::before': {
    content: '""',
    display: 'block',
    position: 'absolute',
    zIndex: -1,
    inset: 0,
    backgroundImage:
      'radial-gradient(ellipse at 50% 50%, hsla(248, 100%, 97%, 1.00), hsl(0, 0%, 100%))',
    backgroundRepeat: 'no-repeat',
    ...theme.applyStyles('dark', {
      backgroundImage:
        'radial-gradient(at 50% 50%, hsla(210, 100%, 16%, 0.5), hsl(220, 30%, 5%))',
    }),
  },
}));

const Card = styled(MuiCard)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  alignSelf: 'center',
  width: '100%',
  padding: theme.spacing(4),
  gap: theme.spacing(2),
  margin: 'auto',
  boxShadow:
    'hsla(220, 30%, 5%, 0.05) 0px 5px 15px 0px, hsla(220, 25%, 10%, 0.05) 0px 15px 35px -5px',
  [theme.breakpoints.up('sm')]: {
    width: '450px',
  },
  ...theme.applyStyles('dark', {
    boxShadow:
      'hsla(220, 30%, 5%, 0.5) 0px 5px 15px 0px, hsla(220, 25%, 10%, 0.08) 0px 15px 35px -5px',
  }),
}));

const buttonTheme = createTheme({
    palette: {
        background: {
            default: '#faf7ffff'
        }
    },
    components: {
        MuiButton: {
            styleOverrides: {
                root: {
                    backgroundColor: '#7986cb'
                }
            }
        }
    }
});

export default function LoginForm() {
    const [username, setUsername] = useState(''); 
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState(null);
    const [passwordError, setPasswordError] = useState(false);
    const [passwordErrorMessage, setPasswordErrorMessage] = useState('');
    const [usernameError, setUsernameError] = useState(false);
    const [usernameErrorMessage, setUsernameErrorMessage] = useState('');
    const {user, setUser} = useContext(UserContext);
    const nav = useNavigate();

    const postLogin = async () => {
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

                nav('/notes');
            } catch (e) {
                console.log(e);
            };
        } else {
            nav('/notes');
        }
    }

    return (
        <div>
            <ThemeProvider theme={buttonTheme}>
            <LoginContainer>
                <Card>
                    <h2>Login</h2>
                    <Box
                        component="form"
                        action={postLogin}
                        sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}
                    >
                    <FormControl>
                        <FormLabel>Username</FormLabel>
                        <TextField 
                            required
                            fullWidth
                            size="small"
                            name="username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            helperText={usernameErrorMessage}
                            color={usernameError ? 'error' : 'primary'}
                        />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Password</FormLabel>
                        <TextField 
                            required
                            fullWidth
                            size="small"
                            name="password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            helperText={passwordErrorMessage}
                            color={passwordError ? 'error' : 'primary'}
                        />
                    </FormControl>
                    <Typography>{message}</Typography>
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                        >
                        Login
                        </Button>
                        <Typography sx={{ textAlign: 'center' }}>
                        Haven't got an account?{' '}
                        <Link href='/' sx={{ alignSelf: 'center' }}>Sign up</Link>
                    </Typography>
                    </Box>
                </Card>
            </LoginContainer>
            </ThemeProvider>
        </div>
    );
}