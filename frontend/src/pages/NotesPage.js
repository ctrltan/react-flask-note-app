import { useContext, useEffect, useState } from "react";
import { UserContext } from "../App";
import axios from "axios";
import { protectedClient } from "../components/wrappers/ProtectedRoute";
import SideBar from "../components/elements/SideBar";



export default function NotesPage() {
    const [notes, setNotes] = useState(null);
    const [message, setMessage] = useState('');
    const {user, setUser} = useContext(UserContext);
    
    useEffect(() => {
        const retrieveNotes = async () => {
            try {
                const res = await protectedClient.get(`${process.env.REACT_APP_BACKEND_URL}/notes`, null, { withCredentials: true });
                console.log(res.data.message);
                if (typeof res.data.message === 'string') {
                    setMessage(res.data.message);
                    return;
                }

                if (Object.keys(notes).length > 0) {
                    setNotes(res.data.message);
                }
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
        - add note button
    */
    
    return (
        <div>
            <p>{notes ? notes : null}</p>
            <p>{message}</p>
            <SideBar />
        </div>
    )

}