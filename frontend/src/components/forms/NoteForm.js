import Box from "@mui/material/Box";
import FormControl from "@mui/material/FormControl";
import FormLabel from "@mui/material/FormLabel";
import TextField from "@mui/material/TextField";
import { useEffect, useState } from "react"
import React from "react";

const noteSubmit = () => {
    console.log("Form works")
}

export default function NoteForm({ noteData }) {
    const [title, setTitle] = useState(() => {
        if (!noteData?.note_id) return '';
        const noteId = noteData.note_id;
        return JSON.parse(localStorage.getItem(`note-${noteId}`))?.title || '';
    });
    const [contents, setContents] = useState(() => {
        if (!noteData?.note_id) return '';
        const noteId = noteData.note_id;
        return JSON.parse(localStorage.getItem(`note-${noteId}`))?.contents || '';
    });

    useEffect(() => {
        console.log(noteData);
        if (!noteData?.note_id) return;
        const noteId = noteData.note_id;

        const updatedNote = {
            'title': title,
            'contents': contents,
            'last_accessed': new Date().toISOString()
        }
        localStorage.setItem(`note-${noteId}`, JSON.stringify(updatedNote));
    }, [])

    return (
        <React.Fragment>
            <Box component='form' sx={{ display: 'flex', gap: 2 }}>
                <FormControl>
                    <FormLabel>Title</FormLabel>
                    <TextField
                    fullWidth
                    name="title"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    />
                </FormControl>
            </Box>
        </React.Fragment>
    );
}