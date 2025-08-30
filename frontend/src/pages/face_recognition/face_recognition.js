import React, { useCallback, useEffect, useRef, useState } from "react"

import { Button } from "primereact/button"
import { Toast } from "primereact/toast"

import "./face_recognition.css"

function FaceRecognition() {
  const toast = useRef(null)
  const log_content = useRef(null)
  const roi_scroll = useRef(null)
  const [roi_images, setROIImages] = useState([])

  const [isConnected, setIsConnected] = useState(false)
  const [isStreaming, setIsStreaming] = useState(false)
  const [videoFrame, setVideoFrame] = useState(null)
  const [logs, setLogs] = useState([])
  // const [fps, setFps] = useState(0)

  const ws = useRef(null)
  const reconnectTimeout = useRef(null)
  const pingInterval = useRef(null)
  const frameCount = useRef(0)
  const lastFrameTime = useRef(Date.now())
  let logCounter = 0

  const WS_URL = "ws://127.0.0.1:8001/ws" // FIXME: 透過環境變數或設定檔輸入

  const showToast = (severity, summary, detail, life = 3000) => {
    toast.current.show({ severity, summary, detail, life })
  }

  // 連接 WebSocket
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

        addLog("[System] Connection successful")
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
        addLog("[System] Connection error")
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

        addLog("[System] Service disconnected, attempting to reconnect...")
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

  const addLog = useCallback((message) => {
    logCounter++
    const logEntry = {
      id: logCounter,
      message,
    }

    setLogs((prev) => [...prev, logEntry].slice(-50))
  }, [])

  const handleDetectionLog = useCallback((detectionLogs) => {
    logCounter++
    const mergeLog =
      new Date(detectionLogs.timestamp).toLocaleString() +
      " Detection: " +
      detectionLogs.detection_results +
      " User name: " +
      detectionLogs.name

    const logEntry = {
      id: logCounter,
      message: mergeLog,
    }

    setLogs((prev) => [...prev, logEntry].slice(-50))
  }, [])

  useEffect(() => {
    if (log_content.current) {
      log_content.current.scrollTop = log_content.current.scrollHeight
    }
  }, [logs])

  useEffect(() => {
    if (roi_scroll.current) {
      roi_scroll.current.scrollLeft = roi_scroll.current.scrollWidth
    }
  }, [roi_images])

  // TODO: 辨識過的人臉 ROI 圖例
  // useEffect(() => {
  //   for (let i = 0; i < 10; i++) {
  //     setROIImages((prevImages) => [...prevImages, "/static/image/roi_not_found.jpg"])
  //   }
  // }, [])

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
      ws.current.send(JSON.stringify({ type: "start_detection" }))
      showToast("info", "Success", "Video stream has been started")
    } else {
      setIsStreaming(false)
      ws.current.send(JSON.stringify({ type: "stop_detection" }))
      showToast("info", "Success", "Video stream has been stopped")
    }
  }

  const handleMessage = useCallback((data) => {
    switch (data.type) {
      case "frame":
        setVideoFrame(`data:image/jpeg;base64,${data.data}`)
        // updateFPS()
        break

      case "log":
        handleDetectionLog(data.data)
        break

      case "status":
        addLog(data.message)
        break

      case "pong":
        break

      default:
        console.log("Unknown message type:", data.type)
    }
  }, [])

  const clearLogs = useCallback(() => {
    setLogs([])
    setVideoFrame(null)
    showToast("success", "Success", "All logs have been cleared")
  }, [])

  // const updateFPS = useCallback(() => {
  //   frameCount.current++
  //   const now = Date.now()
  //   const elapsed = now - lastFrameTime.current

  //   if (elapsed >= 1000) {
  //     const currentFps = Math.round((frameCount.current * 1000) / elapsed)
  //     setFps(currentFps)
  //     frameCount.current = 0
  //     lastFrameTime.current = now
  //   }
  // }, [])

  return (
    <div className="general-page-layout">
      <Toast ref={toast} />
      <div className="row g-2">
        <div className="col-md-8 col-12 image-container">
          <div className="video-stream mb-2">
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
          {/* TODO: 辨識過的人臉 ROI */}
          {/* <div>
            <div ref={roi_scroll} className="roi-container g-2">
              <div className="roi-scroll">
                {roi_images.map((item, index) => (
                  <div key={index} className="roi-item">
                    <img src={item} />
                  </div>
                ))}
              </div>
            </div>
          </div> */}
          <div className="d-flex justify-content-end">
            <div className="me-2">
              <Button
                className="p-button-info func-btn"
                label={isConnected ? "Disconnect" : "Connect"}
                icon={isConnected ? "pi pi-circle-fill" : "pi pi-circle"}
                onClick={() => connectToService()}
              />
            </div>
            <div className="me-2">
              <Button
                className="p-button-info func-btn"
                label={isStreaming ? "Stop Stream" : "Start Stream"}
                icon={isStreaming ? "pi pi-stop" : "pi pi-play"}
                onClick={() => controlStream()}
                disabled={!isConnected}
              />
            </div>
            <div>
              <Button
                className="p-button-info func-btn"
                label="Clear Logs"
                icon="pi pi-trash"
                onClick={() => clearLogs()}
                disabled={logs.length === 0 && !videoFrame}
              />
            </div>
          </div>
        </div>
        <div className="col-md-4 col-12 log-container">
          <div ref={log_content} className="log-panel">
            {logs.map((log) => (
              <div key={log.id}>{log.message}</div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default FaceRecognition
