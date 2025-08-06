export const saveLocalStorage = (key, data) => {
  try {
    localStorage.setItem(key, data)
    return true
  } catch (err) {
    return false
  }
}

export const clearLocalStorage = () => {
  try {
    localStorage.clear()
    return true
  } catch (err) {
    return false
  }
}
