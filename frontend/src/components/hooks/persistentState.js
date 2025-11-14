import { useEffect, useState } from "react";

const usePersistedState = (key) => {
    const [value, setValue] = useState(() => {
        const currValue = localStorage.getItem(key);
        
        if (currValue !== null) {
            return JSON.parse(currValue);
        } else {
            return currValue;
        }
    });

    useEffect(() => {
        if (value !== null) {
            localStorage.setItem(key, JSON.stringify(value));
        }
    }, [value, key]);
    return [value, setValue];
};

export default usePersistedState;