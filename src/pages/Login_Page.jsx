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
  Alert
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

const Login_Page = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  // API base URL
  const API_URL = 'http://127.0.0.1:8000';

  // Handle login with the backend API
  const handleLogin = async () => {
    // Basic validation
    if (!email || !password) {
      setError('Please enter both email and password');
      return;
    }

    try {
      setLoading(true);
      setError('');
      
      // 수정: FastAPI users 라우트에 맞게 로그인 엔드포인트 수정
      const response = await axios.post(`${API_URL}/users/login`, {
        email: email,
        input_pass: password  // 수정: FastAPI 백엔드의 파라미터명(input_pass)에 맞게 변경
      });
      
      // Store user info in localStorage
      const userInfo = response.data;
      localStorage.setItem('user', JSON.stringify(userInfo));
      
      // Redirect to dashboard
      navigate('/dashboard');
    } catch (err) {
      console.error('Login failed:', err);
      
      if (err.response) {
        // 수정: FastAPI 오류 응답 처리
        if (err.response.status === 401) {
          setError('Invalid password');
        } else if (err.response.status === 404) {
          setError('User not found with this email');
        } else {
          setError(`Error: ${err.response.data.detail || 'Login failed'}`);
        }
      } else {
        setError('An error occurred during login. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  // Navigate to signup page
  const handleSignup = () => {
    navigate('/signup');
  };

  // Handle social login (currently just mocks the login)
  const handleSocialLogin = (provider) => {
    setLoading(true);
    
    // In a real app, this would integrate with the social provider's OAuth
    console.log(`Logging in with ${provider}`);
    
    // Mock successful login
    setTimeout(() => {
      const userInfo = {
        id: 1,
        username: 'user',
        email: 'user@example.com',
        provider: provider
      };
      
      localStorage.setItem('user', JSON.stringify(userInfo));
      navigate('/dashboard');
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
                  label="Password"
                  type="password"
                  variant="outlined"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={loading}
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
                    onClick={handleLogin}
                    disabled={loading}
                  >
                    {loading ? <CircularProgress size={24} /> : 'Log in'}
                  </Button>
                  <Button
                    fullWidth
                    variant="contained"
                    sx={{ 
                      bgcolor: 'rgba(255, 255, 255, 0.1)',
                      '&:hover': { bgcolor: 'rgba(255, 255, 255, 0.2)' }
                    }}
                    onClick={handleSignup}
                    disabled={loading}
                  >
                    Sign up
                  </Button>
                </Stack>

                {/* Social Login Buttons */}
                <Typography variant="body2" align="center" sx={{ mt: 2, mb: 1 }}>
                  Or continue with
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
                    onClick={() => handleSocialLogin('google')}
                    disabled={loading}
                  >
                    <Google sx={{ color: '#000' }} />
                  </IconButton>
                  <IconButton 
                    sx={{ 
                      bgcolor: 'white',
                      '&:hover': { bgcolor: '#f5f5f5' }
                    }}
                    onClick={() => handleSocialLogin('apple')}
                    disabled={loading}
                  >
                    <Apple sx={{ color: '#000' }} />
                  </IconButton>
                  <IconButton 
                    sx={{ 
                      bgcolor: 'white',
                      '&:hover': { bgcolor: '#f5f5f5' }
                    }}
                    onClick={() => handleSocialLogin('facebook')}
                    disabled={loading}
                  >
                    <Facebook sx={{ color: '#000' }} />
                  </IconButton>
                  <IconButton 
                    sx={{ 
                      bgcolor: 'white',
                      '&:hover': { bgcolor: '#f5f5f5' }
                    }}
                    onClick={() => handleSocialLogin('github')}
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

export default Login_Page;