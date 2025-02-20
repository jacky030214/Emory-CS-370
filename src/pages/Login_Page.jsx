import React from 'react';
import {
  Box,
  Button,
  TextField,
  Typography,
  IconButton,
  AppBar,
  Toolbar,
  Container,
  Paper,
  Stack
} from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Google, Apple, Facebook, GitHub } from '@mui/icons-material';
import { Link } from 'react-router-dom';

// Create dark theme
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#ff6b00', // Orange color for Flow
    },
    background: {
      default: '#1a1a2e',
      paper: '#1a1a2e',
    },
  },
});

const Login_Page = () => {
  return (
    <ThemeProvider theme={darkTheme}>
      <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
        {/* Header */}
        <AppBar position="static" color="transparent" elevation={0}>
          <Toolbar>
            <Link 
              to="/" 
              style={{ textDecoration: 'none', color: 'inherit' }}
            >
              <Button 
                color="inherit" 
                sx={{ 
                  fontSize: '24px', 
                  textTransform: 'none',
                  '& .flow': { color: 'primary.main' }
                }}
              >
                Degree<span className="flow">Flow</span>
              </Button>
            </Link>
            <Box sx={{ flexGrow: 1 }} />
            <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
              <Button color="inherit">Home</Button>
            </Link>
            <Link to="/settings" style={{ textDecoration: 'none', color: 'inherit' }}>
              <Button color="inherit">Settings</Button>
            </Link>
            <Link to="/profile" style={{ textDecoration: 'none', color: 'inherit' }}>
              <Button color="inherit">Profile</Button>
            </Link>
            <Link to="/help" style={{ textDecoration: 'none', color: 'inherit' }}>
              <Button color="inherit">Help</Button>
            </Link>
          </Toolbar>
        </AppBar>

        {/* Main Content */}
        <Container maxWidth="sm">
          <Box
            sx={{
              mt: 8,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <Typography variant="h4" gutterBottom sx={{ mb: 4 }}>
              Boost your degree with Degree<span style={{ color: '#ff6b00' }}>Flow</span>🚀
            </Typography>

            <Paper 
              elevation={3}
              sx={{
                p: 4,
                width: '100%',
                bgcolor: 'rgba(255, 255, 255, 0.05)',
                borderRadius: 2
              }}
            >
              <Stack spacing={3}>
                <TextField
                  fullWidth
                  label="Email"
                  variant="outlined"
                />
                <TextField
                  fullWidth
                  label="Password"
                  type="password"
                  variant="outlined"
                />
                <Stack 
                  direction="row" 
                  spacing={2}
                  sx={{ mt: 2 }}
                >
                  <Button
                    fullWidth
                    variant="contained"
                    sx={{ 
                      bgcolor: 'rgba(255, 255, 255, 0.1)',
                      '&:hover': { bgcolor: 'rgba(255, 255, 255, 0.2)' }
                    }}
                  >
                    Log in
                  </Button>
                  <Button
                    fullWidth
                    variant="contained"
                    sx={{ 
                      bgcolor: 'rgba(255, 255, 255, 0.1)',
                      '&:hover': { bgcolor: 'rgba(255, 255, 255, 0.2)' }
                    }}
                  >
                    Sign up
                  </Button>
                </Stack>

                {/* Social Login Buttons */}
                <Stack 
                  direction="row" 
                  spacing={2} 
                  justifyContent="center"
                  sx={{ mt: 2 }}
                >
                  <IconButton 
                    sx={{ 
                      bgcolor: 'white',
                      '&:hover': { bgcolor: '#f5f5f5' }
                    }}
                  >
                    <Google sx={{ color: '#000' }} />
                  </IconButton>
                  <IconButton 
                    sx={{ 
                      bgcolor: 'white',
                      '&:hover': { bgcolor: '#f5f5f5' }
                    }}
                  >
                    <Apple sx={{ color: '#000' }} />
                  </IconButton>
                  <IconButton 
                    sx={{ 
                      bgcolor: 'white',
                      '&:hover': { bgcolor: '#f5f5f5' }
                    }}
                  >
                    <Facebook sx={{ color: '#000' }} />
                  </IconButton>
                  <IconButton 
                    sx={{ 
                      bgcolor: 'white',
                      '&:hover': { bgcolor: '#f5f5f5' }
                    }}
                  >
                    <GitHub sx={{ color: '#000' }} />
                  </IconButton>
                </Stack>
              </Stack>
            </Paper>
          </Box>
        </Container>
      </Box>
    </ThemeProvider>
  );
};

export default Login_Page;