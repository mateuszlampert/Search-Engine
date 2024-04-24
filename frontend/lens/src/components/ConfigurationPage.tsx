import { Button, Divider, FormControlLabel, Paper, Slider, Stack, Switch, Typography } from "@mui/material";
import { useState } from "react"
import SearchIcon from '@mui/icons-material/Search';
import { Link } from "react-router-dom";
import TopBar from "./TopBar";
import { LinearGradient } from 'react-text-gradients'


export default function ConfigurationPanel() {
    const [articlesToShow, setArticlesToShow] = useState<number>(10);
    const [svd, setSVD] = useState<boolean>(true);
    const [idf, setIDF] = useState<boolean>(true);

    const handleInitialize = async () => {
        try {
            const request = await fetch(`http://127.0.0.1:5000/initialize`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 'no_articles' : articlesToShow, 'svd' : svd, 'idf' : idf })
            });

            const response = await request.json();
            
            console.log(response)
        }
        catch (error) {
            console.log(`Error occured: ${error}`);
        }
    }

    return <>
        <TopBar />
        <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh"}}>
            <Paper style={{ width: "60%", padding: "5%", backgroundColor: "#111111"}} elevation={21}>
                <Stack spacing={4}>
                    <Typography textAlign="center" variant="h5" color="white">
                        Configure your <LinearGradient gradient={['to left', '#17acff ,#ff68f0']}>Lens</LinearGradient> engine below
                    </Typography>

                    <Divider />

                    <Typography textAlign="center" variant="h6" color="white">
                        Enter number of articles you want to get
                    </Typography>

                    <Slider defaultValue={10} min={5} max={20} valueLabelDisplay="auto" onChange={(_, newValue) => {
                        if (typeof newValue === 'number') {
                            setArticlesToShow(newValue);
                        }
                    }} />

                    <Typography textAlign="center" variant="h6" color="white">
                        Choose features you want to use during browsing
                    </Typography>

                    <Stack direction="row" spacing={4} sx={{display: "flex", justifyContent: "center"}}>
                        <FormControlLabel
                            control={
                                <Switch
                                    checked={svd}
                                    onChange={(event) => {
                                        setSVD(event.target.checked)
                                        console.log(svd);
                                    }}
                                    size="medium"
                                />
                            }
                            label="SVD"
                            sx={{color: "white"}}
                        />
                        <FormControlLabel
                            control={
                                <Switch
                                    checked={idf}
                                    onChange={event => { setIDF(event.target.checked) }}
                                    size="medium"
                                />
                            }
                            label="IDF"
                            sx={{ color: "white" }}
                        />
                    </Stack>
                    <Link to={`/searchx/${articlesToShow}/${svd}/${idf}`} >
                        <Button onClick={handleInitialize} variant="contained" endIcon={<SearchIcon />}>
                            Browse
                        </Button>
                    </Link>
                </Stack>
            </Paper>
        </div>
    </>;
}