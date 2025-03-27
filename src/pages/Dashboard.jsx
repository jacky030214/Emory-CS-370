//wed mar 26 updated
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Paper,
  Grid,
  FormControl,
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
  Snackbar
} from '@mui/material';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import ClassIcon from '@mui/icons-material/Class';
import SearchIcon from '@mui/icons-material/Search';

// Import the CourseAPI service instead of direct api
import { CourseAPI } from '../services/api';

const Dashboard = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [classId, setClassId] = useState('');
  const [classDetails, setClassDetails] = useState(null);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');

  // Handle class search
  const handleClassSearch = async () => {
    if (!classId.trim()) {
      setError('Please enter a class ID');
      return;
    }

    try {
      setLoading(true);
      setError('');
      
      // Use CourseAPI instead of direct api
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

  // Handle input change
  const handleInputChange = (event) => {
    setClassId(event.target.value);
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
        {/* Search Form */}
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