import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Paper,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  Stack,
  Divider,
  List,
  ListItem,
  ListItemText,
  Switch,
  FormControlLabel,
  Snackbar
} from '@mui/material';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import ClassIcon from '@mui/icons-material/Class';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import WarningIcon from '@mui/icons-material/Warning';

const Dashboard = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [majors, setMajors] = useState(['Computer Science', 'Engineering', 'Business', 'Mathematics']);
  const [selectedMajor, setSelectedMajor] = useState('');
  const [recommendedCourses, setRecommendedCourses] = useState([]);
  const [requiredCourses, setRequiredCourses] = useState([]);
  const [availableCourses, setAvailableCourses] = useState([]);
  const [completedCourses, setCompletedCourses] = useState([]);
  const [avoidTimeConflicts, setAvoidTimeConflicts] = useState(true);
  const [requiredOnly, setRequiredOnly] = useState(true);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');

  // API base URL
  const API_URL = 'http://127.0.0.1:8000/api';

  // Check if user is logged in (temporarily disabled)
  useEffect(() => {
    // Always load sample data for development
    setCompletedCourses([
      { id: 101, code: 'CS101', title: 'Introduction to Programming' },
      { id: 102, code: 'MATH101', title: 'Calculus I' }
    ]);
    
    // Commented out login check for development
    /*
    const user = localStorage.getItem('user');
    if (!user) {
      navigate('/login');
    } else {
      // In a real app, you'd fetch the user's completed courses from the backend
      setCompletedCourses([
        { id: 101, code: 'CS101', title: 'Introduction to Programming' },
        { id: 102, code: 'MATH101', title: 'Calculus I' }
      ]);
    }
    */
  }, []);

  // Fetch major requirements when a major is selected
  useEffect(() => {
    if (!selectedMajor) return;

    const fetchRequirements = async () => {
      try {
        setLoading(true);
        setError('');
        
        // Fetch major requirements with proper API endpoint format
        const response = await axios.get(`${API_URL}/majors/requirements`, {
          params: { major_name: selectedMajor }
        });
        
        setRequiredCourses(response.data);
      } catch (err) {
        console.error('Error fetching requirements:', err);
        setError('Failed to fetch major requirements');
        
        // For demo purposes, populate with dummy data when API fails
        setRequiredCourses([
          { id: 101, code: 'CS101', title: 'Introduction to Programming' },
          { id: 201, code: 'CS201', title: 'Data Structures' },
          { id: 301, code: 'CS301', title: 'Algorithms' },
          { id: 401, code: 'CS401', title: 'Database Systems' }
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchRequirements();
  }, [selectedMajor]);

  // Fetch semester schedule when a major is selected
  useEffect(() => {
    if (!selectedMajor) return;

    const fetchSchedule = async () => {
      try {
        setLoading(true);
        setError('');
        
        // Fetch semester schedule with proper API endpoint format
        const response = await axios.get(`${API_URL}/semester/schedule`, {
          params: { major_name: selectedMajor }
        });
        
        setAvailableCourses(response.data);
      } catch (err) {
        console.error('Error fetching schedule:', err);
        setError('Failed to fetch semester schedule');
        
        // For demo purposes, populate with dummy data when API fails
        setAvailableCourses([
          {
            id: 201,
            code: 'CS201',
            title: 'Data Structures',
            description: 'Introduction to data structures and algorithms analysis.',
            credits: 3,
            schedule: { days: ['Mon', 'Wed'], time: '10:00 AM' }
          },
          {
            id: 301,
            code: 'CS301',
            title: 'Algorithms',
            description: 'Design and analysis of computer algorithms.',
            credits: 4,
            schedule: { days: ['Tue', 'Thu'], time: '1:00 PM' }
          },
          {
            id: 401,
            code: 'CS401',
            title: 'Database Systems',
            description: 'Introduction to database design and implementation.',
            credits: 3,
            schedule: { days: ['Mon', 'Wed'], time: '2:00 PM' }
          },
          {
            id: 501,
            code: 'CS501',
            title: 'Operating Systems',
            description: 'Principles of operating systems design.',
            credits: 4,
            schedule: { days: ['Tue', 'Thu'], time: '10:00 AM' }
          }
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchSchedule();
  }, [selectedMajor]);

  // Generate course recommendations when required courses or available courses change
  useEffect(() => {
    if (!requiredCourses.length || !availableCourses.length) return;

    // Improved time conflict check with actual time comparison
    const hasTimeConflict = (course, recommendedList) => {
      if (!avoidTimeConflicts) return false;
      
      // Convert time strings to comparable values (minutes since midnight)
      const parseTime = (timeStr) => {
        const [hours, minutes] = timeStr.match(/(\d+):(\d+)/).slice(1, 3);
        const isPM = timeStr.includes('PM') && hours !== '12';
        const isMidnight = timeStr.includes('AM') && hours === '12';
        return (isMidnight ? 0 : (isPM ? parseInt(hours) + 12 : parseInt(hours))) * 60 + parseInt(minutes);
      };
      
      // Assume each class is 90 minutes long
      const courseStart = parseTime(course.schedule.time);
      const courseEnd = courseStart + 90;
      
      for (const recommendedCourse of recommendedList) {
        // Check if days overlap
        const daysOverlap = course.schedule.days.some(day => 
          recommendedCourse.schedule.days.includes(day)
        );
        
        if (!daysOverlap) continue;
        
        // Check if times overlap
        const recStart = parseTime(recommendedCourse.schedule.time);
        const recEnd = recStart + 90;
        
        if ((courseStart >= recStart && courseStart < recEnd) || 
            (courseEnd > recStart && courseEnd <= recEnd) ||
            (courseStart <= recStart && courseEnd >= recEnd)) {
          return true;
        }
      }
      return false;
    };

    // Generate recommendations
    const generateRecommendations = () => {
      // Get IDs of completed courses
      const completedIds = completedCourses.map(course => course.id);
      
      // Find courses that match requirements and are available this semester
      let recommended = [];
      
      // If we only want required courses
      if (requiredOnly) {
        // Get required course IDs
        const requiredIds = requiredCourses.map(course => course.id);
        
        // Filter available courses to only include required ones
        recommended = availableCourses.filter(course => 
          requiredIds.includes(course.id) && 
          !completedIds.includes(course.id)
        );
      } else {
        // Include all available courses that haven't been completed
        recommended = availableCourses.filter(course => 
          !completedIds.includes(course.id)
        );
      }
      
      // Filter out courses with time conflicts
      if (avoidTimeConflicts) {
        const nonConflicting = [];
        
        for (const course of recommended) {
          if (!hasTimeConflict(course, nonConflicting)) {
            nonConflicting.push(course);
          }
        }
        
        recommended = nonConflicting;
      }
      
      // Sort courses by credits (prioritize higher credit courses)
      recommended.sort((a, b) => b.credits - a.credits);
      
      setRecommendedCourses(recommended);
    };

    generateRecommendations();
  }, [requiredCourses, availableCourses, completedCourses, avoidTimeConflicts, requiredOnly]);

  // Handle major selection
  const handleMajorChange = (event) => {
    setSelectedMajor(event.target.value);
  };

  // View course details
  const viewCourseDetails = async (courseId) => {
    try {
      setLoading(true);
      
      // Fetch detailed course information with proper API endpoint format
      const response = await axios.get(`${API_URL}/courses/${courseId}`);
      
      // In a real app, you'd navigate to course detail page
      console.log('Course details:', response.data);
      setSnackbarMessage(`Course details loaded for ${courseId}`);
      setSnackbarOpen(true);
      
      // Navigate to course detail page (would be implemented in a real app)
      // navigate(`/courses/${courseId}`);
    } catch (err) {
      console.error('Error fetching course details:', err);
      setError('Failed to fetch course details');
    } finally {
      setLoading(false);
    }
  };

  // Handle course selection
  const handleAddToSchedule = (course) => {
    setSnackbarMessage(`${course.code} added to your schedule`);
    setSnackbarOpen(true);
  };

  // Handle snackbar close
  const handleSnackbarClose = () => {
    setSnackbarOpen(false);
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      
      <Grid container spacing={3}>
        {/* Filters */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Filters
            </Typography>
            
            <FormControl fullWidth margin="normal">
              <InputLabel id="major-select-label">Major</InputLabel>
              <Select
                labelId="major-select-label"
                value={selectedMajor}
                label="Major"
                onChange={handleMajorChange}
                disabled={loading}
              >
                <MenuItem value="">
                  <em>Select a major</em>
                </MenuItem>
                {majors.map((major) => (
                  <MenuItem key={major} value={major}>
                    {major}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            
            <Box sx={{ mt: 2 }}>
              <FormControlLabel
                control={
                  <Switch
                    checked={requiredOnly}
                    onChange={(e) => setRequiredOnly(e.target.checked)}
                    color="primary"
                  />
                }
                label="Required courses only"
              />
            </Box>
            
            <Box sx={{ mt: 1 }}>
              <FormControlLabel
                control={
                  <Switch
                    checked={avoidTimeConflicts}
                    onChange={(e) => setAvoidTimeConflicts(e.target.checked)}
                    color="primary"
                  />
                }
                label="Avoid schedule conflicts"
              />
            </Box>
            
            <Divider sx={{ my: 2 }} />
            
            <Typography variant="subtitle1" gutterBottom>
              Completed Courses
            </Typography>
            
            <List dense>
              {completedCourses.map((course) => (
                <ListItem key={course.id}>
                  <CheckCircleIcon color="success" sx={{ mr: 1 }} />
                  <ListItemText
                    primary={course.code}
                    secondary={course.title}
                  />
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
        
        {/* Recommendations */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2, minHeight: 240 }}>
            <Typography variant="h6" gutterBottom>
              Recommended Courses
              {selectedMajor && ` for ${selectedMajor}`}
            </Typography>
            
            {loading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', py: 3 }}>
                <CircularProgress />
              </Box>
            ) : recommendedCourses.length > 0 ? (
              <Grid container spacing={2}>
                {recommendedCourses.map((course) => (
                  <Grid item xs={12} key={course.id}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="h6" component="div">
                          {course.code}: {course.title}
                        </Typography>
                        
                        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                          {course.description}
                        </Typography>
                        
                        <Stack direction="row" spacing={1} sx={{ mt: 2 }}>
                          <Chip 
                            icon={<ClassIcon />} 
                            label={`${course.credits} credits`} 
                            size="small" 
                            color="primary" 
                            variant="outlined"
                          />
                          
                          <Chip 
                            icon={<AccessTimeIcon />} 
                            label={`${course.schedule.days.join(', ')} at ${course.schedule.time}`} 
                            size="small" 
                            color="secondary" 
                            variant="outlined"
                          />
                          
                          {requiredCourses.some(req => req.id === course.id) && (
                            <Chip 
                              label="Required" 
                              size="small" 
                              color="success" 
                            />
                          )}
                        </Stack>
                      </CardContent>
                      
                      <CardActions>
                        <Button size="small" onClick={() => viewCourseDetails(course.id)}>
                          View Details
                        </Button>
                        <Button size="small" color="primary" onClick={() => handleAddToSchedule(course)}>
                          Add to Schedule
                        </Button>
                      </CardActions>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            ) : selectedMajor ? (
              <Box sx={{ p: 3, textAlign: 'center' }}>
                <WarningIcon color="warning" sx={{ fontSize: 40, mb: 1 }} />
                <Typography>
                  No recommended courses found. Please adjust your filters or check if you've completed all requirements.
                </Typography>
              </Box>
            ) : (
              <Box sx={{ p: 3, textAlign: 'center' }}>
                <Typography>
                  Select a major to see course recommendations.
                </Typography>
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>
      
      <Snackbar
        open={snackbarOpen}
        autoHideDuration={4000}
        onClose={handleSnackbarClose}
        message={snackbarMessage}
      />
    </Container>
  );
};

export default Dashboard;