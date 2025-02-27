// src/App.jsx
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom"
import Login_Page from "./pages/Login_Page.jsx"
import Signup_Page from "./pages/Signup_Page.jsx"  // 회원가입 페이지 import 추가
import Dashboard_Page from "./pages/Dashboard_Page.jsx"
// Course pages import
import Courses_Page from "./pages/Courses_Page.jsx"
import CourseDetail_Page from "./pages/CourseDetail_Page.jsx"
import CourseCreate_Page from "./pages/CourseCreate_Page.jsx"

import "./App.css"

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login_Page />} />
        <Route path="/signup" element={<Signup_Page />} />  
        <Route path="/dashboard" element={<Dashboard_Page />} />
        {/* Courses */}
        <Route path="/courses" element={<Courses_Page />} />
        <Route path="/courses/new" element={<CourseCreate_Page />} />
        <Route path="/courses/:courseId" element={<CourseDetail_Page />} />
        <Route path="/" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  )
}

export default App