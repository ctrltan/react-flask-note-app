import { useEffect } from "react"

const noteSubmit = () => {
    console.log("Form works")
}

const NoteForm = () => {
    return (
        <form action={noteSubmit}>
            <input name="title"/>
            <input name="contents" />
            <button type="submit">Create</button>
        </form>
    );
}

export default NoteForm;