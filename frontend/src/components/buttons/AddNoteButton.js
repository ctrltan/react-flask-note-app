import React from "react";
import Button from "@mui/material/Button";
import AddCircleOutlineRoundedIcon from '@mui/icons-material/AddCircleOutlineRounded';
import Stack from "@mui/material/Stack";


export default function AddNoteButton() {
    const addNote = async () => {

    }
    return (
        <React.Fragment>
            <Button size="large" onClick={addNote}>
                <Stack direction='row' sx={{ gap: 1 }}>
                    <AddCircleOutlineRoundedIcon/>
                    New Note
                </Stack>
            </Button>
        </React.Fragment>
    )
}