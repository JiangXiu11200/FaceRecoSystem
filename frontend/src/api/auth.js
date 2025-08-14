import axios from "axios"
import { jwtDecode } from "jwt-decode"

import { clearLocalStorage, saveLocalStorage } from "../utils/local_storage"
import { parseError } from "../utils/parse_error"

export const refreshTokenApi = async () => {
  const accessToken = localStorage.getItem("access_token")
  return axios({
    method: "post",
    url: "/api/token/refresh/",

    headers: {
      "Content-Type": "application/json",
      Authorization: accessToken,
    },
    withCredentials: true,
  })
    .then((response) => {
      saveLocalStorage("access_token", response.data.access_token)
      return true
    })
    .catch((error) => {
      return false
    })
}

export const loginApi = (method, data) => {
  return axios({
    method: method,
    url: "/api/auth/login/",
    data: data,
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      const token = response.data.access_token
      const decoded = jwtDecode(token)
      const permissions = decoded.permissions || []
      saveLocalStorage("access_token", token)
      return permissions
    })
    .catch((error) => {
      throw error
    })
}

export const logoutApi = async () => {
  try {
    const accessToken = localStorage.getItem("access_token")
    const response = await axios({
      method: "post",
      url: "/api/auth/logout/",
      headers: {
        Authorization: accessToken,
      },
      withCredentials: true,
    })
    clearLocalStorage()
    return response
  } catch (error) {
    clearLocalStorage()
    console.error("Logout failed:", error.response?.data || error.message)
    throw error
  }
}
