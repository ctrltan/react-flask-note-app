import { useEffect, useState } from "react";

const usePersistedState = (key) => {
    const [value, setValue] = useState(() => {
        const currValue = localStorage.getItem(key);
        
        if (currValue) {
            return JSON.parse(currValue);
        } else {
            return currValue;
        }
    });

    useEffect(() => {
        localStorage.setItem(key, JSON.stringify(value));
    }, [value, key]);
    return [value, setValue];
};

export default usePersistedState;