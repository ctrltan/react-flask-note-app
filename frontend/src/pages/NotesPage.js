import { useContext, useEffect, useState } from "react";
import { UserContext } from "../App";
import axios, { all } from "axios";
import { protectedClient } from "../components/wrappers/ProtectedRoute";
import SideBar from "../components/elements/SideBar";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import NoteCard from "../components/elements/NoteCard";
import Button from "@mui/material/Button";
import AppBar from "@mui/material/AppBar";
import Stack from "@mui/material/Stack";
import AddCircleOutlineRoundedIcon from '@mui/icons-material/AddCircleOutlineRounded';
import AddNoteButton from "../components/buttons/AddNoteButton";
import { useSearchParams } from "react-router-dom";


export default function NotesPage() {
    const [notes, setNotes] = useState(null);
    const [message, setMessage] = useState('Loading...');
    const [heading, setHeading] = useState(null);
    const [searchParams] = useSearchParams();
    const {user, setUser} = useContext(UserContext);
    const filter = searchParams.get('filter');

    const noteFilter = (allNotes) => {
        if (!filter) {
            setHeading(null);
            return allNotes;
        } else if (filter === 'user') {
            setHeading('Your Notes');
            const userNotes = Object.fromEntries(
                Object.entries(allNotes).filter(([id, data]) => {
                    return data.shared === false;
                })
            );
            return (userNotes);
        } else if (filter === 'shared') {
            setHeading('Shared Notes');
            const sharedNotes = Object.fromEntries(
                Object.entries(allNotes).filter(([id, data]) => {
                    return data.shared === true;
                })
            );
            return sharedNotes;
        } else {
            setHeading(null);
            return allNotes;
        }
    }
    
    useEffect(() => {
        const retrieveNotes = async () => {
            try {
                const res = await protectedClient.get(`${process.env.REACT_APP_BACKEND_URL}/notes`, null, { withCredentials: true });

                if (typeof res.data.message === 'string') {
                    setMessage(res.data.message);
                    return;
                }

                setMessage('');

                if (Object.keys(res.data.message).length > 0) {
                    const filteredNotes = noteFilter(res.data.message);
                    setNotes(filteredNotes);
                } else {
                    setMessage('No notes yet');
                }
            } catch(e) {
                console.log(e)
                setMessage('Try again later');
            }
        }
        retrieveNotes();
    }, [filter])
    
    return (
        <div>
            <Box sx={{ display: 'flex' }}>
                <SideBar />
                <Box component='main' sx={{ p: 3, flexGrow: 1 }}>
                    <Stack direction='row' sx={{ width: '100%' }}>
                        <Typography variant="h6" sx={{ fontWeight: 500, flexGrow: 1 }}>
                            {user.username}'s Note Space
                        </Typography>
                        <AddNoteButton/>
                    </Stack>
                    {heading ? <Typography variant="overline">{heading}</Typography> : heading}
                    {notes ?
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
                            {Object.entries(notes).map(([id, note]) => 
                                <NoteCard noteData={note} noteId={id}/>
                            )}
                        </Box>
                    : <p>{message}</p>}
                </Box>
            </Box>
        </div>
    )

}