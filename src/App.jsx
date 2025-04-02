import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate, useNavigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { 
  CssBaseline, 
  Button, 
  AppBar, 
  Toolbar, 
  Box, 
  IconButton, 
  Avatar, 
  Menu, 
  MenuItem, 
  Divider, 
  ListItemIcon,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Typography
} from '@mui/material';
import { 
  Menu as MenuIcon, 
  Dashboard as DashboardIcon, 
  School as SchoolIcon,
  Person as PersonIcon,
  Logout as LogoutIcon,
  Settings as SettingsIcon
} from '@mui/icons-material';

import Dashboard from './pages/Dashboard';
import LoginPage from './pages/Login_Page';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Create theme for consistent styling
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#ff6b00', // Orange color for branding
    },
    secondary: {
      main: '#03a9f4', // Light blue for secondary actions
    },
    background: {
      default: '#1a1a2e',
      paper: '#1a1a2e',
    },
  },
  typography: {
    fontFamily: "'Roboto', 'Helvetica', 'Arial', sans-serif",
    h4: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 500,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 8,
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: 8,
        },
      },
    },
  },
});

// Protected route component
const ProtectedRoute = ({ children }) => {
  const isAuthenticated = localStorage.getItem('user') !== null;
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
};

// NavMenu component for the drawer and header
const NavMenu = ({ mobileView = false, onClose = null }) => {
  const navigate = useNavigate();
  
  const handleNavigation = (path) => {
    navigate(path);
    if (onClose) onClose();
  };
  
  return (
    <List>
      <ListItem disablePadding>
        <ListItemButton onClick={() => handleNavigation('/dashboard')}>
          <ListItemIcon>
            <DashboardIcon />
          </ListItemIcon>
          <ListItemText primary="Dashboard" />
        </ListItemButton>
      </ListItem>
      <ListItem disablePadding>
        <ListItemButton onClick={() => handleNavigation('/courses')}>
          <ListItemIcon>
            <SchoolIcon />
          </ListItemIcon>
          <ListItemText primary="Courses" />
        </ListItemButton>
      </ListItem>
      <ListItem disablePadding>
        <ListItemButton onClick={() => handleNavigation('/schedule')}>
          <ListItemIcon>
            <SchoolIcon />
          </ListItemIcon>
          <ListItemText primary="Schedule" />
        </ListItemButton>
      </ListItem>
    </List>
  );
};

// Main App component
const App = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [user, setUser] = useState(null);
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);
  
  // Check if user is logged in on app load
  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser));
      } catch (error) {
        // Handle invalid stored user data
        localStorage.removeItem('user');
      }
    }
  }, []);
  
  // Handle drawer toggle
  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };
  
  // Handle profile menu open
  const handleProfileMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };
  
  // Handle profile menu close
  const handleProfileMenuClose = () => {
    setAnchorEl(null);
  };
  
  // Handle logout
  const handleLogout = () => {
    localStorage.removeItem('user');
    setUser(null);
    handleProfileMenuClose();
    // Use navigation instead of direct window.location manipulation
    window.location.href = '/login'; // Simple approach for logout
  };
  
  // Drawer width
  const drawerWidth = 240;
  
  // Drawer content
  const drawer = (
    <Box onClick={handleDrawerToggle} sx={{ textAlign: 'center' }}>
      <Box sx={{ my: 2 }}>
        <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
          <Button 
            color="inherit" 
            sx={{ 
              fontSize: '20px', 
              textTransform: 'none',
              '& .flow': { color: 'primary.main' }
            }}
          >
            Degree<span className="flow">Flow</span>
          </Button>
        </Link>
      </Box>
      <Divider />
      <NavMenu mobileView={true} onClose={handleDrawerToggle} />
    </Box>
  );

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
          {/* App Bar */}
          <AppBar position="sticky" color="default" elevation={1}>
            <Toolbar>
              {user && (
                <IconButton
                  color="inherit"
                  aria-label="open drawer"
                  edge="start"
                  onClick={handleDrawerToggle}
                  sx={{ mr: 2, display: { sm: 'none' } }}
                >
                  <MenuIcon />
                </IconButton>
              )}
              
              <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
                <Button 
                  color="inherit" 
                  sx={{ 
                    fontSize: { xs: '18px', sm: '24px' }, 
                    textTransform: 'none',
                    '& .flow': { color: 'primary.main' }
                  }}
                >
                  Degree<span className="flow">Flow</span>
                </Button>
              </Link>
              
              <Box sx={{ flexGrow: 1 }} />
              
              {user ? (
                <>
                  <Box sx={{ display: { xs: 'none', sm: 'flex' } }}>
                    <Button 
                      color="inherit" 
                      component={Link} 
                      to="/dashboard" 
                      startIcon={<DashboardIcon />}
                    >
                      Dashboard
                    </Button>
                    <Button 
                      color="inherit" 
                      component={Link} 
                      to="/courses" 
                      startIcon={<SchoolIcon />}
                    >
                      Courses
                    </Button>
                    <Button 
                      color="inherit" 
                      component={Link} 
                      to="/schedule" 
                      startIcon={<SchoolIcon />}
                    >
                      Schedule
                    </Button>
                  </Box>
                  
                  <IconButton
                    onClick={handleProfileMenuOpen}
                    size="small"
                    sx={{ ml: 2 }}
                    aria-controls={open ? 'account-menu' : undefined}
                    aria-haspopup="true"
                    aria-expanded={open ? 'true' : undefined}
                  >
                    <Avatar sx={{ width: 32, height: 32, bgcolor: 'primary.main' }}>
                      {user.username ? user.username[0].toUpperCase() : user.email ? user.email[0].toUpperCase() : 'U'}
                    </Avatar>
                  </IconButton>
                  
                  <Menu
                    anchorEl={anchorEl}
                    id="account-menu"
                    open={open}
                    onClose={handleProfileMenuClose}
                    onClick={handleProfileMenuClose}
                    PaperProps={{
                      elevation: 0,
                      sx: {
                        overflow: 'visible',
                        filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',
                        mt: 1.5,
                        '& .MuiAvatar-root': {
                          width: 32,
                          height: 32,
                          ml: -0.5,
                          mr: 1,
                        },
                      },
                    }}
                    transformOrigin={{ horizontal: 'right', vertical: 'top' }}
                    anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
                  >
                    <MenuItem component={Link} to="/profile">
                      <ListItemIcon>
                        <PersonIcon fontSize="small" />
                      </ListItemIcon>
                      Profile
                    </MenuItem>
                    <MenuItem component={Link} to="/settings">
                      <ListItemIcon>
                        <SettingsIcon fontSize="small" />
                      </ListItemIcon>
                      Settings
                    </MenuItem>
                    <Divider />
                    <MenuItem onClick={handleLogout}>
                      <ListItemIcon>
                        <LogoutIcon fontSize="small" />
                      </ListItemIcon>
                      Logout
                    </MenuItem>
                  </Menu>
                </>
              ) : (
                <Button 
                  color="primary" 
                  variant="contained" 
                  component={Link} 
                  to="/login"
                >
                  Login
                </Button>
              )}
            </Toolbar>
          </AppBar>
          
          {/* Responsive drawer for mobile navigation */}
          <Box component="nav">
            <Drawer
              variant="temporary"
              open={mobileOpen}
              onClose={handleDrawerToggle}
              ModalProps={{
                keepMounted: true, // Better mobile performance
              }}
              sx={{
                display: { xs: 'block', sm: 'none' },
                '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
              }}
            >
              {drawer}
            </Drawer>
          </Box>

          {/* Main content */}
          <Box component="main" sx={{ flexGrow: 1 }}>
            <Routes>
              {/* Public routes */}
              <Route path="/login" element={<LoginPage />} />
              
              {/* Protected routes */}
              <Route path="/" element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } />
              <Route path="/dashboard" element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } />
              
              <Route path="/schedule" element={
                <ProtectedRoute>
                  <Box p={4}>
                    <Typography variant="h4" gutterBottom>
                      Semester Schedule
                    </Typography>
                    <SchedulePage />
                  </Box>
                </ProtectedRoute>
              } />
              
              {/* Future routes would be added here */}
              <Route path="/courses" element={
                <ProtectedRoute>
                  <Box p={4} textAlign="center">
                    <Typography variant="h4" gutterBottom>
                      Available Courses
                    </Typography>
                    <CourseListPage />
                  </Box>
                </ProtectedRoute>
              } />
              <Route path="/profile" element={
                <ProtectedRoute>
                  <Box p={4} textAlign="center">
                    Profile page coming soon.
                  </Box>
                </ProtectedRoute>
              } />
              <Route path="/settings" element={
                <ProtectedRoute>
                  <Box p={4} textAlign="center">
                    Settings page coming soon.
                  </Box>
                </ProtectedRoute>
              } />
            </Routes>
          </Box>

          {/* Footer */}
          <Box 
            component="footer" 
            sx={{ 
              py: 2, 
              bgcolor: 'rgba(0, 0, 0, 0.2)', 
              textAlign: 'center',
              mt: 'auto'
            }}
          >
            <Box sx={{ color: 'text.secondary', fontSize: '0.875rem' }}>
              &copy; {new Date().getFullYear()} DegreeFlow University Management System
            </Box>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
};

const SchedulePage = () => {
  const [majorName, setMajorName] = useState("Bachelor of Arts in Mathematics");
  const [scheduleData, setScheduleData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSchedule = async () => {
      try {
        setLoading(true);
        const response = await api.get(`/get_semester_schedule_by_major_name?major_name=${majorName}&startingSem=Fall&startingYear=2023`);
        setScheduleData(response.data);
        setLoading(false);
      } catch (err) {
        console.error("Error fetching schedule:", err);
        setError("Failed to load schedule data");
        setLoading(false);
      }
    };

    fetchSchedule();
  }, [majorName]);

  if (loading) return <div>Loading schedule...</div>;
  if (error) return <div>Error: {error}</div>;

  return (
    <div>
      {Array.isArray(scheduleData) ? (
        scheduleData.map((semester, index) => (
          <Box key={index} sx={{ mb: 3, p: 2, bgcolor: 'background.paper', borderRadius: 1 }}>
            <Typography variant="h6">
              {semester.semester} {semester.year} - {semester.total_credit_hours} Credits
            </Typography>
            {semester.classes && semester.classes.length > 0 ? (
              <Box sx={{ mt: 2 }}>
                {semester.classes.map((course, courseIndex) => (
                  <Box key={courseIndex} sx={{ mb: 1, p: 1, borderLeft: '3px solid', borderColor: 'primary.main' }}>
                    <Typography variant="subtitle1">
                      {course.class_name} ({course.class_id})
                    </Typography>
                    <Typography variant="body2">
                      {course.credit_hours} credits | {course.professor || 'TBA'}
                    </Typography>
                  </Box>
                ))}
              </Box>
            ) : (
              <Typography variant="body2">No classes for this semester</Typography>
            )}
          </Box>
        ))
      ) : (
        <Typography>No schedule data available</Typography>
      )}
    </div>
  );
};

const CourseListPage = () => {
  return (
    <div>
      <Typography variant="body1">
        Course list will be displayed here. This would fetch data from the courses endpoints.
      </Typography>
    </div>
  );
};

export default App;