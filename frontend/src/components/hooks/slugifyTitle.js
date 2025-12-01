
const slugifyTitle = (title) => {
    const slugTitle = title.toLowerCase().trim().replace(/[^a-z0-9\s-]/g, '').replace(/\s+/g, '-').replace(/-+/g, '-');
    
    return slugTitle;
};

export default slugifyTitle;