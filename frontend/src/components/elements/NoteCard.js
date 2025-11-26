import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import CardActions from "@mui/material/CardActions";
import Button from "@mui/material/Button";
import React from "react";

export default function NoteCard({ noteData }) {
    return (
        <React.Fragment>
            <Card variant='outlined' sx={{ width: 370 }}>
                <CardContent>
                    <Typography gutterBottom sx={{ color: 'text.secondary', fontSize: 12 }}>
                        {noteData.last_accessed}
                    </Typography>
                    <Typography variant="h5" component="div">
                        {noteData.title}
                    </Typography>
                    <Typography sx={{ color: 'text.secondary', mb: 1.5, fontSize: 14 }}>Created by {noteData.created_by}</Typography>
                    <Typography variant="body2">
                        {noteData.content}
                    </Typography>
                </CardContent>
                <CardActions>
                    <Button size="small">Edit</Button>
                </CardActions>
            </Card>
        </React.Fragment>
    )
}