import React from "react"
import { Navigate } from "react-router-dom"
import { useToken } from "../contexts/token_provider"

const PUBLIC_ROUTES = ["/login"]

export const PrivateRoute = ({ children }) => {
  const { forceLogout, set_authenticated, is_loading } = useToken()

  const isPublicRoute = PUBLIC_ROUTES.includes(location.pathname)

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

  if (!set_authenticated) {
    forceLogout()
    return <Navigate to="/login" />
  }

  return <React.Fragment>{children}</React.Fragment>
}

export default PrivateRoute
