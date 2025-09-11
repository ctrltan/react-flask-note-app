import { useEffect } from "react"

function noteSubmit() {
    console.log("Form works")
}

export default function NoteForm() {
    return (
        <form action={noteSubmit}>
            <input name="title"/>
            <input name="contents" />
            <button type="submit">Create</button>
        </form>
    );
}
