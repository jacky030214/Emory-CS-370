import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  AppBar,
  Toolbar,
  Button,
  Paper,
  Grid,
  TextField,
  Divider,
  IconButton,
  Menu,
  MenuItem,
  List,
  ListItem,
  ThemeProvider,
  createTheme
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import AddIcon from '@mui/icons-material/Add';

// Create dark theme matching Login_Page
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

function Dashboard_Page() {
  const navigate = useNavigate();
  const [anchorEl, setAnchorEl] = useState(null);
  const [major, setMajor] = useState('');
  const [startingSemester, setStartingSemester] = useState('ex) Fall 2025');
  const [classes, setClasses] = useState([
    { id: 1, name: 'Class 1', credits: 3 },
    { id: 2, name: 'Class 2', credits: 3 },
    { id: 3, name: 'Class 3', credits: 3 }
  ]);

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    navigate('/login');
  };

  const handleAddClass = () => {
    const newId = classes.length > 0 ? Math.max(...classes.map(c => c.id)) + 1 : 1;
    setClasses([...classes, { id: newId, name: `Class ${newId}`, credits: 3 }]);
  };
  
  return (
    <ThemeProvider theme={darkTheme}>
      <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
        {/* App Bar, top of the page */}
        <AppBar position="static" color="transparent" elevation={5}>
          <Toolbar>
            <Button 
              color="inherit" 
              sx={{ 
                fontSize: '20px', 
                textTransform: 'none',
                '& .flow': { color: 'primary.main' }
              }}
              onClick={() => navigate('/login')}
            >
              Degree<span className="flow">Flow</span>
            </Button>
            
            <Box sx={{ flexGrow: 1 }} />
            
            <Button 
              color="inherit"
              onClick={() => navigate('/home')}
              sx={{ marginRight: 2 }}
            >
              Home
            </Button>
            
            <Button 
              color="inherit"
              onClick={() => navigate('/settings')}
              sx={{ marginRight: 2 }}
            >
              Setting
            </Button>
            
            <IconButton
              color="inherit"
              onClick={handleMenuOpen}
            >
              <MenuIcon />
            </IconButton>
            
            <Menu
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={handleMenuClose}
            >
              <MenuItem onClick={() => navigate('/profile')}>Profile</MenuItem>
              <MenuItem onClick={handleLogout}>Log Out</MenuItem>
            </Menu>
          </Toolbar>
        </AppBar>

        {/* Main Content */}
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
          <Box sx={{ mb: 4 }}>
            <Typography variant="h4" gutterBottom sx={{ 
              display: 'flex',
              alignItems: 'center',
              color: 'white'
            }}>
              <MenuIcon sx={{ mr: 1 }} /> College Schedule by Semester
            </Typography>
            
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2, mt: 3 }}>
              <Typography variant="h6" sx={{ mr: 2, color: 'white' }}>
                Your Major:
              </Typography>
              <TextField 
                value={major}
                onChange={(e) => setMajor(e.target.value)}
                variant="outlined"
                size="small"
                sx={{ 
                  width: 200,
                  input: { color: 'white' },
                  '& .MuiOutlinedInput-root': {
                    '& fieldset': {
                      borderColor: 'rgba(255, 255, 255, 0.3)',
                    },
                    '&:hover fieldset': {
                      borderColor: 'rgba(255, 255, 255, 0.5)',
                    },
                  }
                }}
              />
              
              <Typography variant="h6" sx={{ mx: 2, color: 'white' }}>
                Starting Semester:
              </Typography>
              <TextField 
                value={startingSemester}
                variant="outlined"
                size="small"
                sx={{ 
                  width: 150,
                  input: { color: 'white' },
                  bgcolor: 'primary.main',
                  '& .MuiOutlinedInput-root': {
                    '& fieldset': {
                      borderColor: 'primary.main',
                    },
                  }
                }}
              />
            </Box>
          </Box>
          
          <Divider sx={{ mb: 3, bgcolor: 'rgba(255, 255, 255, 0.12)' }} />
          
          <Grid container spacing={3}>
            {/* Semester course list */}
            <Grid item xs={12} md={6}>
              <Paper
                sx={{
                  p: 2,
                  borderRadius: 1,
                  bgcolor: 'rgba(255, 255, 255, 0.05)',
                  border: '1px solid rgba(255, 255, 255, 0.12)'
                }}
              >
                <Typography variant="h6" sx={{ color: 'white', mb: 1 }}>
                  2025 Fall
                </Typography>
                <Typography variant="subtitle2" sx={{ color: 'rgba(255, 255, 255, 0.7)', mb: 2 }}>
                  (Credit Hours)
                </Typography>
                
                <List>
                  {classes.map((cls) => (
                    <ListItem 
                      key={cls.id}
                      sx={{ 
                        p: 1, 
                        mb: 1, 
                        bgcolor: 'rgba(255, 255, 255, 0.03)',
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                        borderRadius: 1
                      }}
                    >
                      <Typography sx={{ color: 'white' }}>
                        {cls.name}
                      </Typography>
                    </ListItem>
                  ))}
                  <Box 
                    sx={{ 
                      display: 'flex', 
                      justifyContent: 'center', 
                      mt: 2,
                      color: 'rgba(255, 255, 255, 0.5)'
                    }}
                  >
                    <Typography>⋮</Typography>
                  </Box>
                </List>
              </Paper>
            </Grid>
            
            {/* Required and Elective classes */}
            <Grid item xs={12} md={6}>
              <Paper
                sx={{
                  p: 2,
                  borderRadius: 1,
                  bgcolor: 'rgba(255, 255, 255, 0.05)',
                  border: '1px solid rgba(255, 255, 255, 0.12)',
                  height: '100%'
                }}
              >
                <Box sx={{ p: 2, border: '1px dashed rgba(255, 255, 255, 0.3)', mb: 4 }}>
                  <Typography variant="h6" sx={{ color: 'white', mb: 2 }}>
                    Required Classes data required
                  </Typography>
                  <Box sx={{ height: 80 }} /> {/* Placeholder for content */}
                </Box>
                
                <Box sx={{ p: 2, border: '1px dashed rgba(255, 255, 255, 0.3)' }}>
                  <Typography variant="h6" sx={{ color: 'white', mb: 2 }}>
                    Elective Classes data required
                  </Typography>
                  <Box sx={{ height: 80 }} /> {/* Placeholder for content */}
                </Box>
              </Paper>
            </Grid>
          </Grid>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default Dashboard_Page;