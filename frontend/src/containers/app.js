import React, { use, useState, useEffect } from "react"
import { Button } from "primereact/button"
import { BrowserRouter, Route, Routes } from "react-router-dom"
import Sidebar from "../components/system_sidebar/system_sidebar"
import Header from "../components/header/header"
import Login from "../components/login/login"
import FaceRecognition from "./face_recognition/face_recognition"
import UserRegistration from "./user_registration/user_registration"

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
            <div>
                {!is_login_page && <Sidebar setSidebarVisible={sidebar_visible} sidebarPinned={setSidebarPinned} />}
                <div className={`main-container ${sidebar_pinned ? "pinned" : ""}`}>
                    {!is_login_page && (
                        <div className="header-container">
                            <Button className="sidebar-btn" icon={sidebar_pinned ? "pi pi-chevron-left" : "pi pi-bars"} onClick={setSidebar} />
                            <Header />
                        </div>
                    )}
                    <Routes>
                        <Route exact path="/" element={<FaceRecognition />} />
                        <Route exact path="/login" element={<Login />} />
                        <Route exact path="/user_registration" element={<UserRegistration />} />
                        {/* <Route path="*" element={<NotFoundComponent />} />{" "} */}
                    </Routes>
                </div>
            </div>
        </BrowserRouter>
    )
}

export default App
