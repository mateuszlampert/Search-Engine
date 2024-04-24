import { Stack } from "@mui/material";
import { ArticleType } from "../types/ArticleType";
import Article from "./Article";

export default function ArticlesList(params: { articles: ArticleType[] }) {
    return <>
        <Stack spacing={4}>
            {params.articles.map((item, _) => (
                <Article article={item} />
            ))}
        </Stack>
    </>
}