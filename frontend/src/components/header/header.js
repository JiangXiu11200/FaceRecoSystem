import React, { useCallback, useEffect, useMemo, useRef, useState } from "react"

import { Avatar } from "primereact/avatar"
import { BreadCrumb } from "primereact/breadcrumb"
import { Dropdown } from "primereact/dropdown"
import { Menu } from "primereact/menu"
import { Toast } from "primereact/toast"
import CountryFlag from "react-country-flag"
import { useLocation, useNavigate } from "react-router-dom"

import { accountsAPI } from "../../api/accounts"
import { logoutApi } from "../../api/auth"
import { clearLocalStorage } from "../../utils/local_storage"

import "./header.css"

function Header() {
  const navigate = useNavigate()
  const toast = useRef(null)
  const home = { icon: "pi pi-home", url: "/" }
  const location = useLocation()
  const menuRight = useRef(null)
  const [selectedLang, setSelectedLang] = useState("en")

  const [avatarURL, setAvatarURL] = useState(null)
  const [userName, setUserName] = useState("user")
  const lastFetchTime = useRef(0)
  const cachedURL = useRef("")
  const cachedFileName = useRef("")

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

  const languages = [
    { label: "English", value: "en", countryCode: "US" },
    // { label: "繁體中文", value: "zh-TW", countryCode: "TW" }, // TODO: add i18n support
  ]

  const showToast = (severity, summary, detail, life = 3000) => {
    toast.current.show({ severity, summary, detail, life })
  }

  const updateAvatarURL = useCallback(async () => {
    const profilePictureFileName = localStorage.getItem(
      "profile_picture_file_name"
    )
    const userName = localStorage.getItem("user_name")
    setUserName(userName)
    const now = Date.now()
    const CACHE_DURATION = 30 * 60 * 1000 // 30 minutes

    const needsUpdate =
      (!cachedURL.current ||
        cachedFileName.current !== profilePictureFileName ||
        now - lastFetchTime.current > CACHE_DURATION) &&
      profilePictureFileName !== "null"

    if (!needsUpdate) {
      // Use cached URL if it matches the current file name
      if (avatarURL !== cachedURL.current) {
        setAvatarURL(cachedURL.current)
      }
      return
    }
    try {
      const response = await accountsAPI("get", "/avatars/", {
        profile_picture_file_name: profilePictureFileName,
      })

      const newURL = response.data.url
      setAvatarURL(newURL)

      // Update cache
      cachedURL.current = newURL
      cachedFileName.current = profilePictureFileName
      lastFetchTime.current = now
    } catch (err) {
      showToast("error", "Header", err.response.data)
    }
  }, [avatarURL])

  useEffect(() => {
    updateAvatarURL()
    const intervalId = setInterval(updateAvatarURL, 30 * 60 * 1000)
    return () => clearInterval(intervalId)
  }, [updateAvatarURL])

  const customOptionTemplate = (option) => (
    <div className="language-option">
      <CountryFlag
        className="country-flag"
        svg
        countryCode={option.countryCode}
        aria-label={option.label}
      />
      <span>{option.label}</span>
    </div>
  )

  const selectedTemplate = (option, props) => {
    if (option) return customOptionTemplate(option)
    return <span>{props.placeholder}</span>
  }

  const items = useMemo(() => {
    return breadcrumbMap[location.pathname] || []
  }, [location.pathname])

  const logoout = () => {
    logoutApi()
    navigate("/login")
    window.location.reload()
    clearLocalStorage()
  }

  const menu_item = [
    {
      template: (item, options) => {
        return (
          <div
            className="p-3 gap-3 d-flex align-items-center"
            style={{ borderBottom: "1px solid #ddd" }}
          >
            <Avatar
              image={avatarURL ? avatarURL : "/image/user.jpg"}
              shape="circle"
              size="large"
            />
            <div>
              <div>{userName}</div>
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
      command: logoout,
    },
  ]

  return (
    <div className="row header-container">
      <div>
        <Toast ref={toast} />
      </div>
      <div className="col left-layout">
        <BreadCrumb className="custom-breadcrumb" model={items} home={home} />
      </div>
      <div className="col right-layout">
        <div className="avatar-wrapper user_menu_btn">
          <div className="d-flex align-items-center justify-content-end">
            {/* TODO: i18n for language selection */}
            <Dropdown
              className="language-dropdown"
              value={selectedLang}
              options={languages}
              onChange={(e) => setSelectedLang(e.value)}
              optionLabel="label"
              itemTemplate={customOptionTemplate}
              valueTemplate={selectedTemplate}
              placeholder="Select Language"
            />
          </div>
          <div className="d-flex align-items-center justify-content-end">
            <Avatar
              image={avatarURL ? avatarURL : "/image/user.jpg"}
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
    </div>
  )
}

export default Header
