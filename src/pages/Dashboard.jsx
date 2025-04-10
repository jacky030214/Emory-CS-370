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
import AddCircleIcon from '@mui/icons-material/AddCircle';
import MenuBookIcon from '@mui/icons-material/MenuBook';

// Import the API services
import { CourseAPI, MajorAPI, UserAPI, ProfessorAPI } from "../services/api";

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
  const [selectedMajor, setSelectedMajor] = useState('Bachelor of Arts in Mathematics');
  const [startingSem, setStartingSem] = useState('Fall');
  const [startingYear, setStartingYear] = useState('2025');
  const [scheduleData, setScheduleData] = useState([]);
  const [loadingSchedule, setLoadingSchedule] = useState(false);
  const [scheduleError, setScheduleError] = useState('');
  
  // GER schedule states
  const [gerScheduleData, setGerScheduleData] = useState([]);
  const [loadingGerSchedule, setLoadingGerSchedule] = useState(false);
  const [gerScheduleError, setGerScheduleError] = useState('');
  
  // Added classes to schedule
  const [customClasses, setCustomClasses] = useState([]);
  
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  
  // Available majors
  const majors = [
    'Bachelor of Arts in African American Studies',
    'Bachelor of Arts in African Studies',
    'Bachelor of Arts in American Studies',
    'Bachelor of Arts in Ancient Mediterranean Studies',
    'Bachelor of Arts in Anthropology',
    'Bachelor of Science in Anthropology and Human Biology',
    'Bachelor of Science in Applied Mathematics',
    'Bachelor of Science in Applied Mathematics and Statistics',
    'Bachelor of Arts in Arabic'
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
      setScheduleError('Please select a major');
      return;
    }
    
    try {
      setLoadingSchedule(true);
      setScheduleError('');
      
      // Use MajorAPI to fetch semester schedule
      const data = await MajorAPI.getSemesterScheduleByName(selectedMajor, startingSem, startingYear);
      
      // If data is an array with error message
      if (Array.isArray(data) && data.length === 1 && typeof data[0] === 'string' && data[0].includes('Failed to generate')) {
        throw new Error(data[0]);
      }
      
      // Handle different response formats
      if (Array.isArray(data)) {
        setScheduleData(data);
      } else if (data && typeof data === 'object') {
        setScheduleData([data]);
      } else {
        throw new Error('Invalid response format from server');
      }
      
      setSnackbarMessage(`Schedule for ${selectedMajor} loaded successfully`);
      setSnackbarOpen(true);
    } catch (err) {
      console.error('Error fetching schedule:', err);
      setScheduleError(`Failed to fetch semester schedule: ${err.message}`);
      setScheduleData([]);
    } finally {
      setLoadingSchedule(false);
    }
  };

  // Handle fetchGERSchedule for major with general education requirements
  const handleFetchGERSchedule = async () => {
    if (!selectedMajor) {
      setGerScheduleError('Please select a major');
      return;
    }
    
    try {
      setLoadingGerSchedule(true);
      setGerScheduleError('');
      
      // Use MajorAPI to fetch GER semester schedule
      const data = await MajorAPI.getSemesterScheduleWithGER(selectedMajor, startingSem, startingYear);
      
      // If data is an array with error message
      if (Array.isArray(data) && data.length === 1 && typeof data[0] === 'string' && data[0].includes('Failed to generate')) {
        throw new Error(data[0]);
      }
      
      // Handle different response formats
      if (Array.isArray(data)) {
        setGerScheduleData(data);
      } else if (data && typeof data === 'object') {
        setGerScheduleData([data]);
      } else {
        throw new Error('Invalid response format from server');
      }
      
      setSnackbarMessage(`GER Schedule for ${selectedMajor} loaded successfully`);
      setSnackbarOpen(true);
    } catch (err) {
      console.error('Error fetching GER schedule:', err);
      setGerScheduleError(`Failed to fetch GER semester schedule: ${err.message}`);
      setGerScheduleData([]);
    } finally {
      setLoadingGerSchedule(false);
    }
  };

  // Handle adding a class to the semester schedule
  const handleAddToSchedule = () => {
    if (!classDetails) return;
    
    // Automatically switch to the schedule tab
    setTabValue(1);
    
    // Add class to custom classes list
    setCustomClasses([...customClasses, classDetails]);
    
    setSnackbarMessage(`${classDetails.class_id}: ${classDetails.class_name} added to your schedule`);
    setSnackbarOpen(true);
  };

  // Render schedule content with error handling
  const renderScheduleContent = (scheduleDataToRender, loadingState, errorState) => {
    if (loadingState) {
      return (
        <Box sx={{ display: 'flex', justifyContent: 'center', py: 3 }}>
          <CircularProgress />
        </Box>
      );
    }
    
    if (errorState) {
      return (
        <Box sx={{ mt: 2 }}>
          <Alert severity="error" sx={{ mb: 2 }}>
            {errorState}
          </Alert>
          
          {errorState.includes('Failed to generate') && (
            <Alert severity="info" sx={{ mt: 2 }}>
              <Typography variant="body2" gutterBottom>
                <strong>가능한 원인:</strong>
              </Typography>
              <ul style={{ margin: '0.5rem 0', paddingLeft: '1.5rem' }}>
                <li>백엔드 알고리즘에서 일정 생성 중 오류가 발생했습니다</li>
                <li>선택한 전공에 대한 요구사항 데이터가 불완전할 수 있습니다</li>
                <li>선택한 시작 학기와 연도에 대한 일정을 생성할 수 없습니다</li>
              </ul>
              <Typography variant="body2" sx={{ mt: 1 }}>
                <strong>추천 해결책:</strong> 다른 전공이나 시작 학기를 선택해보세요.
              </Typography>
            </Alert>
          )}
        </Box>
      );
    }
    
    return renderScheduleData(scheduleDataToRender);
  };

  // Schedule data rendering function with proper null checks
  const renderScheduleData = (scheduleDataToRender) => {
    // First check for custom added classes
    const hasCustomClasses = customClasses.length > 0;
    const hasScheduleData = scheduleDataToRender && scheduleDataToRender.length > 0;
    
    if (!hasCustomClasses && !hasScheduleData) {
      return (
        <Box sx={{ p: 3, textAlign: 'center' }}>
          <Typography>
            No schedule data available. Add classes from the Class Search or select a major schedule.
          </Typography>
        </Box>
      );
    }
    
    return (
      <Box>
        {/* Render Custom Added Classes first (only on the Major Schedule tab) */}
        {hasCustomClasses && tabValue === 1 && (
          <Card variant="outlined" sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" color="secondary">
                Your Added Classes
              </Typography>
              
              <Box sx={{ mt: 2 }}>
                {customClasses.map((course, courseIndex) => (
                  <Box key={courseIndex} sx={{ mb: 1, p: 1, borderLeft: '3px solid', borderColor: 'secondary.main' }}>
                    <Typography variant="subtitle1">
                      {course.class_name || 'Unknown Class'} ({course.class_id || 'No ID'})
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {course.credit_hours ? `${course.credit_hours} credits` : 'Credits unknown'} | {course.professor || 'TBA'}
                    </Typography>
                  </Box>
                ))}
              </Box>
            </CardContent>
          </Card>
        )}
        
        {/* Render Schedule Data */}
        {hasScheduleData && scheduleDataToRender.map((semester, index) => (
          <Card key={index} variant="outlined" sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" color="primary">
                {semester.semester || 'Unknown'} {semester.year || 'Year'} 
                {semester.total_credit_hours ? ` - ${semester.total_credit_hours} Credits` : ''}
              </Typography>
              
              {semester.classes && Array.isArray(semester.classes) && semester.classes.length > 0 ? (
                <Box sx={{ mt: 2 }}>
                  {semester.classes.map((course, courseIndex) => (
                    <Box key={courseIndex} sx={{ mb: 1, p: 1, borderLeft: '3px solid', borderColor: 'primary.main' }}>
                      <Typography variant="subtitle1">
                        {course.class_name || 'Unknown Class'} ({course.class_id || 'No ID'})
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {course.credit_hours ? `${course.credit_hours} credits` : 'Credits unknown'} | {course.professor || 'TBA'}
                        {course.requirement_designation && tabValue === 2 && (
                          <Chip 
                            size="small" 
                            label={course.requirement_designation} 
                            color="secondary" 
                            sx={{ ml: 1 }}
                          />
                        )}
                      </Typography>
                    </Box>
                  ))}
                </Box>
              ) : (
                <Typography variant="body2" sx={{ mt: 1 }}>
                  No classes for this semester
                </Typography>
              )}
            </CardContent>
          </Card>
        ))}
      </Box>
    );
  };

  // Common form for major selection and semester settings, used in both tabs
  const renderMajorSelectionForm = (handleFetchFunction, loadingState) => (
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
          onClick={handleFetchFunction}
          disabled={loadingState}
          startIcon={loadingState ? <CircularProgress size={20} /> : <SchoolIcon />}
          fullWidth
        >
          {loadingState ? 'Loading...' : 'View Schedule'}
        </Button>
      </Box>
    </Paper>
  );

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
          <Tab label="GER Schedule" icon={<MenuBookIcon />} iconPosition="start" />
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
                          {classDetails.prereqs && Array.isArray(classDetails.prereqs) && classDetails.prereqs.length > 0 ? (
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
                    <Button 
                      size="small" 
                      color="primary"
                      startIcon={<AddCircleIcon />}
                      variant="contained"
                      onClick={handleAddToSchedule}
                    >
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
            {renderMajorSelectionForm(handleFetchSchedule, loadingSchedule)}
          </Grid>
          
          {/* Schedule Display */}
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 2, minHeight: 240 }}>
              <Typography variant="h6" gutterBottom>
                Semester Schedule
                {selectedMajor && ` for ${selectedMajor}`}
              </Typography>
              
              {renderScheduleContent(scheduleData, loadingSchedule, scheduleError)}
            </Paper>
          </Grid>
        </Grid>
      </TabPanel>
      
      <TabPanel value={tabValue} index={2}>
        <Grid container spacing={3}>
          {/* Major Selection Form */}
          <Grid item xs={12} md={4}>
            {renderMajorSelectionForm(handleFetchGERSchedule, loadingGerSchedule)}
          </Grid>
          
          {/* GER Schedule Display */}
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 2, minHeight: 240 }}>
              <Typography variant="h6" gutterBottom>
                GER Semester Schedule
                {selectedMajor && ` for ${selectedMajor}`}
              </Typography>
              
              <Typography variant="body2" color="text.secondary" paragraph>
                This schedule includes General Education Requirements (GER) courses along with major requirements.
              </Typography>
              
              {renderScheduleContent(gerScheduleData, loadingGerSchedule, gerScheduleError)}
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