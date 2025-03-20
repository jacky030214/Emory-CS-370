// src/services/api.js
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
      const response = await api.get('/courses');
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
      const response = await api.post('/courses', courseData);
      return response.data;
    } catch (error) {
      console.error('Error creating course:', error);
      throw error;
    }
  }
};

export const UserAPI = {
  // Register new user
  register: async (userData) => {
    try {
      const response = await api.post('/users', userData);
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
  }
};

export const ProfessorAPI = {
  // Get all professors
  getAllProfessors: async () => {
    try {
      const response = await api.get('/professors');
      return response.data;
    } catch (error) {
      console.error('Error fetching professors:', error);
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