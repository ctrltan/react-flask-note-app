import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import DeleteOutlineRoundedIcon from '@mui/icons-material/DeleteOutlineRounded';
import { protectedClient } from "../wrappers/ProtectedRoute";
import React from "react";


export default function NoteDeleteButton({ noteId }) {
    const [open, setOpen] = useState(false);
    const nav = useNavigate();

    const dialogOpen = () => {
        if (document.activeElement) document.activeElement.blur();
        setOpen(true);
    }

    const dialogClose = () => {
        setOpen(false);
    }

    const deleteNote = async () => {
            try {
                const res = await protectedClient.delete(`${process.env.REACT_APP_BACKEND_URL}/notes/delete`, {
                    params: {
                        'note_id': noteId
                    }
                }, { withCredentials: true });

                localStorage.removeItem(`note-${noteId}`);
                nav('/notes');
            } catch (e) {
                console.log(e);
            }
        }

    return (
        <React.Fragment>
            <Button size="small" onClick={dialogOpen} color="warning">
                <DeleteOutlineRoundedIcon/>
            </Button>
            <Dialog open={open} onClose={dialogClose}>
                <DialogTitle>Delete Note</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        Are you sure you want to delete this note?
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button size="small" color="warning" onClick={deleteNote}>Delete</Button>
                    <Button size="small" color="info" onClick={dialogClose}>Cancel</Button>
                </DialogActions>
            </Dialog>
        </React.Fragment>
    )
}