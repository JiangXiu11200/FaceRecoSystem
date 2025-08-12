export const parseDRFError = (error) => {
  if (!error || typeof error !== "object") {
    return "An unknown error occurred."
  }

  const errorMessages = []

  for (const [field, messages] of Object.entries(error)) {
    if (Array.isArray(messages) && messages.length > 0) {
      errorMessages.push(`${field}: ${messages[0]}`)
    }
  }
  return errorMessages.join(", ") || "發生未知錯誤"
}
