import { useContext, useEffect, useState } from "react";
import axios from "axios";
import { Navigate, useNavigate } from 'react-router-dom';
import { UserContext } from "../../App";
import MuiCard from '@mui/material/Card';
import Stack from "@mui/material/Stack";
import { styled } from '@mui/material/styles';
import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";
import TextField from "@mui/material/TextField";
import Box from '@mui/material/Box';
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Link from "@mui/material/Link";

const SignUpContainer = styled(Stack)(({ theme }) => ({
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
    /* backgroundImage:
      'radial-gradient(ellipse at 50% 50%, hsl(210, 100%, 97%), hsl(0, 0%, 100%))', */
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

export default function SignupForm() {
    const [username, setUsername] = useState(''); 
    const [usernameError, setUsernameError] = useState(false);
    const [usernameErrMsg, setUsernameErrMsg] = useState('');

    const [password, setPassword] = useState('');
    const [passwordError, setPasswordError] = useState(false);
    const [passwordColour, setPasswordColour] = useState('primary')
    const [passwordErrMsg, setPasswordErrMsg] = useState('');

    const [email, setEmail] = useState('');
    const [emailError, setEmailError] = useState(false);
    const [emailErrMsg, setEmailErrMsg] = useState('');

    const [message, setMessage] = useState(null);
    const [btnDisabled, setBtnDisabled] = useState(false);

    const {user, setUser} = useContext(UserContext);
    const nav = useNavigate();

    const validateInputs = async () => {
        const validEmail = new RegExp('^[a-zA-Z0-9_.±]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$');

        if (!validEmail.test(email)) {
            setEmailError(true);
            setEmailErrMsg('Invalid email');
        }

        if (username === '') {
            setUsernameError(true);
            setUsernameErrMsg('Invalid username');
        }
    };

    useEffect(() => {
        const containsUppercase = RegExp('(?=.*?[A-Z])').test(password);
        const containsLowercase = RegExp('(?=.*?[a-z])').test(password);
        const containsNumbers = RegExp('(?=.*?[0-9])').test(password);
        const containsSpecialChars = RegExp('(?=.*?[#?!@$%^&*-])').test(password)
        const contains8Chars = RegExp('.{8,}').test(password);

        const validityCount = (containsUppercase + containsLowercase + containsNumbers + containsSpecialChars + contains8Chars);

        if (password === '') {
            setPasswordError(false);
            setPasswordColour('');
            setPasswordErrMsg('');
            setBtnDisabled(true);
        } else if (validityCount === 5) {
            setPasswordError(false);
            setPasswordColour('primary');
            setPasswordErrMsg('');
            setBtnDisabled(false);
        } else if (validityCount > 2) {
            setPasswordError(false);
            setPasswordColour('warning');
            setPasswordErrMsg('Must contain at least 8 characters with min. 1 uppercase, lowercase and special character');
            setBtnDisabled(true);
        } else {
            setPasswordError(true);
            setPasswordColour('error');
            setPasswordErrMsg('Must contain at least 8 characters with min. 1 uppercase, lowercase and special character');
            setBtnDisabled(true);
        };
    }, [password]);

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
            <SignUpContainer direction="column" justifyContent="space-between">
                <Card>
                    <h2>Sign Up</h2>
                    <Box
                        component="form"
                        action={postSignup}
                        sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}
                    >
                    <FormControl>
                        <FormLabel>Username</FormLabel>
                        <TextField 
                            required
                            fullWidth
                            size="small"
                            name="username"
                            type="text"
                            variant="outlined"
                            value={username}
                            error={usernameError}
                            onChange={(e) => setUsername(e.target.value)}
                            helperText={usernameErrMsg}
                            color={usernameError ? 'error' : 'primary'}
                        />
                    </FormControl>
                    <FormControl>
                        <FormLabel>Email</FormLabel>
                        <TextField 
                            required
                            fullWidth
                            size="small"
                            name="email"
                            type="email"
                            value={email}
                            autoComplete="email"
                            variant="outlined"
                            onChange={(e) => setEmail(e.target.value)}
                            error={emailError}
                            helperText={emailErrMsg}
                            color={emailError ? 'error' : 'primary'}
                            placeholder="e.g. you@email.com"
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
                            variant="outlined"
                            autoComplete="new-password"
                            onChange={(e) => setPassword(e.target.value)}
                            error={passwordError}
                            helperText={passwordErrMsg}
                            color={passwordColour}
                        />
                    </FormControl>
                    <Typography>{message}</Typography>
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        disabled={btnDisabled}
                        onClick={validateInputs}
                    >
                    Sign up
                    </Button>
                    <Typography sx={{ textAlign: 'center' }}>
                        Got an account?{' '}
                        <Link href='/login' sx={{ alignSelf: 'center' }}>Login</Link>
                    </Typography>
                    </Box>
                </Card>
            </SignUpContainer>
        </div>
    );
}