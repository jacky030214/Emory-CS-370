// src/pages/CourseCreate_Page.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Grid,
  Alert,
  CircularProgress,
  AppBar,
  Toolbar,
  Breadcrumbs,
  Link,
  Snackbar,
} from '@mui/material';
import { ArrowBack as ArrowBackIcon, Save as SaveIcon } from '@mui/icons-material';
import { CourseAPI } from '../services/api';

const CourseCreate_Page = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    code: '',
    description: '',
    professor_id: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [openSnackbar, setOpenSnackbar] = useState(false);
  const [formErrors, setFormErrors] = useState({});

  const validate = () => {
    const errors = {};
    if (!formData.title) errors.title = '제목은 필수입니다';
    if (!formData.code) errors.code = '코드는 필수입니다';
    if (!formData.professor_id) errors.professor_id = '교수 ID는 필수입니다';
    
    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validate()) return;
    
    try {
      setLoading(true);
      // professor_id를 숫자로 변환
      const dataToSubmit = {
        ...formData,
        professor_id: parseInt(formData.professor_id, 10),
      };
      
      const newCourse = await CourseAPI.createCourse(dataToSubmit);
      setOpenSnackbar(true);
      
      // 약간의 지연 후 상세 페이지로 이동 (사용자가 성공 메시지를 볼 수 있도록)
      setTimeout(() => {
        navigate(`/courses/${newCourse.id}`);
      }, 1500);
    } catch (error) {
      console.error('코스 생성 실패:', error);
      setError('코스 생성에 실패했습니다. 다시 시도해주세요.');
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    navigate('/courses');
  };

  const handleCloseSnackbar = () => {
    setOpenSnackbar(false);
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static" color="primary">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            새 코스 생성
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
          <Typography color="textPrimary">새 코스 생성</Typography>
        </Breadcrumbs>

        <Paper sx={{ p: 3 }}>
          <Button
            startIcon={<ArrowBackIcon />}
            onClick={handleBack}
            sx={{ mb: 2 }}
          >
            목록으로 돌아가기
          </Button>

          <Typography variant="h5" component="h1" gutterBottom>
            새 코스 정보 입력
          </Typography>

          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

          <form onSubmit={handleSubmit}>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  label="코스 제목"
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  fullWidth
                  margin="normal"
                  required
                  error={!!formErrors.title}
                  helperText={formErrors.title}
                />
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <TextField
                  label="코스 코드"
                  name="code"
                  value={formData.code}
                  onChange={handleChange}
                  fullWidth
                  margin="normal"
                  required
                  error={!!formErrors.code}
                  helperText={formErrors.code}
                />
              </Grid>
              
              <Grid item xs={12}>
                <TextField
                  label="코스 설명"
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  fullWidth
                  multiline
                  rows={4}
                  margin="normal"
                />
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <TextField
                  label="교수 ID"
                  name="professor_id"
                  type="number"
                  value={formData.professor_id}
                  onChange={handleChange}
                  fullWidth
                  margin="normal"
                  required
                  error={!!formErrors.professor_id}
                  helperText={formErrors.professor_id}
                />
              </Grid>
              
              <Grid item xs={12} sx={{ mt: 2 }}>
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <SaveIcon />}
                  disabled={loading}
                  sx={{ mr: 2 }}
                >
                  {loading ? '저장 중...' : '코스 저장'}
                </Button>
                
                <Button
                  variant="outlined"
                  onClick={handleBack}
                  disabled={loading}
                >
                  취소
                </Button>
              </Grid>
            </Grid>
          </form>
        </Paper>
      </Container>

      <Snackbar
        open={openSnackbar}
        autoHideDuration={3000}
        onClose={handleCloseSnackbar}
      >
        <Alert onClose={handleCloseSnackbar} severity="success">
          코스가 성공적으로 생성되었습니다!
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default CourseCreate_Page;