import axios from 'axios';

// Base API URL
const API_URL = 'http://127.0.0.1:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const CourseAPI = {
  // Get all courses
  getAllCourses: async () => {
    try {
      const response = await api.get('/courses/');
      return response.data;
    } catch (error) {
      console.error('Error fetching courses:', error);
      throw error;
    }
  },

  // Get course by ID
  getCourseById: async (id) => {
    try {
      const response = await api.get(`/courses/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching course with ID ${id}:`, error);
      throw error;
    }
  },

  // Get course by code
  getCourseByCode: async (code) => {
    try {
      const response = await api.get(`/courses/code/${code}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching course with code ${code}:`, error);
      throw error;
    }
  },

  // Create a new course
  createCourse: async (courseData) => {
    try {
      const response = await api.post('/courses/', courseData);
      return response.data;
    } catch (error) {
      console.error('Error creating course:', error);
      throw error;
    }
  },
  
  // Get class by class ID (from course_mongodb)
  getClassByClassId: async (classId) => {
    try {
      const response = await api.get('/get_class_by_class_id', {
        params: { class_id: classId }
      });
      return response.data;
    } catch (error) {
      console.error(`Error fetching class with ID ${classId}:`, error);
      throw error;
    }
  }
};

export const MajorAPI = {
  // Get all majors
  getAllMajors: async () => {
    try {
      const response = await api.get('/majors');
      return response.data;
    } catch (error) {
      console.error('Error fetching majors:', error);
      throw error;
    }
  },
  
  // Get major requirements by major name
  getMajorRequirementsByName: async (majorName) => {
    try {
      const response = await api.get('/get_major_requirement_by_major_name', {
        params: { major: majorName }
      });
      return response.data;
    } catch (error) {
      console.error(`Error fetching requirements for major ${majorName}:`, error);
      throw error;
    }
  },
  
  // Get semester schedule by major name
  getSemesterScheduleByName: async (majorName) => {
    try {
      const response = await api.get('/get_semester_schedule_by_major_name', {
        params: { major: majorName }
      });
      return response.data;
    } catch (error) {
      console.error(`Error fetching schedule for major ${majorName}:`, error);
      throw error;
    }
  }
};

export const UserAPI = {
  // Get all users
  getAllUsers: async () => {
    try {
      const response = await api.get('/users/');
      return response.data;
    } catch (error) {
      console.error('Error fetching users:', error);
      throw error;
    }
  },
  
  // Register new user
  register: async (userData) => {
    try {
      const response = await api.post('/users/', userData);
      return response.data;
    } catch (error) {
      console.error('Error registering user:', error);
      throw error;
    }
  },

  // Login user
  login: async (credentials) => {
    try {
      const response = await api.post('/users/login', credentials);
      return response.data;
    } catch (error) {
      console.error('Error logging in:', error);
      throw error;
    }
  },

  // Get user by ID
  getUserById: async (id) => {
    try {
      const response = await api.get(`/users/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching user with ID ${id}:`, error);
      throw error;
    }
  },

  // Get user by username
  getUserByUsername: async (username) => {
    try {
      const response = await api.get(`/users/username/${username}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching user with username ${username}:`, error);
      throw error;
    }
  },
  
  // Get user by email
  getUserByEmail: async (email) => {
    try {
      const response = await api.get(`/users/email/${email}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching user with email ${email}:`, error);
      throw error;
    }
  }
};

export const ProfessorAPI = {
  // Get all professors
  getAllProfessors: async () => {
    try {
      const response = await api.get('/professors/');
      return response.data;
    } catch (error) {
      console.error('Error fetching professors:', error);
      throw error;
    }
  },
  
  // Create professor
  createProfessor: async (professorData) => {
    try {
      const response = await api.post('/professors/', professorData);
      return response.data;
    } catch (error) {
      console.error('Error creating professor:', error);
      throw error;
    }
  },

  // Get professor by ID
  getProfessorById: async (id) => {
    try {
      const response = await api.get(`/professors/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching professor with ID ${id}:`, error);
      throw error;
    }
  },

  // Get professor by name
  getProfessorByName: async (name) => {
    try {
      const response = await api.get(`/professors/name/${name}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching professor with name ${name}:`, error);
      throw error;
    }
  }
};