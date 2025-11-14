
import { useContext, useEffect, useState } from 'react';
import axios from 'axios';
import { UserContext } from '../App';
import LogoutButton from '../components/buttons/LogoutButton';

export default function HomePage() {
    const [apiData, setApiData] = useState('');
    const {user, setUser} = useContext(UserContext);

    useEffect(() => {
        const getData = async () => {
            const response = await axios.get(process.env.REACT_APP_BACKEND_URL);
            setApiData(response.data.message);
        }

        getData();
    }, []);

    return (
        <div>
            <header data-testid='api'>{apiData}</header>
            {user ? <h2>Hello {user.username}</h2> : null}
            {user ? <LogoutButton/> : null}
        </div>
    );
}