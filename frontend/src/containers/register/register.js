import React, { useEffect, useRef, useState, useCallback } from "react"
import cloneDeep from "lodash/cloneDeep"
import { Button } from "primereact/button"
import { Dropdown } from "primereact/dropdown"
import { InputText } from "primereact/inputtext"
import { Toast } from "primereact/toast"
import useStream from "../../hooks/use_stream"
import { cleanupObjectUrl, formatErrorMessage } from "../../utils/stream_tools"
import { userRegistrationApi } from "../../api/user_registration"
import "./register.css"

const EMPTY_USER_DETAILS = {
  user_name: "",
  group: "",
}

function Register() {
  const toast = useRef(null)
  const videoRef = useRef(null)
  const stream = useStream({})
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
    const initStream = async () => {
      const connected = await stream.connect()
      if (connected) {
        stream.startStream()
      }
    }
    initStream()
    return () => {
      if (screenshotData?.url) {
        cleanupObjectUrl(screenshotData.url)
      }
    }
  }, [])

  // Handle stream connection and disconnection
  useEffect(() => {
    if (stream.isStreaming && videoRef.current && stream.playlistUrl) {
      stream.initPlayer(videoRef.current)
      showToast("success", "Stream Started", "Video stream is now live")
    }
  }, [stream.isStreaming, stream.playlistUrl])

  // Stream error handling
  useEffect(() => {
    if (stream.error) {
      showToast("error", "Stream Error", formatErrorMessage(stream.error))
    }
  }, [stream.error])

  // Check for stream status
  useEffect(() => {
    if (stream.isConnected && !stream.isStreaming && !hasScreenshot) {
      const interval = setInterval(() => {
        stream.getStatus()
      }, 5000)

      return () => clearInterval(interval)
    }
  }, [stream.isConnected, stream.isStreaming, hasScreenshot])

  const handleScreenshot = async () => {
    if (!videoRef.current) {
      toast.current.show({
        severity: "warn",
        summary: "Warning",
        detail: "Video stream not ready",
      })
      return
    }

    const frameData = await stream.captureFrame(videoRef.current)

    if (frameData) {
      stream.stopStream()
      setScreenshotData(frameData)
      setHasScreenshot(true)
      videoRef.current.poster = frameData.url

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

    const formData = new FormData()
    formData.append(
      "image",
      screenshotData.blob,
      `${newUserDetails.user_name}.jpg`
    )
    formData.append("name", newUserDetails.user_name)
    formData.append("register_group", newUserDetails.group)

    userRegistrationApi("post", "/", formData, true)
      .then((response) => {
        showToast("success", "Success", "User registered successfully")
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
      if (screenshotData?.url) {
        cleanupObjectUrl(screenshotData.url)
      }
      setScreenshotData(null)
      setHasScreenshot(false)

      if (videoRef.current) {
        videoRef.current.poster = ""
      }

      stream.startStream()

      showToast("info", "Cleared", "Screenshot cleared and stream restarted")
    } else {
      toast.current.show({
        severity: "info",
        summary: "Cleared",
        detail: "Form cleared",
      })
    }
  }

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
        <video
          ref={videoRef}
          className="video-element"
          crossOrigin="anonymous"
          autoPlay
          playsInline
          muted
          style={{
            width: "100%",
            height: "100%",
            objectFit: "contain",
            backgroundColor: "#000",
          }}
        />
      </div>

      <div className="row g-2">
        <div className="col-3">
          <div className="form-group">
            <InputText
              className="h-100"
              id="user_name"
              name="user_name"
              value={newUserDetails.user_name}
              keyfilter={/[^\s]/}
              placeholder="User Name"
              onChange={(e) => onInputChange(e, "user_name")}
              disabled={isLoading}
            />
          </div>
        </div>
        <div className="col-2">
          <div className="form-group">
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
        </div>
        <div className="col-7">
          <div className="d-flex flex-wrap justify-content-start gap-2">
            <div className="form-group">
              <Button
                label="Screenshot"
                icon="pi pi-camera"
                className="p-button-info func-btn"
                onClick={() => handleScreenshot()}
                disabled={!stream.isReady || isLoading}
              />
            </div>
            <div className="form-group">
              <Button
                label={isLoading ? "Processing..." : "Register"}
                icon={isLoading ? "pi pi-spin pi-spinner" : "pi pi-check"}
                className="p-button-success func-btn"
                onClick={() => handleRegister()}
                disabled={!hasScreenshot || isLoading}
              />
            </div>
            <div className="form-group">
              <Button
                label="Clear"
                icon="pi pi-times"
                className="p-button-info func-btn"
                onClick={() => handleClear()}
                disabled={isLoading}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Register
