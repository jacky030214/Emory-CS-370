// src/App.jsx
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom"
import Login_Page from "./pages/Login_Page.jsx"
import Dashboard_Page from "./pages/Dashboard_Page.jsx"

import "./App.css"

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login_Page />} />
        <Route path="/dashboard" element={<Dashboard_Page />} />
        <Route path="/" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  )
}

export default App