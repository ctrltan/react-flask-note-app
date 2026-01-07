import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";
import Stack from "@mui/material/Stack";
import TextField from "@mui/material/TextField";
import Typography from "@mui/material/Typography";
import { useEffect, useRef, useState } from "react"
import React from "react";
import { protectedClient } from "../wrappers/ProtectedRoute";
import NoteSaveButton from "../buttons/NoteSaveButton";
import NoteDeleteButton from "../buttons/NoteDeleteButton";


export default function NoteForm({ noteData }) {
    const [title, setTitle] = useState(JSON.parse(localStorage.getItem(`note-${noteData.note_id}`)).title);
    const [contents, setContents] = useState(JSON.parse(localStorage.getItem(`note-${noteData.note_id}`)).contents);
    const [message, setMessage] = useState('');
    
    const [online, setOnline] = useState(true);
    const saveTimer = useRef(null);
    const messageTimer = useRef(null);

    useEffect(() => {
        const updatedNote = {
            'note_id': noteData.note_id,
            'title': title,
            'contents': contents,
            'last_accessed': new Date().toISOString(),
            'shared': false
        }
        localStorage.setItem(`note-${noteData.note_id}`, JSON.stringify(updatedNote));
    }, [title, contents])

    const autoSave = async () => {
        const savedNote = JSON.parse(localStorage.getItem(`note-${noteData.note_id}`)) || {};
        const { note_id, title, contents, last_accessed, shared } = savedNote;
        

        if (messageTimer.current) clearTimeout(messageTimer.current);
        setMessage('Saving...');

        try {
            const res = await protectedClient.post(`${process.env.REACT_APP_BACKEND_URL}/notes/auto-save`, {
                'note_id': note_id,
                'title': title,
                'contents': contents,
                'last_accessed': last_accessed,
                'shared': shared
            }, { withCredentials: true });

            setOnline(true);
            messageTimer.current = setTimeout(() => setMessage('Saved'), 1000);
            setTimeout(() => setMessage(''), 3000);
        } catch (e) {
            console.log(e);
            setOnline(false);
            messageTimer.current = setTimeout(() => setMessage('Offline'), 1000);
            setTimeout(() => setMessage(''), 3000);
        }
    }

    const hardSave = async () => {
        const savedNote = JSON.parse(localStorage.getItem(`note-${noteData.note_id}`)) || {};
        const { note_id, title, contents, last_accessed, shared } = savedNote;

        try {
            const res = await protectedClient.post(`${process.env.REACT_APP_BACKEND_URL}/notes/save`, {
                'note_id': note_id,
                'title': title,
                'contents': contents,
                'last_accessed': last_accessed,
                'shared': shared
            }, { withCredentials: true });
        } catch (e) {
            console.log(e);
        }
    }

    const idleSave = () => {
        if (saveTimer.current) clearTimeout(saveTimer.current);
        saveTimer.current = setTimeout(autoSave, 3000);
    }

    useEffect(() => {
        const hideHandler = () => {
            hardSave();
            if (online) localStorage.removeItem(`note-${noteData.note_id}`);
        }

        const visibilityHandler = () => {
            if (document.visibilityState === 'hidden') {
                hardSave();
            }
        }

        const browserNavHandler = () => {
            hardSave();
            if (online) localStorage.removeItem(`note-${noteData.note_id}`);
        }

        document.addEventListener('visibilitychange', visibilityHandler);
        window.addEventListener('pagehide', hideHandler);
        window.addEventListener('popstate', browserNavHandler);
        return () => {
            setTimeout(() => {
                document.removeEventListener('visibilitychange', visibilityHandler);
                window.removeEventListener('pagehide', hideHandler);
                window.removeEventListener('popstate', browserNavHandler);
                const res = protectedClient.post(`${process.env.REACT_APP_BACKEND_URL}/notes/schedule-save`, {'note_id': noteData.note_id});
                if (online) localStorage.removeItem(`note-${noteData.note_id}`);
            }, 0)
        }
    }, [])

    return (
        <React.Fragment>
            <Box component='form' sx={{ display: 'flex', gap: 2, flexDirection: 'column' }}>
                <FormControl>
                    <FormLabel>Title</FormLabel>
                    <Stack direction='row' sx={{ flexGrow: 1 }}>
                        <TextField
                        fullWidth
                        name="title"
                        value={title}
                        onChange={(e) => {
                            setTitle(e.target.value); 
                            idleSave()
                        }}
                        />
                        <Button disabled>Add Friends</Button>
                    </Stack>
                </FormControl>
                <Card sx={{ p: 2 }}>
                    <CardContent>
                        <TextField
                        fullWidth
                        multiline
                        rows={20}
                        name="contents"
                        value={contents}
                        onChange={(e) => {
                            setContents(e.target.value);
                            idleSave()
                        }}
                        />
                    </CardContent>
                    <Stack direction='row' sx={{ width: '100%' }}>
                        <NoteSaveButton noteId={noteData.note_id}/>
                        <Typography sx={{ flexGrow: 1 }}></Typography>
                        <Typography>{message}</Typography>
                        <Typography sx={{ flexGrow: 1 }}></Typography>
                        <NoteDeleteButton noteId={noteData.note_id}/>
                    </Stack>
                </Card>
            </Box>
        </React.Fragment>
    );
}