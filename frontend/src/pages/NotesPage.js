import { useContext, useEffect, useState } from "react";
import { UserContext } from "../App";
import axios from "axios";


export default function NotesPage() {
    const [notes, setNotes] = useState(null);
    const [message, setMessage] = useState('');
    const {user, setUser} = useContext(UserContext);

    //retrieve all user notes from the database and display them
    
    useEffect(async () => {
        try {
            res = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/notes`, null, { withCredentials: true });
            
            if (typeof res.data.message === 'string') {
                setMessage(res.data.message);
                return;
            }

            setNotes(res.data.message);
        } catch(e) {
            console.log(e)
        }
    }, [])

    /*components: 
        - side navbar with user
        - note block component to view notes -> clickable notes
        - search bar for notes
    */


}