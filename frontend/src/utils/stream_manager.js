import Hls from "hls.js"

class StreamManager {
  constructor(config = {}) {
    this.ws = null
    this.hls = null
    this.sessionId = null
    this.isConnected = false
    this.isStreaming = false

    this.config = {
      wsBaseUrl: config.wsBaseUrl || "ws://localhost:8000/ws/stream",
      httpBaseUrl: config.httpBaseUrl || "http://localhost:8000",
      token: config.token || localStorage.getItem("access_token") || "",
      debug: config.debug || false,
      ...config,
    }
    console.log("StreamManager initialized with config:", this.config)

    this.callbacks = {
      onConnected: null,
      onDisconnected: null,
      onStreamStarted: null,
      onStreamStopped: null,
      onError: null,
      onMessage: null,
    }
  }

  generateSessionId() {
    return `session_${Date.now()}_${Math.random().toString(36).substring(7)}`
  }

  connect() {
    return new Promise((resolve, reject) => {
      try {
        this.sessionId = this.generateSessionId()
        const wsUrl = `${this.config.wsBaseUrl}/${this.sessionId}/?token=${this.config.token}`

        if (this.config.debug) {
          console.log("[Debug] Connecting to WebSocket:", wsUrl)
        }

        this.ws = new WebSocket(wsUrl)

        this.ws.onopen = () => {
          this.isConnected = true
          if (this.config.debug) {
            console.log("[Debug] WebSocket connected")
          }
          this.triggerCallback("onConnected", { sessionId: this.sessionId })
          resolve({ success: true, sessionId: this.sessionId })
        }

        this.ws.onmessage = (event) => {
          const data = JSON.parse(event.data)
          if (this.config.debug) {
            console.log("[Debug] WebSocket message:", data)
          }
          this.handleMessage(data)
        }

        this.ws.onerror = (error) => {
          console.error("[Debug] WebSocket error:", error)
          this.isConnected = false
          this.isStreaming = false
          this.triggerCallback("onError", { type: "connection", error })
          reject(error)
        }

        this.ws.onclose = () => {
          if (this.config.debug) {
            console.log("[Debug] WebSocket disconnected")
          }
          this.isConnected = false
          this.isStreaming = false
          this.triggerCallback("onDisconnected")
        }
      } catch (error) {
        console.error("Failed to initialize WebSocket:", error)
        reject(error)
      }
    })
  }

  handleMessage(data) {
    this.triggerCallback("onMessage", data)

    switch (data.type) {
      case "connection_established":
        if (this.config.debug) {
          console.log("[Debug] Session established:", data.session_id)
        }
        break

      case "stream_started":
        this.isStreaming = true
        this.triggerCallback("onStreamStarted", data)
        break

      case "stream_stopped":
        this.isStreaming = false
        this.triggerCallback("onStreamStopped", data)
        break

      case "stream_status":
        this.isStreaming = data.is_ready
        if (data.is_ready && data.playlist_url) {
          this.triggerCallback("onStreamStarted", data)
        }
        break

      case "error":
        console.error("Server error:", data.message)
        this.triggerCallback("onError", {
          type: "server",
          message: data.message,
        })
        break

      default:
        if (this.config.debug) {
          console.log("[Debug] Unknown message type:", data.type)
        }
    }
  }

  sendCommand(command, params = {}) {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      console.error("WebSocket is not connected")
      return false
    }

    const message = JSON.stringify({ command, ...params })
    if (this.config.debug) {
      console.log("[Debug] Sending command:", message)
    }
    this.ws.send(message)
    return true
  }

  startStream() {
    if (this.isStreaming) {
      if (this.config.debug) {
        console.log("[Debug] Stream already running, skipping start command")
      }
      return false
    }

    return this.sendCommand("start_stream")
  }

  stopStream() {
    const result = this.sendCommand("stop_stream")
    if (this.hls) {
      this.destroyHlsPlayer()
    }
    return result
  }

  getStreamStatus() {
    return this.sendCommand("get_status")
  }

  async waitForPlaylist(url, retries = 30, delay = 1000) {
    for (let i = 0; i < retries; i++) {
      try {
        const res = await fetch(url, { method: "HEAD" })
        if (res.ok) {
          if (this.config.debug) {
            console.log(`[Debug] Playlist found at attempt ${i + 1}`)
          }
          return true
        }
      } catch (e) {
        if (this.config.debug) {
          console.error(`[Debug] Error checking playlist: ${e.message}`)
        }
      }

      if (this.config.debug) {
        console.log(`[Debug] Waiting for playlist... (${i + 1}/${retries})`)
      }
      await new Promise((resolve) => setTimeout(resolve, delay))
    }
    return false
  }

  async initHlsPlayer(videoElement, playlistUrl) {
    if (!videoElement || !playlistUrl) {
      console.error("Video element or playlist URL missing")
      return false
    }

    const fullUrl = `${this.config.httpBaseUrl}${playlistUrl}`

    if (this.config.debug) {
      console.log("[Debug] Initializing HLS player with URL:", fullUrl)
    }

    const exists = await this.waitForPlaylist(fullUrl)
    if (!exists) {
      console.error("Playlist not ready after waiting")
      this.triggerCallback("onError", {
        type: "hls",
        message: "Playlist not available",
      })
      return false
    }

    if (Hls.isSupported()) {
      if (this.hls) {
        this.hls.destroy()
      }

      // Create a new HLS instance
      this.hls = new Hls({
        debug: this.config.debug,
        manifestLoadingMaxRetry: 10,
        manifestLoadingRetryDelay: 1000,
        fragLoadingMaxRetry: 10,
        fragLoadingRetryDelay: 1000,
        // Low latency settings
        liveSyncDurationCount: 3,
        liveMaxLatencyDurationCount: 10,
        liveDurationInfinity: true,
        highBufferWatchdogPeriod: 1,
      })

      this.hls.loadSource(fullUrl)
      this.hls.attachMedia(videoElement)

      // HLS 事件處理
      this.hls.on(Hls.Events.MANIFEST_PARSED, () => {
        if (this.config.debug) {
          console.log("[Debug] HLS manifest parsed")
        }
        videoElement.play().catch((e) => {
          console.log("Auto-play failed:", e)
        })
      })

      this.hls.on(Hls.Events.ERROR, (event, data) => {
        console.error("HLS error:", data)
        if (data.fatal) {
          this.handleHlsError(data)
        }
      })

      return true
    } else if (videoElement.canPlayType("application/vnd.apple.mpegurl")) {
      // iOS Safari can play HLS natively
      videoElement.src = fullUrl
      videoElement.addEventListener("loadedmetadata", () => {
        videoElement.play()
      })
      return true
    }

    return false
  }

  handleHlsError(data) {
    switch (data.type) {
      case Hls.ErrorTypes.NETWORK_ERROR:
        console.log("Network error, trying to recover...")
        this.hls.startLoad()
        break
      case Hls.ErrorTypes.MEDIA_ERROR:
        console.log("Media error, trying to recover...")
        this.hls.recoverMediaError()
        break
      default:
        console.error("Fatal error, destroying HLS")
        this.destroyHlsPlayer()
        this.triggerCallback("onError", {
          type: "hls_fatal",
          error: data,
        })
        break
    }
  }

  destroyHlsPlayer() {
    if (this.hls) {
      this.hls.destroy()
      this.hls = null
    }
  }

  captureFrame(videoElement, quality = 0.9) {
    return new Promise((resolve, reject) => {
      if (!videoElement) {
        reject(new Error("Video not ready for capture"))
        return
      }

      const canvas = document.createElement("canvas")
      canvas.width = videoElement.videoWidth || 1280
      canvas.height = videoElement.videoHeight || 720

      const ctx = canvas.getContext("2d")
      ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height)

      canvas.toBlob(
        (blob) => {
          if (blob) {
            const imageUrl = URL.createObjectURL(blob)
            resolve({
              blob,
              url: imageUrl,
              width: canvas.width,
              height: canvas.height,
            })
          } else {
            reject(new Error("Failed to capture frame"))
          }
        },
        "image/jpeg",
        quality
      )
    })
  }

  // Register event listeners
  on(event, callback) {
    if (this.callbacks.hasOwnProperty(event)) {
      this.callbacks[event] = callback
    }
  }

  // Trigger event callbacks
  triggerCallback(event, data = null) {
    if (this.callbacks[event] && typeof this.callbacks[event] === "function") {
      this.callbacks[event](data)
    }
  }

  disconnect() {
    if (this.config.debug) {
      console.log("[Debug] Cleaning up StreamManager...")
    }

    if (this.isStreaming) {
      this.stopStream()
    }

    if (this.ws) {
      if (this.ws.readyState === WebSocket.OPEN) {
        this.ws.close()
      }
      this.ws = null
    }

    this.destroyHlsPlayer()

    this.isConnected = false
    this.isStreaming = false
    this.sessionId = null
  }

  getState() {
    return {
      sessionId: this.sessionId,
      isConnected: this.isConnected,
      isStreaming: this.isStreaming,
      wsState: this.ws ? this.ws.readyState : null,
    }
  }
}

export default StreamManager
