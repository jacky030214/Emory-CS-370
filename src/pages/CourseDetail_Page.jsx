// src/pages/CourseDetail_Page.jsx
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Paper,
  Typography,
  Grid,
  Button,
  Divider,
  Alert,
  CircularProgress,
  Breadcrumbs,
  Link,
  AppBar,
  Toolbar,
} from '@mui/material';
import { ArrowBack as ArrowBackIcon } from '@mui/icons-material';
import { CourseAPI } from '../services/api';

const CourseDetail_Page = () => {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCourseDetails();
  }, [courseId]);

  const fetchCourseDetails = async () => {
    try {
      setLoading(true);
      const data = await CourseAPI.getCourseById(courseId);
      setCourse(data);
      setError(null);
    } catch (error) {
      console.error('코스 세부 정보 로딩 실패:', error);
      setError('코스 정보를 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    navigate('/courses');
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Alert severity="error">{error}</Alert>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={handleBack}
          sx={{ mt: 2 }}
        >
          코스 목록으로 돌아가기
        </Button>
      </Container>
    );
  }

  if (!course) {
    return (
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Alert severity="warning">코스를 찾을 수 없습니다.</Alert>
        <Button
          startIcon={<ArrowBackIcon />}
          onClick={handleBack}
          sx={{ mt: 2 }}
        >
          코스 목록으로 돌아가기
        </Button>
      </Container>
    );
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" color="primary">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            코스 세부 정보
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 2 }}>
          <Link color="inherit" href="#" onClick={() => navigate('/')}>
            홈
          </Link>
          <Link color="inherit" href="#" onClick={() => navigate('/courses')}>
            코스 목록
          </Link>
          <Typography color="textPrimary">{course.title}</Typography>
        </Breadcrumbs>

        <Paper sx={{ p: 3 }}>
          <Button
            startIcon={<ArrowBackIcon />}
            onClick={handleBack}
            sx={{ mb: 2 }}
          >
            목록으로 돌아가기
          </Button>

          <Typography variant="h4" component="h1" gutterBottom>
            {course.title}
          </Typography>
          
          <Typography variant="subtitle1" color="textSecondary" gutterBottom>
            코스 코드: {course.code}
          </Typography>

          <Divider sx={{ my: 2 }} />

          <Grid container spacing={3}>
            <Grid item xs={12} md={8}>
              <Typography variant="h6" gutterBottom>
                코스 설명
              </Typography>
              <Typography paragraph>
                {course.description || '코스 설명이 없습니다.'}
              </Typography>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <Paper elevation={2} sx={{ p: 2, bgcolor: 'background.default' }}>
                <Typography variant="h6" gutterBottom>
                  코스 정보
                </Typography>
                
                <Typography variant="body1" paragraph>
                  <strong>교수:</strong> {course.professor.name}
                </Typography>
                
                {/* 추가 코스 정보가 있다면 여기에 표시 */}
              </Paper>
            </Grid>
          </Grid>
        </Paper>
      </Container>
    </Box>
  );
};

export default CourseDetail_Page;