import axios from 'axios';
import { useEffect, useState } from 'react';

export default function HomePage() {
    const [apiData, setApiData] = useState('');

    useEffect(() => {
        const getData = async () => {
            const response = await axios.get('http://127.0.0.1:8000/');
            setApiData(response.data.message);
        }

        getData();
    }, []);

    return (
        <div>
            <header>{apiData}</header>
        </div>
    );
}