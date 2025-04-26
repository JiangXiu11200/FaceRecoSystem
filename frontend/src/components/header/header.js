import { BreadCrumb } from "primereact/breadcrumb"
import { Button } from "primereact/button"
import { Menu } from "primereact/menu"
import React, { useMemo, useRef } from "react"
import { LiaUserCircle } from "react-icons/lia"
import { useLocation } from "react-router-dom"

import "./header.css"

function Header() {
  const location = useLocation()
  const home = { icon: "pi pi-home", url: "/" }
  const menuRight = useRef(null)

  const breadcrumbMap = {
    "/": [{ label: "Face Recognition" }],
    "/user_registration": [{ label: "User Registration" }],
    "/alarm_logs": [{ label: "Alarm Logs" }],
    "/activity_logs": [{ label: "Activity Logs" }],
    "/settings/recognition": [{ label: "Settings" }, { label: "Recognition" }],
    "/settings/accounts": [{ label: "Settings" }, { label: "Accounts" }],
    "/settings/system": [{ label: "Settings" }, { label: "System" }],
  }

  const items = useMemo(() => {
    console.log("location", location)
    return breadcrumbMap[location.pathname] || []
  }, [location.pathname])

  const menu_item = [
    { label: "New", icon: "pi pi-fw pi-plus" },
    { label: "Delete", icon: "pi pi-fw pi-trash" },
  ]
  return (
    <div className="row header-container">
      <div className="col left-layout">
        <BreadCrumb className="custom-breadcrumb" model={items} home={home} />
      </div>
      <div className="col right-layout">
        <div>
          <Menu
            id="user_menu"
            model={menu_item}
            popup
            ref={menuRight}
            popupAlignment="right"
          />
          <Button
            id="user_menu"
            className="header-button p-button-rounded p-button-text p-button-icon-only p-0"
            icon={<LiaUserCircle className="user-icon" />}
            onClick={(event) => menuRight.current.toggle(event)}
            aria-controls="user_menu"
          />
        </div>
      </div>
    </div>
  )
}

export default Header
