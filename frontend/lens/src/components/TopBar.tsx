import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import { LinearGradient } from 'react-text-gradients';
import { GiSpectacleLenses } from "react-icons/gi";


export default function TopBar() {
    return (
        <AppBar position="fixed" sx={{ background: "black" }}>
            <Toolbar>
                <IconButton
                    size="large"
                    edge="start"
                    color="info"
                    href="/"
                >
                    <GiSpectacleLenses color='pink' />
                </IconButton>
                <Typography
                    variant="h6"
                    noWrap
                    component="a"
                    href="/"
                    sx={{
                        display: { xs: 'none', md: 'flex' },
                        fontFamily: 'monospace',
                        fontWeight: 700,
                        letterSpacing: '.3rem',
                        color: 'inherit',
                        textDecoration: 'none',
                    }}
                >
                    <LinearGradient gradient={['to left', '#b0e3ff ,#ff99e6']}>Lens</LinearGradient>
                </Typography>
            </Toolbar>
        </AppBar>
    );
}