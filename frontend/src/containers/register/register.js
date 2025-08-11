import cloneDeep from "lodash/cloneDeep"
import { Button } from "primereact/button"
import { Dropdown } from "primereact/dropdown"
import { InputText } from "primereact/inputtext"
import { Toast } from "primereact/toast"
import React, { useEffect, useRef, useState } from "react"
import useStream from "../../hooks/use_stream"
import { cleanupObjectUrl, formatErrorMessage } from "../../utils/stream_tools"

import "./register.css"

function Register() {
  const toast = useRef(null)
  const videoRef = useRef(null)
  const stream = useStream({})
  const [hasScreenshot, setHasScreenshot] = useState(false)
  const [screenshotData, setScreenshotData] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const empty_user_details = {
    user_name: "",
    group: "",
  }
  const [new_user_details, setNewUserDetails] = useState(
    cloneDeep(empty_user_details)
  )
  const [user_groups, setUserGroups] = useState([])

  // Initialize websocket connection and stream.
  useEffect(() => {
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
      toast.current.show({
        severity: "success",
        summary: "Stream Started",
        detail: "Streaming is active",
      })
    }
  }, [stream.isStreaming, stream.playlistUrl])

  // Stream error handling
  useEffect(() => {
    if (stream.error) {
      toast.current.show({
        severity: "error",
        summary: "Error",
        detail: formatErrorMessage(stream.error),
      })
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

      toast.current.show({
        severity: "success",
        summary: "Screenshot",
        detail: "Screenshot captured successfully",
      })
    } else {
      toast.current.show({
        severity: "error",
        summary: "Error",
        detail: "Failed to capture screenshot",
      })
    }
  }

  // TODO: User registration logic, call API to register user with screenshot
  const handleRegister = async () => {
    if (!new_user_details.user_name.trim()) {
      toast.current.show({
        severity: "error",
        summary: "Validation Error",
        detail: "Please enter user name",
      })
      return
    }

    if (!hasScreenshot || !screenshotData) {
      toast.current.show({
        severity: "error",
        summary: "Validation Error",
        detail: "Please take a screenshot first",
      })
      return
    }

    setIsLoading(true)

    try {
      console.log("Registering user:", {
        user_name: new_user_details.user_name,
        group: new_user_details.group,
        session_id: stream.sessionId,
        image_size: screenshotData.blob.size,
      })

      setTimeout(() => {
        toast.current.show({
          severity: "success",
          summary: "Success",
          detail: "User registered successfully",
        })
        onClear()
      }, 1000)
    } catch (error) {
      console.error("Registration error:", error)
      toast.current.show({
        severity: "error",
        summary: "Registration Failed",
        detail: error.message || "Failed to register user",
      })
    } finally {
      setIsLoading(false)
    }
  }

  // Clear Screenshots
  const onClear = () => {
    setNewUserDetails(cloneDeep(empty_user_details))

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

      toast.current.show({
        severity: "info",
        summary: "Cleared",
        detail: "Screenshot cleared and stream restarted",
      })
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
    let _new_user_details = { ...new_user_details }
    _new_user_details[name] = value
    setNewUserDetails(_new_user_details)
  }

  const selectGroup = (e) => {
    setNewUserDetails({ ...new_user_details, group: e.value })
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

      <div className="buttonbar-layout">
        <div>
          <div className="form-group">
            <InputText
              className="h-100"
              id="user_name"
              name="user_name"
              value={new_user_details.user_name}
              keyfilter={/[^\s]/}
              placeholder="User Name"
              onChange={(e) => onInputChange(e, "user_name")}
              disabled={isLoading}
            />
          </div>
        </div>
        <div>
          <div className="form-group">
            <Dropdown
              className="h-100"
              value={new_user_details.group}
              optionLabel="name"
              optionValue="code"
              options={user_groups}
              onChange={(e) => selectGroup(e)}
              placeholder="Select Group"
              disabled={isLoading}
            />
          </div>
        </div>
        <div>
          <div className="form-group">
            <Button
              label="Screenshot"
              icon="pi pi-camera"
              className="p-button-info func-btn"
              onClick={() => handleScreenshot()}
              disabled={!stream.isReady || isLoading}
            />
          </div>
        </div>
        <div>
          <div className="form-group">
            <Button
              label={isLoading ? "Processing..." : "Register"}
              icon={isLoading ? "pi pi-spin pi-spinner" : "pi pi-check"}
              className="p-button-success func-btn"
              onClick={() => handleRegister()}
              disabled={!hasScreenshot || isLoading}
            />
          </div>
        </div>
        <div>
          <div className="form-group">
            <Button
              label="Clear"
              icon="pi pi-times"
              className="p-button-info func-btn"
              onClick={() => onClear()}
              disabled={isLoading}
            />
          </div>
        </div>
      </div>
    </div>
  )
}

export default Register
