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
      { 
        id: 170, 
        code: 'CS170', 
        title: 'Introduction to Programming'
      },
      { 
        id: 111, 
        code: 'MATH111', 
        title: 'Calculus I'
      }
    ]);
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
          { 
            id: 170, 
            code: 'CS170', 
            title: 'Introduction To Computer Science I',
            description: 'First course in computer science programming sequence.',
            credits: 4,
            schedule: { days: ['Tue', 'Thu'], time: '11:00 AM' }
          },
          { 
            id: 171, 
            code: 'CS171', 
            title: 'Introduction to Computer Science II',
            description: 'Second course in computer science programming sequence.',
            credits: 4,
            schedule: { days: ['Mon', 'Wed'], time: '1:00 PM' }
          },
          { 
            id: 190, 
            code: 'CS190', 
            title: 'Fresh Seminar: Computer Science',
            description: 'Seminar focusing on AI impact in education.',
            credits: 1,
            schedule: { days: ['Fri'], time: '10:00 AM' }
          },
          { 
            id: 211, 
            code: 'CS211', 
            title: 'Introduction to Artificial Intelligence',
            description: 'Basic concepts and techniques in artificial intelligence.',
            credits: 3,
            schedule: { days: ['Mon', 'Wed'], time: '11:00 AM' }
          },
          { 
            id: 224, 
            code: 'CS224', 
            title: 'Foundations of Computer Science',
            description: 'Mathematical foundations of computer science.',
            credits: 3,
            schedule: { days: ['Tue', 'Thu'], time: '9:00 AM' }
          },
          { 
            id: 253, 
            code: 'CS253', 
            title: 'Data Structures and Algorithms',
            description: 'Fundamental data structures and algorithm analysis.',
            credits: 4,
            schedule: { days: ['Tue', 'Thu'], time: '2:00 PM' }
          }
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
            id: 171,
            code: 'CS171',
            title: 'Introduction to Computer Science II',
            description: 'Second course in computer science programming sequence.',
            credits: 4,
            schedule: { days: ['Mon', 'Wed'], time: '1:00 PM' }
          },
          {
            id: 211,
            code: 'CS211',
            title: 'Introduction to Artificial Intelligence',
            description: 'Basic concepts and techniques in artificial intelligence.',
            credits: 3,
            schedule: { days: ['Mon', 'Wed'], time: '11:00 AM' }
          },
          {
            id: 224,
            code: 'CS224',
            title: 'Foundations of Computer Science',
            description: 'Mathematical foundations of computer science.',
            credits: 3,
            schedule: { days: ['Tue', 'Thu'], time: '9:00 AM' }
          },
          {
            id: 253,
            code: 'CS253',
            title: 'Data Structures and Algorithms',
            description: 'Fundamental data structures and algorithm analysis.',
            credits: 4,
            schedule: { days: ['Tue', 'Thu'], time: '2:00 PM' }
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
    // 디버깅용 콘솔 로그
    console.log("Recommendation useEffect triggered");
    console.log("Required courses length:", requiredCourses.length);
    console.log("Available courses length:", availableCourses.length);
    
    // 중요 변경: 더 이상 requiredCourses와 availableCourses 길이 검사에 의존하지 않음
    // 이 경우 어느 한쪽이 빈 배열이라도 진행할 수 있음
    if (selectedMajor === '') return;

    // Improved time conflict check with actual time comparison
    const hasTimeConflict = (course, recommendedList) => {
      if (!avoidTimeConflicts) return false;
      
      // 일정 정보가 없는 경우 충돌 없음으로 처리
      if (!course.schedule || !course.schedule.time || !course.schedule.days) {
        return false;
      }
      
      // Convert time strings to comparable values (minutes since midnight)
      const parseTime = (timeStr) => {
        if (!timeStr) return 0;
        
        const match = timeStr.match(/(\d+):(\d+)/);
        if (!match) return 0;
        
        const [hours, minutes] = match.slice(1, 3);
        const isPM = timeStr.includes('PM') && hours !== '12';
        const isMidnight = timeStr.includes('AM') && hours === '12';
        return (isMidnight ? 0 : (isPM ? parseInt(hours) + 12 : parseInt(hours))) * 60 + parseInt(minutes);
      };
      
      // Assume each class is 90 minutes long
      const courseStart = parseTime(course.schedule.time);
      const courseEnd = courseStart + 90;
      
      for (const recommendedCourse of recommendedList) {
        // Check if the recommended course has schedule info
        if (!recommendedCourse.schedule || !recommendedCourse.schedule.time || !recommendedCourse.schedule.days) {
          continue;
        }
        
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
      console.log("Completed course IDs:", completedIds);
      
      // Find courses that match requirements and are available this semester
      let recommended = [];
      
      // If we only want required courses
      if (requiredOnly) {
        // Get required course IDs
        const requiredIds = requiredCourses.map(course => course.id);
        console.log("Required course IDs:", requiredIds);
        
        // Filter available courses to only include required ones
        recommended = availableCourses.filter(course => {
          const isRequired = requiredIds.includes(course.id);
          const isCompleted = completedIds.includes(course.id);
          console.log(`Course ${course.code}: isRequired=${isRequired}, isCompleted=${isCompleted}`);
          return isRequired && !isCompleted;
        });
      } else {
        // Include all available courses that haven't been completed
        recommended = availableCourses.filter(course => 
          !completedIds.includes(course.id)
        );
      }
      
      console.log("Initial recommended courses:", recommended.map(c => c.code));
      
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
      recommended.sort((a, b) => (b.credits || 0) - (a.credits || 0));
      
      console.log("Final recommended courses:", recommended.map(c => c.code));
      setRecommendedCourses(recommended);
    };

    generateRecommendations();
  }, [requiredCourses, availableCourses, completedCourses, avoidTimeConflicts, requiredOnly, selectedMajor]);

  // Handle major selection
  const handleMajorChange = (event) => {
    const major = event.target.value;
    console.log("Selected major:", major);
    setSelectedMajor(major);
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
                          {course.description || 'No description available.'}
                        </Typography>
                        
                        <Stack direction="row" spacing={1} sx={{ mt: 2 }}>
                          {course.credits && (
                            <Chip 
                              icon={<ClassIcon />} 
                              label={`${course.credits} credits`} 
                              size="small" 
                              color="primary" 
                              variant="outlined"
                            />
                          )}
                          
                          {course.schedule && course.schedule.days && (
                            <Chip 
                              icon={<AccessTimeIcon />} 
                              label={`${course.schedule.days.join(', ')} at ${course.schedule.time}`} 
                              size="small" 
                              color="secondary" 
                              variant="outlined"
                            />
                          )}
                          
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