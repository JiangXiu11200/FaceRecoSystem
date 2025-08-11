import axios from "axios"


export const userRegistrationApi = (method, url, data = {}) => {
  const accessToken = localStorage.getItem("access_token")
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
      throw error
    })
}
