import { Divider, Paper, Stack, Typography } from "@mui/material";
import { ArticleType } from "../types/ArticleType";
import { Link } from "react-router-dom";

export default function Article(params: {article: ArticleType}){

    return <>
        <Paper sx={{ width: "100%", height: "15%", padding: "5", backgroundColor: "#222222"}} elevation={4}>
            <Stack spacing={2} padding={5}>
                <Typography variant="h5" textAlign="left" color="white">
                    {params.article.title}
                </Typography>
                <Link to={params.article.url} >
                    <Typography textAlign="left" sx={{ color: "grey" }}>
                        {params.article.url}
                    </Typography>
                </Link>
                <Divider />
                <Typography textAlign="left" color="white">
                    Matching: {params.article.matching}
                </Typography>
            </Stack>
        </Paper>
    </>
}