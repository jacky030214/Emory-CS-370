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
  const [majors, setMajors] = useState([]);
  const [selectedMajor, setSelectedMajor] = useState('');
  const [recommendedCourses, setRecommendedCourses] = useState([]);
  const [requiredCourses, setRequiredCourses] = useState([]);
  const [availableCourses, setAvailableCourses] = useState([]);
  const [completedCourses, setCompletedCourses] = useState([]);
  const [avoidTimeConflicts, setAvoidTimeConflicts] = useState(true);
  const [requiredOnly, setRequiredOnly] = useState(true);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');

  // ✅ Correct FastAPI Base URL
  const API_URL = 'http://127.0.0.1:8000';

  // Fetch available majors from the backend
  useEffect(() => {
    const fetchMajors = async () => {
      try {
        setLoading(true);
        setError('');
        
        const response = await axios.get(`${API_URL}/majors`);
        
        // Assuming the response returns an array of major objects
        // If the structure is different, adjust accordingly
        setMajors(response.data);
      } catch (err) {
        console.error('Error fetching majors:', err);
        setError('Failed to fetch majors list');
        // Fall back to hardcoded majors if API call fails
        setMajors(['Computer Science', 'Engineering', 'Business', 'Mathematics']);
      } finally {
        setLoading(false);
      }
    };

    fetchMajors();
  }, []);

  // Load sample completed courses for development
  useEffect(() => {
    setCompletedCourses([
      { id: 170, code: 'CS170', title: 'Introduction to Programming' },
      { id: 111, code: 'MATH111', title: 'Calculus I' }
    ]);
  }, []);

  // ✅ Fetch Major Requirements (Fixed Endpoint & Params)
  useEffect(() => {
    if (!selectedMajor) return;

    const fetchRequirements = async () => {
      try {
        setLoading(true);
        setError('');
        
        const response = await axios.get(`${API_URL}/get_major_requirement_by_major_name`, {
          params: { major: selectedMajor }
        });

        setRequiredCourses(response.data);
      } catch (err) {
        console.error('Error fetching requirements:', err);
        setError('Failed to fetch major requirements');
      } finally {
        setLoading(false);
      }
    };

    fetchRequirements();
  }, [selectedMajor]);

  // ✅ Fetch Semester Schedule (Fixed Endpoint & Params)
  useEffect(() => {
    if (!selectedMajor) return;

    const fetchSchedule = async () => {
      try {
        setLoading(true);
        setError('');

        const response = await axios.get(`${API_URL}/get_semester_schedule_by_major_name`, {
          params: { major: selectedMajor }
        });

        setAvailableCourses(response.data);
      } catch (err) {
        console.error('Error fetching schedule:', err);
        setError('Failed to fetch semester schedule');
      } finally {
        setLoading(false);
      }
    };

    fetchSchedule();
  }, [selectedMajor]);

  // ✅ Fetch Course Details (Correct API Call)
  const viewCourseDetails = async (courseId) => {
    try {
      setLoading(true);
      
      const response = await axios.get(`${API_URL}/courses/${courseId}`);
      
      console.log('Course details:', response.data);
      setSnackbarMessage(`Course details loaded for ${courseId}`);
      setSnackbarOpen(true);
      
    } catch (err) {
      console.error('Error fetching course details:', err);
      setError('Failed to fetch course details');
    } finally {
      setLoading(false);
    }
  };

  // Handle Major Selection
  const handleMajorChange = (event) => {
    setSelectedMajor(event.target.value);
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
                  <MenuItem key={typeof major === 'object' ? major.id : major} value={typeof major === 'object' ? major.name : major}>
                    {typeof major === 'object' ? major.name : major}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Paper>
        </Grid>
        
        {/* Recommendations */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2, minHeight: 240 }}>
            <Typography variant="h6" gutterBottom>
              Recommended Courses {selectedMajor && `for ${selectedMajor}`}
            </Typography>
            
            {loading ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', py: 3 }}>
                <CircularProgress />
              </Box>
            ) : requiredCourses.length > 0 ? (
              <Grid container spacing={2}>
                {requiredCourses.map((course) => (
                  <Grid item xs={12} key={course.id}>
                    <Card variant="outlined">
                      <CardContent>
                        <Typography variant="h6">
                          {course.code}: {course.title}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {course.description || 'No description available.'}
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
                            label={`${course.schedule?.days?.join(', ')} at ${course.schedule?.time}`} 
                            size="small" 
                            color="secondary" 
                            variant="outlined"
                          />
                        </Stack>
                      </CardContent>
                      <CardActions>
                        <Button size="small" onClick={() => viewCourseDetails(course.id)}>
                          View Details
                        </Button>
                      </CardActions>
                    </Card>
                  </Grid>
                ))}
              </Grid>
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
        onClose={() => setSnackbarOpen(false)}
        message={snackbarMessage}
      />
    </Container>
  );
};

export default Dashboard;