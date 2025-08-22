import React, { useCallback, useEffect, useRef, useState } from "react"

import cloneDeep from "lodash/cloneDeep"
import { Button } from "primereact/button"
import { Dropdown } from "primereact/dropdown"
import { InputText } from "primereact/inputtext"
import { Toast } from "primereact/toast"

import { userRegistrationApi } from "../../api/user_registration"

import "./user_register.css"

const EMPTY_USER_DETAILS = {
  user_name: "",
  group: "",
}

function RegisterFace() {
  const toast = useRef(null)

  const WS_URL = "ws://127.0.0.1:8001/ws" // FIXME: 透過環境變數或設定檔輸入

  const [isConnected, setIsConnected] = useState(false)
  const [isStreaming, setIsStreaming] = useState(false)
  const [videoFrame, setVideoFrame] = useState(null)

  const ws = useRef(null)
  const reconnectTimeout = useRef(null)
  const pingInterval = useRef(null)

  const [hasScreenshot, setHasScreenshot] = useState(false)
  const [screenshotData, setScreenshotData] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [newUserDetails, setNewUserDetails] = useState(
    cloneDeep(EMPTY_USER_DETAILS)
  )
  const [userGroups, setUserGroups] = useState([])

  const showToast = (severity, summary, detail, life = 3000) => {
    toast.current.show({ severity, summary, detail, life })
  }

  const fetchGroups = () => {
    userRegistrationApi("get", "/group/")
      .then((response) => {
        const groups = response.data.results.map((group) => ({
          name: group.group_name,
          code: group.id,
        }))
        setUserGroups(groups)
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  // Initialize websocket connection and stream.
  useEffect(() => {
    fetchGroups()
  }, [])

  const handleScreenshot = async () => {
    if (!videoFrame) {
      showToast("warn", "Warning", "Video stream not ready")
      return
    }

    if (videoFrame) {
      setScreenshotData(videoFrame)
      setHasScreenshot(true)
      stopStream()

      showToast("success", "Screenshot", "Screenshot taken successfully")
    } else {
      showToast("error", "Error", "Failed to capture screenshot")
    }
  }

  const handleRegister = async () => {
    if (!newUserDetails.user_name.trim()) {
      showToast("error", "Validation Error", "Please enter user name")
      return
    }

    if (!hasScreenshot || !screenshotData) {
      showToast("error", "Please take a screenshot first")
      return
    }

    setIsLoading(true)

    const data = {
      register_group: newUserDetails.group,
      name: newUserDetails.user_name,
      image: screenshotData,
    }

    userRegistrationApi("post", "/", data, true)
      .then((response) => {
        showToast("success", "Success", "User registered successfully")
        handleClear()
      })
      .catch((error) => {
        showToast("error", "Error", error.response.data)
      })
      .finally(() => {
        setIsLoading(false)
      })
  }

  const handleClear = () => {
    setNewUserDetails(cloneDeep(EMPTY_USER_DETAILS))

    if (hasScreenshot) {
      setScreenshotData(null)
      setVideoFrame(null)
      setHasScreenshot(false)
      showToast("success", "Success", "Screenshot cleared")
    } else {
      toast.current.show({
        severity: "info",
        summary: "Cleared",
        detail: "Form cleared",
      })
    }
  }

  const connectWebSocket = useCallback(() => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      return
    }

    try {
      ws.current = new WebSocket(WS_URL)

      ws.current.onopen = () => {
        setIsConnected(true)

        if (reconnectTimeout.current) {
          clearTimeout(reconnectTimeout.current)
        }

        // Heartbeat ping
        pingInterval.current = setInterval(() => {
          if (ws.current?.readyState === WebSocket.OPEN) {
            ws.current.send(JSON.stringify({ type: "ping" }))
          }
        }, 30000)
      }

      ws.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          handleMessage(data)
        } catch (error) {
          console.error("Failed to parse message:", error)
        }
      }

      ws.current.onerror = (error) => {
        console.error("WebSocket error:", error)
      }

      ws.current.onclose = () => {
        console.log("WebSocket disconnected")
        setIsConnected(false)
        setVideoFrame(null)

        if (pingInterval.current) {
          clearInterval(pingInterval.current)
        }

        reconnectTimeout.current = setTimeout(() => {
          console.log("Attempting to reconnect...")
          connectWebSocket()
        }, 5000)
      }
    } catch (error) {
      console.log("Failed to create WebSocket:", error)
    }
  }, [])

  const disconnectWebSocket = useCallback(() => {
    if (reconnectTimeout.current) {
      clearTimeout(reconnectTimeout.current)
    }

    if (pingInterval.current) {
      clearInterval(pingInterval.current)
    }

    if (ws.current) {
      ws.current.close()
      ws.current = null
    }

    setIsConnected(false)
    setVideoFrame(null)
  }, [])

  useEffect(() => {
    return () => {
      disconnectWebSocket()
    }
  }, [])

  const connectToService = () => {
    if (isConnected) {
      disconnectWebSocket()
      showToast("info", "Info", "WebSocket connection closed")
    } else {
      connectWebSocket()
      showToast("info", "Info", "WebSocket connection established")
    }
  }

  const controlStream = () => {
    if (!isStreaming) {
      setIsStreaming(true)
      ws.current.send(JSON.stringify({ type: "start_video_stream" }))
      showToast("info", "Success", "Video stream has been started")
    } else {
      setIsStreaming(false)
      ws.current.send(JSON.stringify({ type: "stop_video_stream" }))
      showToast("info", "Success", "Video stream has been stopped")
    }
  }

  const stopStream = () => {
    if (isStreaming) {
      setIsStreaming(false)
      ws.current.send(JSON.stringify({ type: "stop_video_stream" }))
    }
  }

  const handleMessage = useCallback((data) => {
    switch (data.type) {
      case "frame":
        setVideoFrame(`data:image/jpeg;base64,${data.data}`)
        // updateFPS()
        break

      case "pong":
        break

      default:
        console.log("Unknown message type:", data.type)
    }
  }, [])

  const onInputChange = (e, name) => {
    const value = (e.target && e.target.value) || ""
    let _new_user_details = { ...newUserDetails }
    _new_user_details[name] = value
    setNewUserDetails(_new_user_details)
  }

  return (
    <div className="content-layout">
      <Toast ref={toast} />
      <div className="image-layout">
        {videoFrame ? (
          <img src={videoFrame} alt="video_stream" />
        ) : (
          <img
            style={{
              width: "100%",
              height: "100%",
              objectFit: "contain",
              backgroundColor: "#000",
            }}
          />
        )}
      </div>

      <div className="row g-2 align-items-center">
        <div className="col-3">
          <InputText
            id="user_name"
            name="user_name"
            value={newUserDetails.user_name}
            keyfilter={/[^\s]/}
            placeholder="User Name"
            onChange={(e) => onInputChange(e, "user_name")}
            disabled={isLoading}
          />
        </div>
        <div className="col-2">
          <Dropdown
            className="w-100"
            value={newUserDetails.group}
            optionLabel="name"
            optionValue="code"
            options={userGroups}
            onChange={(e) => onInputChange(e, "group")}
            placeholder="Select Group"
            disabled={isLoading}
          />
        </div>
        <div className="col-7">
          <div className="d-flex flex-wrap justify-content-start gap-2">
            <Button
              label="Screenshot"
              icon="pi pi-camera"
              className="p-button-info func-btn"
              onClick={() => handleScreenshot()}
              disabled={!videoFrame || hasScreenshot}
            />
            <Button
              label={isLoading ? "Processing..." : "Register"}
              icon={isLoading ? "pi pi-spin pi-spinner" : "pi pi-check"}
              className="p-button-success func-btn"
              onClick={() => handleRegister()}
              disabled={!hasScreenshot}
            />
            <Button
              label="Clear"
              icon="pi pi-times"
              className="p-button-info func-btn"
              onClick={() => handleClear()}
              disabled={!hasScreenshot}
            />
            <Button
              label={isStreaming ? "Stop Stream" : "Start Stream"}
              icon={isStreaming ? "pi pi-stop" : "pi pi-play"}
              className="p-button-info func-btn"
              onClick={() => controlStream()}
              disabled={!isConnected}
            />
            <div className="me-2">
              <Button
                className="p-button-info func-btn"
                label={isConnected ? "Disconnect" : "Connect"}
                icon={isConnected ? "pi pi-circle-fill" : "pi pi-circle"}
                onClick={() => connectToService()}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default RegisterFace
