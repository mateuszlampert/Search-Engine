import { FormControl, InputLabel, Input, IconButton, Stack, Typography } from "@mui/material";
import { useState } from "react";
import SearchIcon from '@mui/icons-material/Search';
import { ArticleType } from "../types/ArticleType";
import ArticlesList from "./ArticlesList";
import TopBar from "./TopBar";
import { LinearGradient } from "react-text-gradients";
import { GiSpectacleLenses } from "react-icons/gi";

export default function SearchPage() {
    const [phrase, setPhrase] = useState<string>()
    const [data, setData] = useState<ArticleType[]>();

    const handleSearch = async () => {
        try {
            const request = await fetch(`http://127.0.0.1:5000/search`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 'phrase': phrase })
            });

            const response = await request.json();
            
            setData(response.results)
            console.log(response)
        }
        catch (error) {
            console.log(`Error occured: ${error}`);
        }

    }
    return <>
        <TopBar />
        <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100%"}}>
            <div style={{ width: "60%", height: "100%", padding: "5%" }}>
                <Stack spacing={4}>
                    <div style={{ display: "flex", justifyContent: "center" }}>
                        <IconButton href="/" >
                            <GiSpectacleLenses color='pink' size="10vw"/>
                        </IconButton>
                    </div>
                    <FormControl fullWidth>
                        <InputLabel>
                            <Typography
                                variant="h6"
                                noWrap
                                component="a"
                                href="/"
                                sx={{
                                    display: { xs: 'none', md: 'flex' },
                                    fontFamily: 'monospace',
                                    fontWeight: 700,
                                    color: 'inherit',
                                    textDecoration: 'none',
                                }}
                            >
                                <LinearGradient gradient={['to left', '#b0e3ff ,#ff99e6']}>What are we researching today?...</LinearGradient>
                            </Typography>
                        </InputLabel>
                        <Input
                            fullWidth
                            endAdornment={
                                <IconButton color="primary" onClick={handleSearch} disabled={phrase === undefined || phrase.length === 0}>
                                    <SearchIcon />
                                </IconButton>
                            }
                            onChange={e => setPhrase(e.target.value)}
                            style={{color: "white"}}
                        />
                    </FormControl>
                    {data && <ArticlesList articles={data} />}
                </Stack>
            </div>
        </div>
    </>
}