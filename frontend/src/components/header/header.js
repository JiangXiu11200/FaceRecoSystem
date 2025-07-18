import React, { useMemo, useRef, useState } from "react"
import { Avatar } from "primereact/avatar"
import { BreadCrumb } from "primereact/breadcrumb"
import { Menu } from "primereact/menu"
import { useLocation, useNavigate } from "react-router-dom"

import "./header.css"

function Header() {
  const navigate = useNavigate()
  const home = { icon: "pi pi-home", url: "/" }
  const location = useLocation()
  const menuRight = useRef(null)
  const [userPhotoUrl, setUserPhotoUrl] = useState(null)

  const breadcrumbMap = {
    "/": [{ label: "Face Recognition" }],
    "/user-registration": [{ label: "User Registration" }],
    "/alarm-logs": [{ label: "Alarm Logs" }],
    "/activity-logs": [{ label: "Activity Logs" }],
    "/accounts": [{ label: "Settings" }, { label: "Accounts" }],
    "/recognition": [{ label: "Settings" }, { label: "Recognition" }],
    "/system": [{ label: "Settings" }, { label: "System" }],
    "/face-recognition-config": [
      { label: "Settings" },
      { label: "Face Recognition" },
    ],
  }

  const items = useMemo(() => {
    console.log("location", location)
    return breadcrumbMap[location.pathname] || []
  }, [location.pathname])

  const menu_item = [
    {
      template: (item, options) => {
        return (
          <div
            className="p-3 gap-3 d-flex align-items-center"
            style={{ borderBottom: "1px solid #ddd" }}
          >
            <Avatar
              image={userPhotoUrl ?? "/image/cat.jpg"}
              shape="circle"
              size="large"
            />{" "}
            {/* The backend returns the S3 URL */}
            <div>
              <div>{"Jonas"}</div> {/* // The backend return user name */}
            </div>
          </div>
        )
      },
      disabled: true,
    },
    { label: "Help & Support", icon: "pi pi-question-circle" },
    {
      label: "Logout",
      icon: "pi pi-sign-out",
      command: () => {
        navigate("/login"), window.location.reload()
      },
    },
  ]
  return (
    <div className="row header-container">
      <div className="col left-layout">
        <BreadCrumb className="custom-breadcrumb" model={items} home={home} />
      </div>
      <div className="col right-layout">
        <div className="avatar-wrapper user_menu_btn">
          <Avatar
            image={userPhotoUrl ?? "/image/cat.jpg"}
            shape="circle"
            size="large"
            onClick={(event) => menuRight.current.toggle(event)}
          />
          <Menu
            id="user_menu"
            model={menu_item}
            popup
            ref={menuRight}
            popupAlignment="right"
          />
        </div>
      </div>
    </div>
  )
}

export default Header
