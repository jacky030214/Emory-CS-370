import React, { useState, useEffect } from 'react';
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
  createTheme,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Snackbar,
  Alert,
  CircularProgress
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import AddIcon from '@mui/icons-material/Add';
import DeleteIcon from '@mui/icons-material/Delete';
import { CourseAPI, UserAPI } from '../services/api'; // Updated import for API services

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
  const [user, setUser] = useState(null);
  const [anchorEl, setAnchorEl] = useState(null);
  const [classes, setClasses] = useState([]);
  const [availableCourses, setAvailableCourses] = useState([]);
  const [requiredCourses, setRequiredCourses] = useState([]);
  const [electiveCourses, setElectiveCourses] = useState([]);
  const [professors, setProfessors] = useState([]);
  const [selectedProfessor, setSelectedProfessor] = useState('');
  const [selectedSemester, setSelectedSemester] = useState('');
  const [majors, setMajors] = useState([
    'Computer Science', 'Information Technology', 'Software Engineering', 
    'Data Science', 'Cybersecurity', 'Business Administration'
  ]);
  const [selectedMajor, setSelectedMajor] = useState('');
  const [semesters, setSemesters] = useState([
    'Fall 2025', 'Spring 2026', 'Summer 2026', 'Fall 2026', 'Spring 2027'
  ]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedCourse, setSelectedCourse] = useState('');

  // Load user info
  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
      const parsedUser = JSON.parse(userData);
      setUser(parsedUser);
      
      // Get user details from API if needed
      const fetchUserDetails = async () => {
        try {
          if (parsedUser.id) {
            const userDetails = await UserAPI.getUserById(parsedUser.id);
            // Update with additional user details if needed
            console.log('User details fetched:', userDetails);
          }
        } catch (err) {
          console.error('Failed to fetch user details:', err);
        }
      };
      
      fetchUserDetails();
    } else {
      // Redirect non-logged in users to login page
      navigate('/login');
    }
  }, [navigate]);

  // Load courses and professors
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch courses
        const courses = await CourseAPI.getAllCourses();
        
        // Filter required and elective courses
        const required = courses.filter(course => course.is_required);
        const electives = courses.filter(course => !course.is_required);
        
        setAvailableCourses(courses);
        setRequiredCourses(required);
        setElectiveCourses(electives);
        
        // Fetch professors
        const professorData = await ProfessorAPI.getAllProfessors();
        setProfessors(professorData);
        
        // Fetch majors (if you have an API endpoint for it)
        // const majorData = await MajorAPI.getAllMajors();
        // setMajors(majorData);
        
      } catch (err) {
        console.error('Failed to load data:', err);
        setError('Failed to load data');
        setOpenSnackbar(true);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    // Remove user info from local storage on logout
    localStorage.removeItem('user');
    navigate('/login');
  };

  const handleOpenAddClassDialog = () => {
    setOpenDialog(true);
  };

  const handleCloseAddClassDialog = () => {
    setOpenDialog(false);
    setSelectedCourse('');
  };

  const handleAddClass = () => {
    if (!selectedCourse) {
      setError('Please select a course');
      setOpenSnackbar(true);
      return;
    }

    const selectedCourseObj = availableCourses.find(
      course => `${course.code} - ${course.name}` === selectedCourse
    );

    if (selectedCourseObj) {
      // Check for duplicates
      const isDuplicate = classes.some(cls => cls.id === selectedCourseObj.id);
      
      if (!isDuplicate) {
        setClasses([
          ...classes, 
          { 
            id: selectedCourseObj.id, 
            name: `${selectedCourseObj.code} - ${selectedCourseObj.name}`, 
            credits: selectedCourseObj.credits 
          }
        ]);
        
        // Show success message
        setError('Course added successfully');
        setOpenSnackbar(true);
      } else {
        setError('Course already added');
        setOpenSnackbar(true);
      }
    }
    
    handleCloseAddClassDialog();
  };

  const handleRemoveClass = (classId) => {
    setClasses(classes.filter(cls => cls.id !== classId));
  };

  const handleCloseSnackbar = () => {
    setOpenSnackbar(false);
  };

  // Function to save schedule to backend (would need to be implemented in API)
  const handleSaveSchedule = async () => {
    try {
      setLoading(true);
      // This would need to be implemented in our API
      // const response = await CourseAPI.saveUserSchedule({
      //   userId: user.id,
      //   semester: startingSemester,
      //   courses: classes.map(cls => cls.id)
      // });
      
      setError('Schedule saved successfully');
      setOpenSnackbar(true);
    } catch (err) {
      console.error('Failed to save schedule:', err);
      setError('Failed to save schedule');
      setOpenSnackbar(true);
    } finally {
      setLoading(false);
    }
  };

  // Show nothing if not logged in (will redirect)
  if (!user && !loading) return null;

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
              Settings
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
              <MenuItem onClick={() => navigate('/profile')}>
                Profile {user && `(${user.username})`}
              </MenuItem>
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
              <MenuIcon sx={{ mr: 1 }} /> Dashboard 📂
            </Typography>
            
            <Grid container spacing={2} sx={{ mt: 3, mb: 2 }}>
              <Grid item xs={12} md={3}>
                <TextField
                  select
                  label="Select Semester"
                  fullWidth
                  value={selectedSemester}
                  onChange={(e) => setSelectedSemester(e.target.value)}
                  variant="outlined"
                  size="small"
                  sx={{ 
                    input: { color: 'white' },
                    '& .MuiOutlinedInput-root': {
                      '& fieldset': {
                        borderColor: 'rgba(255, 255, 255, 0.3)',
                      },
                      '&:hover fieldset': {
                        borderColor: 'rgba(255, 255, 255, 0.5)',
                      },
                    },
                    '& .MuiInputLabel-root': {
                      color: 'rgba(255, 255, 255, 0.7)',
                    },
                    '& .MuiSelect-select': {
                      color: 'white',
                    }
                  }}
                >
                  {semesters.map((semester) => (
                    <MenuItem key={semester} value={semester}>
                      {semester}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              
              <Grid item xs={12} md={3}>
                <TextField
                  select
                  label="Filter by Professor"
                  fullWidth
                  value={selectedProfessor}
                  onChange={(e) => setSelectedProfessor(e.target.value)}
                  variant="outlined"
                  size="small"
                  sx={{ 
                    input: { color: 'white' },
                    '& .MuiOutlinedInput-root': {
                      '& fieldset': {
                        borderColor: 'rgba(255, 255, 255, 0.3)',
                      },
                      '&:hover fieldset': {
                        borderColor: 'rgba(255, 255, 255, 0.5)',
                      },
                    },
                    '& .MuiInputLabel-root': {
                      color: 'rgba(255, 255, 255, 0.7)',
                    },
                    '& .MuiSelect-select': {
                      color: 'white',
                    }
                  }}
                >
                  <MenuItem value="">Davide Fossati</MenuItem>
                  <MenuItem value="">Steven La Fleur</MenuItem>
                  <MenuItem value="">Jinho Choi</MenuItem>
                  <MenuItem value="">Fei Liu</MenuItem>
                  {professors.map((professor) => (
                    <MenuItem key={professor.id} value={professor.id}>
                      {professor.name}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              
              <Grid item xs={12} md={3}>
                <TextField
                  select
                  label="Select Major"
                  fullWidth
                  value={selectedMajor}
                  onChange={(e) => setSelectedMajor(e.target.value)}
                  variant="outlined"
                  size="small"
                  sx={{ 
                    input: { color: 'white' },
                    '& .MuiOutlinedInput-root': {
                      '& fieldset': {
                        borderColor: 'rgba(255, 255, 255, 0.3)',
                      },
                      '&:hover fieldset': {
                        borderColor: 'rgba(255, 255, 255, 0.5)',
                      },
                    },
                    '& .MuiInputLabel-root': {
                      color: 'rgba(255, 255, 255, 0.7)',
                    },
                    '& .MuiSelect-select': {
                      color: 'white',
                    }
                  }}
                >
                  <MenuItem value="">All Majors</MenuItem>
                  {majors.map((major) => (
                    <MenuItem key={major} value={major}>
                      {major}
                    </MenuItem>
                  ))}
                </TextField>
              </Grid>
              
              <Grid item xs={12} md={3}>
                <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handleOpenAddClassDialog}
                    startIcon={<AddIcon />}
                    sx={{ height: '40px' }}
                  >
                    Add Course
                  </Button>
                </Box>
              </Grid>
            </Grid>
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
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <div>
                    <Typography variant="h6" sx={{ color: 'white' }}>
                      {selectedSemester || 'Current Semester'}
                    </Typography>
                    <Typography variant="subtitle2" sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
                      (Credit Hours)
                    </Typography>
                  </div>
                </Box>
                
                {loading ? (
                  <Box sx={{ display: 'flex', justifyContent: 'center', my: 3 }}>
                    <CircularProgress />
                  </Box>
                ) : (
                  <List>
                    {classes.length > 0 ? (
                      classes.map((cls) => (
                        <ListItem 
                          key={cls.id}
                          sx={{ 
                            p: 1, 
                            mb: 1, 
                            bgcolor: 'rgba(255, 255, 255, 0.03)',
                            border: '1px solid rgba(255, 255, 255, 0.1)',
                            borderRadius: 1,
                            display: 'flex',
                            justifyContent: 'space-between'
                          }}
                        >
                          <Typography sx={{ color: 'white', flexGrow: 1 }}>
                            {cls.name}
                          </Typography>
                          <Typography sx={{ color: 'rgba(255, 255, 255, 0.7)', mx: 2 }}>
                            {cls.credits} credits
                          </Typography>
                          <IconButton 
                            size="small" 
                            onClick={() => handleRemoveClass(cls.id)}
                            sx={{ color: 'rgba(255, 0, 0, 0.7)' }}
                          >
                            <DeleteIcon fontSize="small" />
                          </IconButton>
                        </ListItem>
                      ))
                    ) : (
                      <Typography sx={{ color: 'rgba(255, 255, 255, 0.5)', textAlign: 'center', my: 3 }}>
                        No courses added yet
                      </Typography>
                    )}
                  </List>
                )}
                
                {classes.length > 0 && (
                  <Box sx={{ mt: 2, p: 1, bgcolor: 'rgba(255, 255, 255, 0.05)', borderRadius: 1 }}>
                    <Typography sx={{ color: 'white', textAlign: 'right' }}>
                      Total Credits: {classes.reduce((sum, cls) => sum + cls.credits, 0)} credits
                    </Typography>
                  </Box>
                )}
                
                {classes.length > 0 && (
                  <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
                    <Button 
                      variant="contained" 
                      color="primary" 
                      onClick={handleSaveSchedule}
                      disabled={loading}
                    >
                      {loading ? <CircularProgress size={24} /> : 'Save Schedule'}
                    </Button>
                  </Box>
                )}
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
                    Required Classes
                  </Typography>
                  {loading ? (
                    <Box sx={{ display: 'flex', justifyContent: 'center', my: 2 }}>
                      <CircularProgress size={24} />
                    </Box>
                  ) : (
                    <List sx={{ maxHeight: '200px', overflow: 'auto' }}>
                      {requiredCourses.length > 0 ? (
                        requiredCourses.map((course) => (
                          <ListItem 
                            key={course.id}
                            sx={{ 
                              p: 1, 
                              mb: 1, 
                              bgcolor: 'rgba(255, 255, 255, 0.03)',
                              border: '1px solid rgba(255, 255, 255, 0.1)',
                              borderRadius: 1
                            }}
                          >
                            <Typography sx={{ color: 'white', fontSize: '0.9rem' }}>
                              {course.code} - {course.name} ({course.credits} credits)
                            </Typography>
                          </ListItem>
                        ))
                      ) : (
                        <Typography sx={{ color: 'rgba(255, 255, 255, 0.5)', textAlign: 'center' }}>
                          No required courses found
                        </Typography>
                      )}
                    </List>
                  )}
                </Box>
                
                <Box sx={{ p: 2, border: '1px dashed rgba(255, 255, 255, 0.3)' }}>
                  <Typography variant="h6" sx={{ color: 'white', mb: 2 }}>
                    Elective Classes
                  </Typography>
                  {loading ? (
                    <Box sx={{ display: 'flex', justifyContent: 'center', my: 2 }}>
                      <CircularProgress size={24} />
                    </Box>
                  ) : (
                    <List sx={{ maxHeight: '200px', overflow: 'auto' }}>
                      {electiveCourses.length > 0 ? (
                        electiveCourses.map((course) => (
                          <ListItem 
                            key={course.id}
                            sx={{ 
                              p: 1, 
                              mb: 1, 
                              bgcolor: 'rgba(255, 255, 255, 0.03)',
                              border: '1px solid rgba(255, 255, 255, 0.1)',
                              borderRadius: 1
                            }}
                          >
                            <Typography sx={{ color: 'white', fontSize: '0.9rem' }}>
                              {course.code} - {course.name} ({course.credits} credits)
                            </Typography>
                          </ListItem>
                        ))
                      ) : (
                        <Typography sx={{ color: 'rgba(255, 255, 255, 0.5)', textAlign: 'center' }}>
                          No elective courses found
                        </Typography>
                      )}
                    </List>
                  )}
                </Box>
              </Paper>
            </Grid>
          </Grid>
        </Container>

        {/* Add Course Dialog */}
        <Dialog open={openDialog} onClose={handleCloseAddClassDialog}>
          <DialogTitle>Add Course</DialogTitle>
          <DialogContent>
            <TextField
              select
              label="Select Course"
              fullWidth
              value={selectedCourse}
              onChange={(e) => setSelectedCourse(e.target.value)}
              margin="normal"
            >
              {availableCourses
                .filter(course => 
                  (!selectedProfessor || course.professor_id === selectedProfessor) && 
                  (!selectedMajor || course.major === selectedMajor)
                )
                .map(course => (
                  <MenuItem key={course.id} value={`${course.code} - ${course.name}`}>
                    {course.code} - {course.name} ({course.credits} credits)
                  </MenuItem>
                ))
              }
            </TextField>
            
            <TextField
              select
              label="Assign to Semester"
              fullWidth
              value={selectedSemester}
              onChange={(e) => setSelectedSemester(e.target.value)}
              margin="normal"
            >
              {semesters.map(semester => (
                <MenuItem key={semester} value={semester}>
                  {semester}
                </MenuItem>
              ))}
            </TextField>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseAddClassDialog}>Cancel</Button>
            <Button onClick={handleAddClass} color="primary">Add</Button>
          </DialogActions>
        </Dialog>

        {/* Notification message */}
        <Snackbar
          open={openSnackbar}
          autoHideDuration={6000}
          onClose={handleCloseSnackbar}
          anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        >
          <Alert 
            onClose={handleCloseSnackbar} 
            severity={error.includes('success') ? 'success' : 'error'} 
            sx={{ width: '100%' }}
          >
            {error}
          </Alert>
        </Snackbar>
      </Box>
    </ThemeProvider>
  );
}

export default Dashboard_Page;