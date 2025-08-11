export const blobToBase64 = (blob) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onloadend = () => resolve(reader.result)
    reader.onerror = reject
    reader.readAsDataURL(blob)
  })
}

// export const createRegistrationFormData = (userData, sessionId, imageBlob) => {
//   const formData = new FormData()
//   formData.append("user_name", userData.user_name)
//   formData.append("group", userData.group)
//   formData.append("session_id", sessionId)
//   formData.append("image", imageBlob, "screenshot.jpg")
//   return formData
// }

export const cleanupObjectUrl = (url) => {
  if (url && url.startsWith("blob:")) {
    URL.revokeObjectURL(url)
  }
}

export const checkBrowserSupport = () => {
  const support = {
    websocket: "WebSocket" in window,
    mediaDevices: !!(
      navigator.mediaDevices && navigator.mediaDevices.getUserMedia
    ),
    hls: window.Hls && Hls.isSupported(),
    canvas: !!document.createElement("canvas").getContext,
  }

  const isSupported = Object.values(support).every((v) => v)

  return {
    ...support,
    isSupported,
  }
}

export const formatErrorMessage = (error) => {
  if (typeof error === "string") {
    return error
  }

  if (error.message) {
    return error.message
  }

  if (error.type === "connection") {
    return "Cannot connect to the streaming server."
  }

  if (error.type === "hls") {
    return "Loading streaming data failed."
  }

  return "An unknown error occurred."
}
