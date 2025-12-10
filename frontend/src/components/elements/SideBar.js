import LogoutButton from "../buttons/LogoutButton";
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
import { useContext } from "react";
import { UserContext } from "../../App";
import { useNavigate } from "react-router-dom";

const drawerWidth = 240;



export default function SideBar() {
    const {user, setUser} = useContext(UserContext);
    const nav = useNavigate();

    const getAllNotes = () => {
        nav('/notes');
    }

    const getUserNotes = () => {
        nav('/notes?filter=user');
    }

    const getSharedNotes = () => {
        nav('/notes?filter=shared');
    }

    return (
        <div>
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
                    <Typography sx={{ fontWeight: 800 }}>NoteTogether</Typography>
                </Toolbar>
                
                <List>
                    <ListItem disablePadding>
                    <ListItemButton onClick={getAllNotes}>
                        <ListItemText>All Notes</ListItemText>
                    </ListItemButton>
                    </ListItem>
                    <ListItem disablePadding>
                    <ListItemButton onClick={getUserNotes}>
                        <ListItemText>Your Notes</ListItemText>
                    </ListItemButton>
                    </ListItem>
                    <ListItem disablePadding>
                    <ListItemButton onClick={getSharedNotes}>
                        <ListItemText>Shared Notes</ListItemText>
                    </ListItemButton>
                    </ListItem>
                </List>
                <List style={{ position: 'absolute', bottom: 0 }}>
                    <ListItem>
                        <LogoutButton />
                    </ListItem>
                </List>
            </Drawer>
        </div>
    )
}