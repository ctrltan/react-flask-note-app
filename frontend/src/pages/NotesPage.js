import { useContext, useEffect, useState } from "react";
import { UserContext } from "../App";
import axios from "axios";
import { protectedClient } from "../components/wrappers/ProtectedRoute";
import LogoutButton from "../components/buttons/LogoutButton";
import Toolbar from "@mui/material/Toolbar";
import ListItemText from "@mui/material/ListItemText";
import ListItemButton from "@mui/material/ListItemButton";
import ListItem from "@mui/material/ListItem";
import List from "@mui/material/List";
import Divider from "@mui/material/Divider";
import Drawer from "@mui/material/Drawer";
import CssBaseline from "@mui/material/CssBaseline";
import AppBar from "@mui/material/AppBar";
import Typography from "@mui/material/Typography";


const drawerWidth = 240;



export default function NotesPage() {
    const [notes, setNotes] = useState(null);
    const [message, setMessage] = useState('');
    const {user, setUser} = useContext(UserContext);
    
    useEffect(() => {
        const retrieveNotes = async () => {
            try {
                const res = await protectedClient.get(`${process.env.REACT_APP_BACKEND_URL}/notes`, null, { withCredentials: true });
                console.log(res.data.message);
                if (typeof res.data.message === 'string') {
                    setMessage(res.data.message);
                    return;
                }

                if (Object.keys(notes).length > 0) {
                    setNotes(res.data.message);
                }
            } catch(e) {
                console.log(e)
            }
        }
        retrieveNotes();
    }, [])

    /*components: 
        - side navbar with user
        - note block component to view notes -> clickable notes
        - search bar for notes
    */
    
    return (
        <div>
            <p>{notes ? notes : null}</p>
            <p>{message}</p>
            <CssBaseline />
            <Drawer
                sx={{
                width: drawerWidth,
                flexShrink: 0,
                '& .MuiDrawer-paper': {
                    width: drawerWidth,
                    boxSizing: 'border-box',
                },
                }}
                variant="permanent"
                anchor="left"
            >
                <Toolbar>
                    <Typography>NoteTogether</Typography>
                </Toolbar>
                <Divider />
                <List>
                {['Inbox', 'Starred', 'Send email', 'Drafts'].map((text, index) => (
                    <ListItem key={text} disablePadding>
                    <ListItemButton>
                        <ListItemText primary={text} />
                    </ListItemButton>
                    </ListItem>
                ))}
                {['All mail', 'Trash', 'Spam'].map((text, index) => (
                    <ListItem key={text} disablePadding>
                    <ListItemButton>
                        <ListItemText primary={text} />
                    </ListItemButton>
                    </ListItem>
                ))}
                <ListItemButton>
                    <LogoutButton />
                </ListItemButton>
                </List>
            </Drawer>
        </div>
    )

}