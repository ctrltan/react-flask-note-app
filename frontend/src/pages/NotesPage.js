import { useContext, useEffect, useState } from "react";
import { UserContext } from "../App";
import axios from "axios";
import { protectedClient } from "../components/wrappers/ProtectedRoute";
import LogoutButton from "../components/buttons/LogoutButton";


export default function NotesPage() {
    const [notes, setNotes] = useState(null);
    const [message, setMessage] = useState('');
    const {user, setUser} = useContext(UserContext);

    //retrieve all user notes from the database and display them
    
    useEffect(() => {
        const retrieveNotes = async () => {
            try {
                const res = await protectedClient.get(`${process.env.REACT_APP_BACKEND_URL}/notes`, null, { withCredentials: true });
                console.log(res.data.message);
                if (typeof res.data.message === 'string') {
                    setMessage(res.data.message);
                    return;
                }

                setNotes(res.data.message);
            } catch(e) {
                console.log(e)
            }
        }
        retrieveNotes();
    }, [])

    /*components: 
        - side navbar with user
        - note block component to view notes -> clickable notes
        - search bar for notes
    */
    
    return (
        <div>
            
            <p>{message}</p>
            <LogoutButton />
        </div>
    )

}