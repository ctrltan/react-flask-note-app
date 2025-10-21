
import { useEffect, useState } from 'react';
import axios from 'axios';

export default function HomePage() {
    const [apiData, setApiData] = useState('');

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
        </div>
    );
}