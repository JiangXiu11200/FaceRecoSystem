import { useCallback, useEffect, useRef, useState } from "react"

import StreamManager from "../utils/stream_manager"

const useStream = (config = {}) => {
  const streamManagerRef = useRef(null)
  const [state, setState] = useState({
    isConnected: false,
    isStreaming: false,
    sessionId: null,
    playlistUrl: null,
    error: null,
  })

  // 初始化 StreamManager
  useEffect(() => {
    const manager = new StreamManager({
      ...config,
    })

    manager.on("onConnected", (data) => {
      setState((prev) => ({
        ...prev,
        isConnected: true,
        sessionId: data.sessionId,
        error: null,
      }))
    })

    manager.on("onDisconnected", () => {
      setState((prev) => ({
        ...prev,
        isConnected: false,
        isStreaming: false,
      }))
    })

    manager.on("onStreamStarted", (data) => {
      setState((prev) => ({
        ...prev,
        isStreaming: true,
        playlistUrl: data.playlist_url,
      }))
    })

    manager.on("onStreamStopped", () => {
      setState((prev) => ({
        ...prev,
        isStreaming: false,
        playlistUrl: null,
      }))
    })

    manager.on("onError", (error) => {
      setState((prev) => ({
        ...prev,
        error,
      }))
    })

    streamManagerRef.current = manager

    return () => {
      if (streamManagerRef.current) {
        streamManagerRef.current.disconnect()
      }
    }
  }, [])

  const connect = useCallback(async () => {
    if (streamManagerRef.current) {
      try {
        await streamManagerRef.current.connect()
        return true
      } catch (error) {
        return false
      }
    }
    return false
  }, [])

  const startStream = useCallback(() => {
    if (streamManagerRef.current) {
      return streamManagerRef.current.startStream()
    }
    return false
  }, [])

  const stopStream = useCallback(() => {
    if (streamManagerRef.current) {
      return streamManagerRef.current.stopStream()
    }
    return false
  }, [])

  const initPlayer = useCallback(
    async (videoElement) => {
      if (streamManagerRef.current && state.playlistUrl) {
        return await streamManagerRef.current.initHlsPlayer(
          videoElement,
          state.playlistUrl
        )
      }
      return false
    },
    [state.playlistUrl]
  )

  const captureFrame = useCallback(async (videoElement) => {
    if (streamManagerRef.current) {
      try {
        return await streamManagerRef.current.captureFrame(videoElement)
      } catch (error) {
        console.error("Capture failed:", error)
        return null
      }
    }
    return null
  }, [])

  return {
    ...state,
    connect,
    startStream,
    stopStream,
    initPlayer,
    captureFrame,
    getStatus: () => streamManagerRef.current?.getStreamStatus(),
    isReady: state.isConnected && state.isStreaming,
  }
}

export default useStream
