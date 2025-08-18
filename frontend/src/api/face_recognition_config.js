import axios from "axios"

import { parseDRFError } from "../utils/parse_error"

export const faceRecognitionConfigApi = (method, url, data = {}) => {
  const accessToken = localStorage.getItem("access_token")

  const headers = {
    Authorization: accessToken,
    "Content-Type": "application/json",
  }

  const config = {
    method,
    url: `/api/face-recognition-config${url}`,
    headers,
    data: data,
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
