import React, { useState, useEffect } from "react"
import { PanelMenu } from "primereact/panelmenu"
import { Sidebar } from "primereact/sidebar"
import { Button } from "primereact/button"
import "./system_sidebar.css"

function SystemSidebar({ setSidebarVisible, sidebarPinned: setSidebarPinned }) {
    const [visible, setVisible] = useState(false)

    useEffect(() => {
        setVisible((visible) => !visible)
        setSidebarPinned((sidebarPinned) => !sidebarPinned)
    }, [setSidebarVisible])

    const hideSidebar = () => {
        setVisible(false)
        setSidebarPinned(false)
    }

    const menuItems = [
        { label: "Face Recognition", icon: "pi pi-camera" },
        { label: "User Registration", icon: "pi pi-user-plus" },
        { label: "Alarm Logs", icon: "pi pi-exclamation-triangle" },
        { label: "Activity Logs", icon: "pi pi-calendar-clock" },
        {
            label: "Settings",
            icon: "pi pi-wrench",
            items: [
                { label: "Recognition", icon: "pi pi-eye" },
                { label: "Accounts", icon: "pi pi-user" },
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
