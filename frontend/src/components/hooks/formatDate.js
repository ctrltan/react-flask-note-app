
const formatDate = (date) => {
    const currentTime = new Date().getTime();
    const currentTimeSeconds = Math.floor(currentTime/1000);

    const givenDate = new Date(date).getTime();
    const givenDateSeconds = Math.floor(givenDate/1000)

    const timeDiffSeconds = currentTimeSeconds - givenDateSeconds;
    const timeDiffMinutes = Math.floor(timeDiffSeconds/60);
    const timeDiffHours = Math.floor(timeDiffMinutes/60);
    const timeDiffDays = Math.floor(timeDiffHours/24);

    if (timeDiffSeconds <= 1) {
        return 'now';
    } else if (timeDiffSeconds < 60) {
        return `${timeDiffSeconds}s ago`;
    } else if (timeDiffMinutes < 60) {
        const suffix = timeDiffMinutes === 1 ? 'minute' : 'minutes';
        return `${timeDiffMinutes} ${suffix} ago`;
    } else if (timeDiffHours < 24) {
        const suffix = timeDiffHours === 1 ? 'hour' : 'hours';
        return `${timeDiffHours} ${suffix} ago`;
    } else if (timeDiffDays < 7) {
        const suffix = timeDiffDays === 1 ? 'day' : 'days';
        return `${timeDiffDays} ${suffix} ago`;
    } else {
        const originalDate = new Date(date).toLocaleString([], {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
        return originalDate;
    }
}

export default formatDate;