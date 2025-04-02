import React, { useState, useEffect } from 'react';
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
  TextField,
  Button,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  CardActions,
  Chip,
  Stack,
  Divider,
  Snackbar,
  Tabs,
  Tab
} from '@mui/material';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import ClassIcon from '@mui/icons-material/Class';
import SearchIcon from '@mui/icons-material/Search';
import SchoolIcon from '@mui/icons-material/School';

// Import the API services
import { CourseAPI, MajorAPI } from '../services/api';

// TabPanel component for tab content
function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`dashboard-tabpanel-${index}`}
      aria-labelledby={`dashboard-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ pt: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

const Dashboard = () => {
  const navigate = useNavigate();
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [classId, setClassId] = useState('');
  const [classDetails, setClassDetails] = useState(null);
  
  // Major schedule states
  const [selectedMajor, setSelectedMajor] = useState('');
  const [startingSem, setStartingSem] = useState('Fall');
  const [startingYear, setStartingYear] = useState('2024');
  const [scheduleData, setScheduleData] = useState([]);
  const [loadingSchedule, setLoadingSchedule] = useState(false);
  
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  
  // Available majors
  const majors = [
    'Bachelor of Arts in Mathematics',
    'Bachelor of Science in Computer Science',
    'Bachelor of Arts in Business Administration',
    'Bachelor of Science in Engineering'
  ];

  // Handle tab change
  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  // Handle class search
  const handleClassSearch = async () => {
    if (!classId.trim()) {
      setError('Please enter a class ID');
      return;
    }

    try {
      setLoading(true);
      setError('');
      
      // Use CourseAPI to fetch class details
      const data = await CourseAPI.getClassByClassId(classId);
      setClassDetails(data);
      
      setSnackbarMessage(`Class ${classId} details loaded successfully`);
      setSnackbarOpen(true);
    } catch (err) {
      console.error('Error fetching class details:', err);
      setError('Failed to fetch class details. Please check the class ID and try again.');
      setClassDetails(null);
    } finally {
      setLoading(false);
    }
  };

  // Handle input change for class ID
  const handleInputChange = (event) => {
    setClassId(event.target.value);
  };
  
  // Handle major selection change
  const handleMajorChange = (event) => {
    setSelectedMajor(event.target.value);
  };
  
  // Handle fetchSchedule for major
  const handleFetchSchedule = async () => {
    if (!selectedMajor) {
      setError('Please select a major');
      return;
    }
    
    try {
      setLoadingSchedule(true);
      setError('');
      
      // Use MajorAPI to fetch semester schedule
      const data = await MajorAPI.getSemesterScheduleByName(selectedMajor, startingSem, startingYear);
      setScheduleData(data);
      
      setSnackbarMessage(`Schedule for ${selectedMajor} loaded successfully`);
      setSnackbarOpen(true);
    } catch (err) {
      console.error('Error fetching schedule:', err);
      setError('Failed to fetch semester schedule. Please try again.');
      setScheduleData([]);
    } finally {
      setLoadingSchedule(false);
    }
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
      
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="dashboard tabs">
          <Tab label="Class Search" icon={<ClassIcon />} iconPosition="start" />
          <Tab label="Major Schedule" icon={<SchoolIcon />} iconPosition="start" />
        </Tabs>
      </Box>
      
      <TabPanel value={tabValue} index={0}>
        <Grid container spacing={3}>
          {/* Class Search Form */}
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 2, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                Class Search
              </Typography>
              
              <FormControl fullWidth margin="normal">
                <TextField
                  label="Class ID"
                  value={classId}
                  onChange={handleInputChange}
                  placeholder="e.g. Math111"
                  disabled={loading}
                  fullWidth
                  variant="outlined"
                  helperText="Enter a class ID to search"
                />
              </FormControl>
              
              <Box sx={{ mt: 2 }}>
                <Button 
                  variant="contained" 
                  color="primary" 
                  onClick={handleClassSearch}
                  disabled={loading}
                  startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
                  fullWidth
                >
                  {loading ? 'Searching...' : 'Search'}
                </Button>
              </Box>
            </Paper>
          </Grid>
          
          {/* Class Details */}
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 2, minHeight: 240 }}>
              <Typography variant="h6" gutterBottom>
                Class Details
              </Typography>
              
              {loading ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', py: 3 }}>
                  <CircularProgress />
                </Box>
              ) : classDetails ? (
                <Card variant="outlined">
                  <CardContent>
                    <Typography variant="h5" gutterBottom>
                      {classDetails.class_id}: {classDetails.class_name}
                    </Typography>
                    
                    <Typography variant="body1" paragraph>
                      {classDetails.class_desc || 'No description available.'}
                    </Typography>
                    
                    <Divider sx={{ my: 2 }} />
                    
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="subtitle2">Details:</Typography>
                        <Box sx={{ mt: 1 }}>
                          <Stack direction="row" spacing={1} sx={{ mb: 1 }}>
                            <Chip 
                              icon={<ClassIcon />} 
                              label={`${classDetails.credit_hours} credits`} 
                              size="small" 
                              color="primary" 
                              variant="outlined"
                            />
                          </Stack>
                          <Typography variant="body2">
                            <strong>Offered:</strong> {classDetails.recurring}
                          </Typography>
                          <Typography variant="body2">
                            <strong>Designation:</strong> {classDetails.requirement_designation}
                          </Typography>
                          <Typography variant="body2">
                            <strong>Campus:</strong> {classDetails.campus}
                          </Typography>
                        </Box>
                      </Grid>
                      
                      <Grid item xs={12} sm={6}>
                        <Typography variant="subtitle2">Prerequisites:</Typography>
                        <Box sx={{ mt: 1 }}>
                          {classDetails.prereqs && classDetails.prereqs.length > 0 ? (
                            classDetails.prereqs.map((prereq, index) => (
                              <Chip 
                                key={index}
                                label={prereq} 
                                size="small" 
                                sx={{ mr: 1, mb: 1 }}
                              />
                            ))
                          ) : (
                            <Typography variant="body2">No prerequisites</Typography>
                          )}
                        </Box>
                      </Grid>
                    </Grid>
                  </CardContent>
                  <CardActions>
                    <Button size="small" color="primary">
                      Add to Schedule
                    </Button>
                  </CardActions>
                </Card>
              ) : (
                <Box sx={{ p: 3, textAlign: 'center' }}>
                  <Typography>
                    Enter a class ID and click Search to view class details.
                  </Typography>
                </Box>
              )}
            </Paper>
          </Grid>
        </Grid>
      </TabPanel>
      
      <TabPanel value={tabValue} index={1}>
        <Grid container spacing={3}>
          {/* Major Selection Form */}
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 2, height: '100%' }}>
              <Typography variant="h6" gutterBottom>
                Select Major and Starting Semester
              </Typography>
              
              <FormControl fullWidth margin="normal">
                <InputLabel id="major-select-label">Major</InputLabel>
                <Select
                  labelId="major-select-label"
                  value={selectedMajor}
                  label="Major"
                  onChange={handleMajorChange}
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
              
              <FormControl fullWidth margin="normal">
                <InputLabel id="semester-select-label">Starting Semester</InputLabel>
                <Select
                  labelId="semester-select-label"
                  value={startingSem}
                  label="Starting Semester"
                  onChange={(e) => setStartingSem(e.target.value)}
                >
                  <MenuItem value="Fall">Fall</MenuItem>
                  <MenuItem value="Spring">Spring</MenuItem>
                  <MenuItem value="Summer">Summer</MenuItem>
                </Select>
              </FormControl>
              
              <FormControl fullWidth margin="normal">
                <TextField
                  label="Starting Year"
                  value={startingYear}
                  onChange={(e) => setStartingYear(e.target.value)}
                  type="number"
                  variant="outlined"
                />
              </FormControl>
              
              <Box sx={{ mt: 2 }}>
                <Button 
                  variant="contained" 
                  color="primary" 
                  onClick={handleFetchSchedule}
                  disabled={loadingSchedule}
                  startIcon={loadingSchedule ? <CircularProgress size={20} /> : <SchoolIcon />}
                  fullWidth
                >
                  {loadingSchedule ? 'Loading...' : 'View Schedule'}
                </Button>
              </Box>
            </Paper>
          </Grid>
          
          {/* Schedule Display */}
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 2, minHeight: 240 }}>
              <Typography variant="h6" gutterBottom>
                Semester Schedule
                {selectedMajor && ` for ${selectedMajor}`}
              </Typography>
              
              {loadingSchedule ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', py: 3 }}>
                  <CircularProgress />
                </Box>
              ) : scheduleData && scheduleData.length > 0 ? (
                <Box>
                  {scheduleData.map((semester, index) => (
                    <Card key={index} variant="outlined" sx={{ mb: 3 }}>
                      <CardContent>
                        <Typography variant="h6" color="primary">
                          {semester.semester} {semester.year} - {semester.total_credit_hours} Credits
                        </Typography>
                        
                        {semester.classes && semester.classes.length > 0 ? (
                          <Box sx={{ mt: 2 }}>
                            {semester.classes.map((course, courseIndex) => (
                              <Box key={courseIndex} sx={{ mb: 1, p: 1, borderLeft: '3px solid', borderColor: 'primary.main' }}>
                                <Typography variant="subtitle1">
                                  {course.class_name} ({course.class_id})
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                  {course.credit_hours} credits | {course.professor || 'TBA'}
                                </Typography>
                              </Box>
                            ))}
                          </Box>
                        ) : (
                          <Typography variant="body2">No classes for this semester</Typography>
                        )}
                      </CardContent>
                    </Card>
                  ))}
                </Box>
              ) : (
                <Box sx={{ p: 3, textAlign: 'center' }}>
                  <Typography>
                    Select a major and click "View Schedule" to see the recommended semester plan.
                  </Typography>
                </Box>
              )}
            </Paper>
          </Grid>
        </Grid>
      </TabPanel>

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