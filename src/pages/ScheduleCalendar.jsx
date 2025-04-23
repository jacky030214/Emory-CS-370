import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Typography,
  Button,
} from '@mui/material';
import { CourseAPI } from '../services/api';

const ScheduleCalendar = () => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        setLoading(true);
        const data = await CourseAPI.getAllCourses();
        setCourses(data);
        setLoading(false);
      } catch (err) {
        console.error("Error fetching courses:", err);
        setError("Failed to load course data");
        setLoading(false);
      }
    };

    fetchCourses();
  }, []);

  // Generate time slots from 8 AM to 9 PM
  const timeSlots = Array.from({ length: 14 }, (_, i) => {
    const hour = i + 8;
    return `${hour}:00`;
  });

  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'];

  if (loading) return <Box p={4}><Typography>Loading schedule...</Typography></Box>;
  if (error) return <Box p={4}><Typography color="error">Error: {error}</Typography></Box>;

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" sx={{ mb: 3 }}>Weekly Schedule</Typography>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Time</TableCell>
              {days.map((day) => (
                <TableCell key={day} align="center">{day}</TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {timeSlots.map((time) => (
              <TableRow key={time}>
                <TableCell component="th" scope="row">
                  {time}
                </TableCell>
                {days.map((day) => (
                  <TableCell key={`${day}-${time}`} align="center">
                    {courses
                      .filter(course => {
                        // This is a placeholder - you'll need to implement proper time/day matching
                        // based on your actual course time data structure
                        return course.time && course.time.includes(day) && course.time.includes(time);
                      })
                      .map(course => (
                        <Box
                          key={course.id}
                          sx={{
                            p: 1,
                            m: 0.5,
                            bgcolor: 'primary.main',
                            color: 'white',
                            borderRadius: 1,
                          }}
                        >
                          <Typography variant="body2">
                            {course.name}
                          </Typography>
                          <Typography variant="caption">
                            {course.professor?.first_name} {course.professor?.last_name}
                          </Typography>
                        </Box>
                      ))}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default ScheduleCalendar; 