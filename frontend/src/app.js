import React, { useState } from "react"
import { Button } from "primereact/button"
import { BrowserRouter, Route, Routes } from "react-router-dom"

import Header from "./components/header/header"
import Sidebar from "./components/system_sidebar/system_sidebar"
import Login from "./containers/login/login"

import Accounts from "./pages/accounts/accounts"
import ActivityLogs from "./pages/activity_logs/activity_logs"
import AlarmLogs from "./pages/alarm_logs/alarm_logs"
import FaceRecognition from "./pages/face_recognition/face_recognition"
import FaceRecognitionConfig from "./pages/face_recognition_config/face_recognition_config"
import UserRegistration from "./pages/user_registration/user_registration"

import { TokenProvider } from "./contexts/token_provider"

import "./app.css"

function App() {
  const [sidebar_visible, setSidebarVisible] = useState(false)
  const [sidebar_pinned, setSidebarPinned] = useState(false)
  const is_login_page = location.pathname === "/login"

  const setSidebar = () => {
    setSidebarVisible((sidebar_visible) => !sidebar_visible)
  }

  // const NotFoundComponent = () => {
  //     window.location.href = "/"
  //     return null
  // }

  return (
    <BrowserRouter>
      <TokenProvider>
        <div>
          {!is_login_page && (
            <Sidebar
              setSidebarVisible={sidebar_visible}
              sidebarPinned={setSidebarPinned}
            />
          )}
          <div className={`main-container ${sidebar_pinned ? "pinned" : ""}`}>
            {!is_login_page && (
              <div className="header-container">
                <Button
                  className="sidebar-btn"
                  icon={sidebar_pinned ? "pi pi-chevron-left" : "pi pi-bars"}
                  onClick={setSidebar}
                />
                <Header />
              </div>
            )}
            <Routes>
              <Route exact path="/" element={<FaceRecognition />} />
              <Route exact path="/login" element={<Login />} />
              <Route
                exact
                path="/user-registration"
                element={<UserRegistration />}
              />
              <Route exact path="/alarm-logs" element={<AlarmLogs />} />
              <Route exact path="/activity-logs" element={<ActivityLogs />} />
              <Route exact path="/accounts" element={<Accounts />} />
              <Route
                exact
                path="/face-recognition-config"
                element={<FaceRecognitionConfig />}
              />
              {/* <Route path="*" element={<NotFoundComponent />} />{" "} */}
            </Routes>
          </div>
        </div>
      </TokenProvider>
    </BrowserRouter>
  )
}

export default App
