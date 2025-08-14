import React from "react"

import { BrowserRouter, Route, Routes } from "react-router-dom"

import Layout from "./components/layout/layout"
import Login from "./containers/login/login"
import { TokenProvider } from "./contexts/token_provider"
import Accounts from "./pages/accounts/accounts"
import ActivityLogs from "./pages/activity_logs/activity_logs"
import AlarmLogs from "./pages/alarm_logs/alarm_logs"
import FaceRecognition from "./pages/face_recognition/face_recognition"
import FaceRecognitionConfig from "./pages/face_recognition_config/face_recognition_config"
import UserRegistration from "./pages/user_registration/user_registration"
import PrivateRoute from "./routes/private_route"

import "./app.css"

function App() {
  const NotFoundComponent = () => {
    window.location.href = "/"
    return null
  }

  return (
    <BrowserRouter>
      <TokenProvider>
        <Routes>
          <Route path="/login" element={<Login />} />

          <Route
            path="/*"
            element={
              <PrivateRoute>
                <Layout>
                  <Routes>
                    <Route path="/" element={<FaceRecognition />} />
                    <Route
                      path="/user-registration"
                      element={<UserRegistration />}
                    />
                    <Route path="/alarm-logs" element={<AlarmLogs />} />
                    <Route path="/activity-logs" element={<ActivityLogs />} />
                    <Route path="/accounts" element={<Accounts />} />
                    <Route
                      path="/face-recognition-config"
                      element={<FaceRecognitionConfig />}
                    />
                    <Route path="*" element={<NotFoundComponent />} />
                  </Routes>
                </Layout>
              </PrivateRoute>
            }
          />
        </Routes>
      </TokenProvider>
    </BrowserRouter>
  )
}

export default App
