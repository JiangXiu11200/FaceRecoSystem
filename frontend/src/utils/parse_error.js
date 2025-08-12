export const parseDRFError = (error) => {
  if (!error || typeof error !== "object") {
    return "An unknown error occurred. (error01)"
  }

  if (error.error && typeof error.error === "string") {
    return error.error
  }

  const errorMessages = []
  for (const [field, messages] of Object.entries(error)) {
    if (Array.isArray(messages) && messages.length > 0) {
      errorMessages.push(`${field}: ${messages[0]}`)
    }
  }
  return errorMessages.join(", ") || "An unknown error occurred. (error02)"
}
