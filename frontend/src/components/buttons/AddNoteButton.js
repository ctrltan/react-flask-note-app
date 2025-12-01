import React from "react";
import Button from "@mui/material/Button";
import AddCircleOutlineRoundedIcon from '@mui/icons-material/AddCircleOutlineRounded';
import Stack from "@mui/material/Stack";
import { protectedClient } from "../wrappers/ProtectedRoute";
import { useNavigate } from "react-router-dom";


export default function AddNoteButton() {
    const nav = useNavigate();

    const addNote = async () => {
        /*
        Get the new note data and navigate to edit that note specifically
        Create a hook that takes note id and retrieves the note then allows editing so editing logic is not repeated
        */
        nav('/notes/new-note');
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