import { useEffect } from "react";
import React from "react";
import { useNavigate } from "react-router-dom"
import slugifyTitle from "../hooks/slugifyTitle";
import Button from "@mui/material/Button";


export default function NoteEditButton({ noteId, noteTitle }) {
    const nav = useNavigate();

    const navEditPage = () => {
        const slugTitle = slugifyTitle(noteTitle);

        nav(`/notes/${noteId}/${slugTitle}`);
    }

    return (
        <React.Fragment>
            <Button size="small" onClick={navEditPage}>Edit</Button>
        </React.Fragment>
    )
}