import React, { useEffect, useState } from "react"
import { PanelMenu } from "primereact/panelmenu"
import { Sidebar } from "primereact/sidebar"
import { useNavigate } from "react-router-dom"

import "./system_sidebar.css"

function SystemSidebar({ setSidebarVisible, sidebarPinned: setSidebarPinned }) {
  const navigate = useNavigate()
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    setVisible((visible) => !visible)
    setSidebarPinned((sidebarPinned) => !sidebarPinned)
  }, [setSidebarVisible])

  const hideSidebar = () => {
    setVisible(false)
    setSidebarPinned(false)
  }

  const isSettingsPath = ["/accounts", "/face-recognition-config"].some(
    (path) => location.pathname.startsWith(path)
  )

  const menuItems = [
    {
      label: "Face Recognition",
      icon: "pi pi-camera",
      command: () => navigate("/"),
    },
    {
      label: "User Registration",
      icon: "pi pi-user-plus",
      command: () => navigate("/user-registration"),
    },
    {
      label: "Alarm Logs",
      icon: "pi pi-exclamation-triangle",
      command: () => navigate("/alarm-logs"),
    },
    {
      label: "Activity Logs",
      icon: "pi pi-calendar-clock",
      command: () => navigate("/activity-logs"),
    },
    {
      label: "Settings",
      expanded: isSettingsPath,
      icon: "pi pi-wrench",
      items: [
        {
          label: "Accounts",
          icon: "pi pi-user",
          command: () => navigate("/accounts"),
        },
        {
          label: "Face Recognition ",
          icon: "pi pi-file-edit",
          command: () => navigate("/face-recognition-config"),
        },
        { label: "System", icon: "pi pi-cog" },
      ],
    },
  ]

  return (
    <div className={`app-container ${visible ? "pinned" : ""}`}>
      <Sidebar
        className={`custom-sidebar ${visible ? "pinned" : ""}`}
        visible={visible}
        onHide={hideSidebar}
        showCloseIcon={false}
        modal={false}
        dismissable={false}
      >
        <PanelMenu model={menuItems} />
      </Sidebar>
    </div>
  )
}

export default SystemSidebar
