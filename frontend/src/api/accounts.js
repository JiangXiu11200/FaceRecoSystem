import axios from "axios"

import { parseDRFError } from "../utils/parse_error"

export const accountsAPI = (method, url, data) => {
  const headers = {}
  const isFormData = data instanceof FormData
  const accessToken = localStorage.getItem("access_token")

  if (!isFormData) {
    ;(headers["Authorization"] = accessToken),
      (headers["Content-Type"] = "application/json")
  } else {
    ;(headers["Authorization"] = accessToken),
      (headers["Content-Type"] = "multipart/form-data")
  }

  const config = {
    method,
    url: `/api/accounts${url}`,
    headers,
  }
  if (method.toLowerCase() === "get" || method.toLowerCase() === "delete") {
    config.params = data
  } else {
    config.data = data
  }

  return axios(config)
    .then((response) => {
      return response
    })
    .catch((error) => {
      if (error.response && error.response.data) {
        error.response.data = parseDRFError(error.response.data)
      }
      throw error
    })
}
