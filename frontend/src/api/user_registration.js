import axios from "axios"
import { parseDRFError } from "../utils/parse_error"

export const userRegistrationApi = (method, url, data = {}) => {
  const accessToken = localStorage.getItem("access_token")
  if (method == "get") {
    url = url + `?offset=${data.offset}&limit=${data.limit}`
  }
  return axios({
    method: method,
    url: `/api/user-registration${url}`,
    data: data,
    headers: {
      "Content-Type": "application/json",
      Authorization: accessToken,
    },
  })
    .then((response) => {
      return response
    })
    .catch((error) => {
      error.response.data = parseDRFError(error.response.data)
      throw error
    })
}
