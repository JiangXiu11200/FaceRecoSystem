import React, { createContext, useContext, useEffect, useState } from "react"

import { jwtDecode } from "jwt-decode"
import { Button } from "primereact/button"
import { Dialog } from "primereact/dialog"

import { logoutApi, refreshTokenApi } from "../api/auth"
import { clearLocalStorage } from "../utils/local_storage"

const TokenContext = createContext()

export const TokenProvider = ({ children }) => {
  const [set_authenticated, setAuthenticated] = useState(false)
  const [is_loading, setIsLoading] = useState(true) // Used to make private routes wait for token check
  const [permissions, setPermissions] = useState([])
  const [logout_reason, setLogoutReason] = useState(false)
  const [logout_dialog_message, setLogoutDialogMessage] = useState("")

  useEffect(() => {
    const token = localStorage.getItem("access_token")
    if (token) {
      const { permissions } = jwtDecode(token)
      setPermissions(permissions)
    }
  }, [])

  useEffect(() => {
    checkTokenStatus()
    const intervalId = setInterval(checkTokenStatus, 5 * 60 * 1000)

    return () => clearInterval(intervalId)
  }, [])

  const checkTokenStatus = async () => {
    const token = localStorage.getItem("access_token")

    if (!token) {
      setIsLoading(false)
      return
    }

    if (isTokenExpired(token)) {
      await refreshAccessToken()
    } else {
      setAuthenticated(true)
      setIsLoading(false)
    }
  }

  const refreshAccessToken = async () => {
    try {
      const response = await refreshTokenApi()

      if (response) {
        setAuthenticated(true)
      } else {
        // refresh token is invalid or expired
        setLogoutDialogMessage("Your session has expired, please log in again.")
        setLogoutReason(true)
      }
    } catch (err) {
      setLogoutDialogMessage("Unable to update session, please log in again.")
      setLogoutReason(true)
      setIsLoading(false)
    }
  }

  const isTokenExpired = (token) => {
    try {
      const { exp } = jwtDecode(token)
      const now = Date.now() / 1000
      const isExpired = exp < now
      return isExpired
    } catch (err) {
      return true // Token is invalid
    }
  }

  const logout = async () => {
    try {
      await logoutApi()
    } catch (err) {
    } finally {
      clearLocalStorage()
      setAuthenticated(false)
      setIsLoading(false)
      setPermissions([])
      window.location.href = "/login"
    }
  }

  const forceLogout = () => {
    clearLocalStorage()
    setAuthenticated(false)
    setIsLoading(false)
    setLogoutReason(false)
    setPermissions([])
    window.location.href = "/login"
  }

  const hideSystemNotificationDialog = () => {
    logout()
    setLogoutReason(false)
  }

  const contextValue = {
    forceLogout,
    set_authenticated,
    permissions,
    is_loading,
  }

  const confirmAlarmDialogFooter = (
    <React.Fragment>
      <div className="d-flex justify-content-end">
        <div className="d-flex">
          <div className="me-2">
            <Button
              label="Confirm"
              icon="pi pi-check"
              className="p-button-text func-btn"
              onClick={hideSystemNotificationDialog}
            />
          </div>
        </div>
      </div>
    </React.Fragment>
  )

  return (
    <TokenContext.Provider value={contextValue}>
      {children}
      {logout_reason && (
        <Dialog
          visible={true}
          className=""
          header="System"
          footer={confirmAlarmDialogFooter}
          onHide={hideSystemNotificationDialog}
        >
          <div>
            <b>{logout_dialog_message}</b>
          </div>
        </Dialog>
      )}
    </TokenContext.Provider>
  )
}

export const useToken = () => {
  const context = useContext(TokenContext)
  if (!context) {
    throw new Error("useToken must be used within a TokenProvider")
  }
  return context
}
