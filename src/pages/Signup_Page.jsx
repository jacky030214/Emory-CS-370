import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
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
  Stack,
  CircularProgress,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Google, Apple, Facebook, GitHub } from '@mui/icons-material';
import { Link } from 'react-router-dom';

// Create dark theme for consistency
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

const Signup_Page = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [userType, setUserType] = useState('student');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // API base URL
  const API_URL = 'http://127.0.0.1:8000';

  // Handle signup with the backend API
  const handleSignup = async () => {
    // Basic validation
    if (!email || !password || !username) {
      setError('Please fill in all required fields');
      return;
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters long');
      return;
    }

    try {
      setLoading(true);
      setError('');
      
      // Send signup request to FastAPI backend
      const response = await axios.post(`${API_URL}/users/create_user`, {
        email: email,
        username: username,
        password: password,
        user_type: userType
      });
      
      // If signup successful, navigate to login
      if (response.status === 201 || response.status === 200) {
        navigate('/login');
      }
    } catch (err) {
      console.error('Signup failed:', err);
      
      if (err.response) {
        if (err.response.status === 400) {
          setError('Invalid input data. Please check your information.');
        } else if (err.response.status === 409) {
          setError('Email or username already exists');
        } else {
          setError(`Error: ${err.response.data.detail || 'Signup failed'}`);
        }
      } else {
        setError('An error occurred during signup. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  // Navigate to login page
  const handleLogin = () => {
    navigate('/login');
  };

  // Handle social signup (currently just mocks the signup)
  const handleSocialSignup = (provider) => {
    setLoading(true);
    
    // In a real app, this would integrate with the social provider's OAuth
    console.log(`Signing up with ${provider}`);
    
    // Mock successful signup
    setTimeout(() => {
      navigate('/login');
    }, 1000);
  };

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
              Create your Degree<span style={{ color: '#ff6b00' }}>Flow</span> account 🎓
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
              {error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                  {error}
                </Alert>
              )}
              
              <Stack spacing={3}>
                <TextField
                  fullWidth
                  label="Email"
                  variant="outlined"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={loading}
                />
                <TextField
                  fullWidth
                  label="Username"
                  variant="outlined"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  disabled={loading}
                />
                <TextField
                  fullWidth
                  label="Password"
                  type="password"
                  variant="outlined"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={loading}
                />
                <TextField
                  fullWidth
                  label="Confirm Password"
                  type="password"
                  variant="outlined"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  disabled={loading}
                />

                <FormControl fullWidth>
                  <InputLabel>User Type</InputLabel>
                  <Select
                    value={userType}
                    label="User Type"
                    onChange={(e) => setUserType(e.target.value)}
                    disabled={loading}
                  >
                    <MenuItem value="student">Student</MenuItem>
                    <MenuItem value="professor">Professor</MenuItem>
                    <MenuItem value="admin">Administrator</MenuItem>
                  </Select>
                </FormControl>
                
                <Stack 
                  direction="row" 
                  spacing={2}
                  sx={{ mt: 2 }}
                >
                  <Button
                    fullWidth
                    variant="contained"
                    sx={{ 
                      bgcolor: 'primary.main',
                      '&:hover': { bgcolor: '#ff8a33' }
                    }}
                    onClick={handleSignup}
                    disabled={loading}
                  >
                    {loading ? <CircularProgress size={24} /> : 'Sign up'}
                  </Button>
                  <Button
                    fullWidth
                    variant="contained"
                    sx={{ 
                      bgcolor: 'rgba(255, 255, 255, 0.1)',
                      '&:hover': { bgcolor: 'rgba(255, 255, 255, 0.2)' }
                    }}
                    onClick={handleLogin}
                    disabled={loading}
                  >
                    Log in
                  </Button>
                </Stack>

                {/* Social Signup Buttons */}
                <Typography variant="body2" align="center" sx={{ mt: 2, mb: 1 }}>
                  Or sign up with
                </Typography>
                
                <Stack 
                  direction="row" 
                  spacing={2} 
                  justifyContent="center"
                >
                  <IconButton 
                    sx={{ 
                      bgcolor: 'white',
                      '&:hover': { bgcolor: '#f5f5f5' }
                    }}
                    onClick={() => handleSocialSignup('google')}
                    disabled={loading}
                  >
                    <Google sx={{ color: '#000' }} />
                  </IconButton>
                  <IconButton 
                    sx={{ 
                      bgcolor: 'white',
                      '&:hover': { bgcolor: '#f5f5f5' }
                    }}
                    onClick={() => handleSocialSignup('apple')}
                    disabled={loading}
                  >
                    <Apple sx={{ color: '#000' }} />
                  </IconButton>
                  <IconButton 
                    sx={{ 
                      bgcolor: 'white',
                      '&:hover': { bgcolor: '#f5f5f5' }
                    }}
                    onClick={() => handleSocialSignup('facebook')}
                    disabled={loading}
                  >
                    <Facebook sx={{ color: '#000' }} />
                  </IconButton>
                  <IconButton 
                    sx={{ 
                      bgcolor: 'white',
                      '&:hover': { bgcolor: '#f5f5f5' }
                    }}
                    onClick={() => handleSocialSignup('github')}
                    disabled={loading}
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

export default Signup_Page;