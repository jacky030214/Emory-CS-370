// src/App.jsx
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom"
import Login_Page from "./pages/Login_Page.jsx"
import Dashboard_Page from "./pages/Dashboard_Page.jsx"
import Profile_Page from "./pages/Profile_Page.jsx"  // Profile_Page import 추가
import Settings_Page from "./pages/Settings_Page.jsx"  // Settings_Page import 추가

import "./App.css"

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login_Page />} />
        <Route path="/dashboard" element={<Dashboard_Page />} />
        <Route path="/profile" element={<Profile_Page />} />  {/* Profile 라우트 추가 */}
        <Route path="/settings" element={<Settings_Page />} />  {/* Settings 라우트 추가 */}
        <Route path="/" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  )
}

export default App