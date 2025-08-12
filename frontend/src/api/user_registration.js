import axios from "axios"
import { parseDRFError } from "../utils/parse_error"

export const userRegistrationApi = (
  method,
  url,
  data = {},
  isFormData = false
) => {
  const accessToken = localStorage.getItem("access_token")

  const headers = {
    Authorization: accessToken,
  }

  if (!isFormData) {
    headers["Content-Type"] = "application/json"
  }

  const config = {
    method,
    url: `/api/user-registration${url}`,
    headers,
  }

  if (method.toLowerCase() === "get" || method.toLowerCase() === "delete") {
    config.params = data
  } else {
    config.data = data
  }

  return axios(config)
    .then((response) => response)
    .catch((error) => {
      if (error.response && error.response.data) {
        error.response.data = parseDRFError(error.response.data)
      }
      throw error
    })
}
