import React, { useEffect, useState } from "react"
import { PanelMenu } from "primereact/panelmenu"
import { Sidebar } from "primereact/sidebar"
import { useNavigate } from "react-router-dom"
import { useToken } from "../../contexts/token_provider"

import "./system_sidebar.css"

function SystemSidebar({ setSidebarVisible, sidebarPinned: setSidebarPinned }) {
  const navigate = useNavigate()
  const [visible, setVisible] = useState(false)
  const { permissions } = useToken()
  const isDevelopment = process.env.NODE_ENV === "development"
  const bypassAuth = process.env.REACT_APP_DEV_BYPASS_AUTH === "true"

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

  const baseMenuItems = [
    {
      label: "Face Recognition",
      icon: "pi pi-camera",
      permission: "face-recognition",
      command: () => navigate("/"),
    },
    {
      label: "User Registration",
      icon: "pi pi-user-plus",
      permission: "user-registration",
      command: () => navigate("/user-registration"),
    },
    {
      label: "Alarm Logs",
      icon: "pi pi-exclamation-triangle",
      permission: "alarm-logs",
      command: () => navigate("/alarm-logs"),
    },
    {
      label: "Activity Logs",
      icon: "pi pi-calendar-clock",
      permission: "activity-logs",
      command: () => navigate("/activity-logs"),
    },
    {
      label: "Settings",
      expanded: isSettingsPath,
      icon: "pi pi-wrench",
      permission:
        permissions.includes("accounts") ||
        permissions.includes("face-recognition-config")
          ? null
          : "none",
      items: [
        {
          label: "Accounts",
          icon: "pi pi-user",
          permission: "accounts",
          command: () => navigate("/accounts"),
        },
        {
          label: "Face Recognition ",
          icon: "pi pi-file-edit",
          permission: "face-recognition-config",
          command: () => navigate("/face-recognition-config"),
        },
      ],
    },
  ]

  const filterMenuItems = (items) => {
    if (isDevelopment && bypassAuth) {
      return items
    }

    return items
      .filter((item) => {
        if (!item.permission) return true
        return permissions.includes(item.permission)
      })
      .map((item) => {
        if (item.items) {
          return { ...item, items: filterMenuItems(item.items) }
        }
        return item
      })
  }

  const menuItems = filterMenuItems(baseMenuItems)

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
