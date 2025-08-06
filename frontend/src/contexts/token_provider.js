import React, { createContext, useEffect, useContext, useState } from "react"
import { jwtDecode } from "jwt-decode"
import { refreshTokenApi, logoutApi } from "../api/auth"
import { Dialog } from "primereact/dialog"
import { Button } from "primereact/button"
import { clearLocalStorage } from "../utils/local_storage"

const TokenContext = createContext()

export const TokenProvider = ({ children }) => {
  const [set_authenticated, setAuthenticated] = useState(false)
  const [logout_reason, setLogoutReason] = useState(false)
  const [logout_dialog_message, setLogoutDialogMessage] = useState("")

  useEffect(() => {
    checkTokenStatus()
    const intervalId = setInterval(checkTokenStatus, 5 * 1 * 1000)

    return () => clearInterval(intervalId)
  }, [])

  const checkTokenStatus = async () => {
    const token = localStorage.getItem("access_token")

    if (!token) {
      return
    }

    if (isTokenExpired(token)) {
      refreshAccessToken()
    } else {
      setAuthenticated(true)
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
      window.location.href = "/login"
    }
  }

  const hideSystemNotificationDialog = () => {
    logout()
    setLogoutReason(false)
  }

  const contextValue = {
    set_authenticated,
    logout,
    refreshAccessToken,
    isTokenExpired,
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
