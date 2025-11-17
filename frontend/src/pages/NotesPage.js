import { useContext } from "react";
import { UserContext } from "../App";


export default function NotesPage() {
    const {user, setUser} = useContext(UserContext);

    //retrieve all user notes from the database and display them
    /*needs: 
        - side navbar with folders
        - note block component to view notes
    */
}