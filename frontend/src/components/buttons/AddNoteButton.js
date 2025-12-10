import React, { useState } from "react";
import Button from "@mui/material/Button";
import AddCircleOutlineRoundedIcon from '@mui/icons-material/AddCircleOutlineRounded';
import Stack from "@mui/material/Stack";
import { protectedClient } from "../wrappers/ProtectedRoute";
import { useNavigate } from "react-router-dom";
import slugifyTitle from "../hooks/slugifyTitle";


export default function AddNoteButton() {
    const nav = useNavigate();
    const [message, setMessage] = useState('');

    const addNote = async () => {
        try {
            const res = await protectedClient.get(`${process.env.REACT_APP_BACKEND_URL}/notes/new-note`, null, { withCredentials: true });
            console.log(res.data.message);

            if (typeof res.data.message === 'string') {
                setMessage(res.data.message);
                return;
            }
            
            setMessage('');

            const {note_id, title} = res.data.message;
            const slugTitle = slugifyTitle(title);

            nav(`/notes/${note_id}/${slugTitle}`);
        } catch (e) {
            console.log(e);
        }
    }

    return (
        <React.Fragment>
            <Button size="large" onClick={addNote}>
                <Stack direction='row' sx={{ gap: 1 }}>
                    <AddCircleOutlineRoundedIcon/>
                    Create Note
                </Stack>
            </Button>
        </React.Fragment>
    )
}