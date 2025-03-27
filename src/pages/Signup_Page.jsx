// src/pages/Signup_Page.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
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
  Alert,
  Snackbar
} from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Google, Apple, Facebook, GitHub } from '@mui/icons-material';
import { Link } from 'react-router-dom';

// Create dark theme (same as Login_Page)
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
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    name: '',
    school: ''
  });
  const [errors, setErrors] = useState({});
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState('success');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error for this field when user types
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    // Email validation
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }
    
    // Password validation
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }
    
    // Confirm password validation
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }
    
    // Name validation
    if (!formData.name) {
      newErrors.name = 'Name is required';
    }
    
    // School validation
    if (!formData.school) {
      newErrors.school = 'School is required';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      // Here you would typically make an API call to register the user
      // For now, we'll just simulate a successful registration
      setSnackbarMessage('Registration successful! Redirecting to login...');
      setSnackbarSeverity('success');
      setOpenSnackbar(true);
      
      // Save user data to localStorage (as a simple example)
      const userData = {
        email: formData.email,
        name: formData.name,
        school: formData.school
      };
      localStorage.setItem('userData', JSON.stringify(userData));
      
      // Redirect to login page after a short delay
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } else {
      setSnackbarMessage('Please fix the errors in the form');
      setSnackbarSeverity('error');
      setOpenSnackbar(true);
    }
  };

  const handleSocialSignup = (provider) => {
    setSnackbarMessage(`${provider} signup not implemented yet`);
    setSnackbarSeverity('info');
    setOpenSnackbar(true);
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
            <Link to="/login" style={{ textDecoration: 'none', color: 'inherit' }}>
              <Button color="inherit">Login</Button>
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
              mb: 8,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
            }}
          >
            <Typography variant="h4" gutterBottom sx={{ mb: 4 }}>
              Sign up for Degree<span style={{ color: '#ff6b00' }}>Flow</span>🚀
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
              <form onSubmit={handleSubmit}>
                <Stack spacing={3}>
                  <TextField
                    fullWidth
                    label="Email"
                    name="email"
                    variant="outlined"
                    value={formData.email}
                    onChange={handleChange}
                    error={Boolean(errors.email)}
                    helperText={errors.email}
                  />
                  <TextField
                    fullWidth
                    label="Password"
                    name="password"
                    type="password"
                    variant="outlined"
                    value={formData.password}
                    onChange={handleChange}
                    error={Boolean(errors.password)}
                    helperText={errors.password}
                  />
                  <TextField
                    fullWidth
                    label="Confirm Password"
                    name="confirmPassword"
                    type="password"
                    variant="outlined"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    error={Boolean(errors.confirmPassword)}
                    helperText={errors.confirmPassword}
                  />
                  <TextField
                    fullWidth
                    label="Full Name"
                    name="name"
                    variant="outlined"
                    value={formData.name}
                    onChange={handleChange}
                    error={Boolean(errors.name)}
                    helperText={errors.name}
                  />
                  <TextField
                    fullWidth
                    label="School / University"
                    name="school"
                    variant="outlined"
                    value={formData.school}
                    onChange={handleChange}
                    error={Boolean(errors.school)}
                    helperText={errors.school}
                  />
                  
                  <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    sx={{ 
                      bgcolor: 'primary.main',
                      '&:hover': { bgcolor: '#ff8c00' }
                    }}
                  >
                    Create Account
                  </Button>

                  <Typography variant="body2" align="center" sx={{ mt: 2 }}>
                    Already have an account?{' '}
                    <Link to="/login" style={{ color: '#ff6b00' }}>
                      Log in
                    </Link>
                  </Typography>
                </Stack>
              </form>

              <Typography variant="body2" align="center" sx={{ mt: 3, mb: 2 }}>
                Or sign up with:
              </Typography>

              {/* Social Signup Buttons */}
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
                  onClick={() => handleSocialSignup('Google')}
                >
                  <Google sx={{ color: '#000' }} />
                </IconButton>
                <IconButton 
                  sx={{ 
                    bgcolor: 'white',
                    '&:hover': { bgcolor: '#f5f5f5' }
                  }}
                  onClick={() => handleSocialSignup('Apple')}
                >
                  <Apple sx={{ color: '#000' }} />
                </IconButton>
                <IconButton 
                  sx={{ 
                    bgcolor: 'white',
                    '&:hover': { bgcolor: '#f5f5f5' }
                  }}
                  onClick={() => handleSocialSignup('Facebook')}
                >
                  <Facebook sx={{ color: '#000' }} />
                </IconButton>
                <IconButton 
                  sx={{ 
                    bgcolor: 'white',
                    '&:hover': { bgcolor: '#f5f5f5' }
                  }}
                  onClick={() => handleSocialSignup('GitHub')}
                >
                  <GitHub sx={{ color: '#000' }} />
                </IconButton>
              </Stack>
            </Paper>
          </Box>
        </Container>

        {/* Snackbar for notifications */}
        <Snackbar
          open={openSnackbar}
          autoHideDuration={6000}
          onClose={() => setOpenSnackbar(false)}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        >
          <Alert 
            onClose={() => setOpenSnackbar(false)} 
            severity={snackbarSeverity}
            sx={{ width: '100%' }}
          >
            {snackbarMessage}
          </Alert>
        </Snackbar>
      </Box>
    </ThemeProvider>
  );
};

export default Signup_Page;