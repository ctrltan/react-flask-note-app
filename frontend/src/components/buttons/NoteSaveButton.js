import Button from "@mui/material/Button";
import { protectedClient } from "../wrappers/ProtectedRoute";
import { useState } from "react";
import MoreHorizRoundedIcon from '@mui/icons-material/MoreHorizRounded';
import { useRef } from "react";
import React from "react";


function LoadingIcon() {
    return (
        <React.Fragment>
            <MoreHorizRoundedIcon />
        </React.Fragment>
    )
}


export default function NoteSaveButton({ noteId }) {
    const [saving, setSaving] = useState('Save');
    const [btnDisable, setBtnDisable] = useState(false);
    const saveTimer = useRef(null);

    const save = async () => {
            const savedNote = JSON.parse(localStorage.getItem(`note-${noteId}`)) || {};
            const { note_id, title, contents, last_accessed, shared } = savedNote;

            if (saveTimer.current) clearTimeout(saveTimer.current);
            setBtnDisable(true);
            setSaving(LoadingIcon);
    
            try {
                const res = await protectedClient.post(`${process.env.REACT_APP_BACKEND_URL}/notes/save`, {
                    'note_id': note_id,
                    'title': title,
                    'contents': contents,
                    'last_accessed': last_accessed,
                    'shared': shared
                }, { withCredentials: true });

                saveTimer.current = setTimeout(() => setSaving('Saved'), 2000);
                setTimeout(() => {setSaving('Save'); setBtnDisable(false)}, 1000);
            } catch (e) {
                console.log(e);
                saveTimer.current = setTimeout(() => setSaving('Offline'), 2000);
                setTimeout(() => {setSaving('Save'); setBtnDisable(false)}, 1000);
            }
        }

    return (
        <React.Fragment>
            <Button size="small" onClick={save} disabled={btnDisable}>{saving}</Button>
        </React.Fragment>
    )
}