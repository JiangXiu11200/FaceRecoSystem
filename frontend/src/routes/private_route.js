import React from "react"
import { Navigate, useLocation } from "react-router-dom"
import { useToken } from "../contexts/token_provider"

const PUBLIC_ROUTES = ["/login"]

export const PrivateRoute = ({ children }) => {
  const { forceLogout, set_authenticated, permissions, is_loading } = useToken()
  const location = useLocation() // Use useLocation hook instead of global location
  const isDevelopment = process.env.NODE_ENV === "development"
  const bypassAuth = process.env.REACT_APP_DEV_BYPASS_AUTH === "true"
  const isPublicRoute = PUBLIC_ROUTES.includes(location.pathname)
  const accessPathName =
    location.pathname === "/" ? "" : location.pathname.split("/")[1]

  if (isDevelopment && bypassAuth) {
    console.log("🔥 You are currently using developer mode!")
    return children
  }

  if (isPublicRoute) {
    return children
  }

  if (is_loading) {
    return (
      <div
        className="d-flex justify-content-center align-items-center"
        style={{ height: "100vh" }}
      >
        <div className="spinner-border me-2" role="status"></div>
        <span className="sr-only">Loading...</span>
      </div>
    )
  }

  if (!set_authenticated || !permissions || permissions.length === 0) {
    forceLogout()
    return <Navigate to="/login" replace />
  }

  if (location.pathname === "/") {
    if (permissions.includes("face-recognition")) {
      return children
    } else {
      return <Navigate to={`/${permissions[0]}`} replace />
    }
  }

  if (accessPathName && !permissions.includes(accessPathName)) {
    return <Navigate to={`/${permissions[0]}`} replace />
  }

  return children
}

export default PrivateRoute
