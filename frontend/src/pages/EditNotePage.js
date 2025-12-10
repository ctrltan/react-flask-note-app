import Box from "@mui/material/Box";
import { useParams } from "react-router-dom";
import SideBar from "../components/elements/SideBar";
import { use, useEffect, useState } from "react";
import { protectedClient } from "../components/wrappers/ProtectedRoute";
import NoteForm from "../components/forms/NoteForm";
import Typography from "@mui/material/Typography";


export default function EditNotePage() {
    const { id, slugTitle } = useParams();
    const [noteData, setNoteData] = useState(null);
    const [message, setMessage] = useState(null);

    useEffect(() => {
        const getNote = async () => {
            const noteId = parseInt(id);
            const res = await protectedClient.get(`${process.env.REACT_APP_BACKEND_URL}/notes/get-note`, { 
                params: {
                    'note_id': noteId
                }}, { withCredentials: true });

            if (typeof res.data.message === 'string') {
                setMessage(res.data.message);
                return;
            }
            setMessage(null);

            const { note_id, title, contents, last_accessed, shared } = res.data.message;

            if (!localStorage.getItem(`note-${note_id}`)) {
                localStorage.setItem(`note-${note_id}`, JSON.stringify(res.data.message));
            }
            setNoteData(res.data.message);
        }
        getNote();
    },[])

    return (
        <div>
            <Box sx={{ display: 'flex' }}>
                <SideBar />
                <Box component='main' sx={{ p: 3, flexGrow: 1 }}>
                    {message ? <Typography>{message}</Typography> : noteData ? <NoteForm noteData={noteData}/> : <Typography>Loading...</Typography>}
                </Box>
            </Box>
        </div>
    )
}