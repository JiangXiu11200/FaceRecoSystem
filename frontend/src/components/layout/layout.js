import React, { useCallback, useState } from "react"

import { Button } from "primereact/button"
import { useLocation } from "react-router-dom"

import Header from "../header/header"
import Sidebar from "../system_sidebar/system_sidebar"

import "./layout.css"

const Layout = ({ children }) => {
  const location = useLocation()
  const [sidebar_visible, setSidebarVisible] = useState(false)
  const [sidebar_pinned, setSidebarPinned] = useState(false)

  const is_login_page = location.pathname === "/login"

  const setSidebar = useCallback(() => {
    setSidebarVisible((prev) => !prev)
  }, [])

  return (
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
        {children}
      </div>
    </div>
  )
}

export default Layout
