import Box from "@mui/material/Box";
import { useParams } from "react-router-dom";
import SideBar from "../components/elements/SideBar";
import { use, useEffect, useState } from "react";
import { protectedClient } from "../components/wrappers/ProtectedRoute";
import NoteForm from "../components/forms/NoteForm";


export default function EditNotePage() {
    const { id, slugTitle } = useParams();
    const [noteData, setNoteData] = useState(null);
    const [message, setMessage] = useState('');

    useEffect(() => {
        const getNote = async () => {
            const note_id = parseInt(id);
            const res = await protectedClient.get(`${process.env.REACT_APP_BACKEND_URL}/notes/get-note`, { 
                params: {
                    'note_id': note_id
                }}, { withCredentials: true });

            if (typeof res.data.message === 'string') {
                setMessage(res.data.message);
                return;
            }
            setMessage('');
            setNoteData(res.data.message);
        }
        getNote();
    },[])

    return (
        <div>
            <Box sx={{ display: 'flex' }}>
                <SideBar />
                <Box component='main' sx={{ p: 3, flexGrow: 1 }}>
                    <NoteForm noteData={noteData}/>
                </Box>
            </Box>
        </div>
    )
}