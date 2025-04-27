import React, { useRef, useEffect, useState } from "react"

import "./face_recognition.css"

function FaceRecognition() {
  const log_content = useRef(null)
  const roi_scroll = useRef(null)
  const [logs, setLogs] = useState([])
  const [roi_images, setROIImages] = useState([])

  // TAG: This is a mock data for testing
  useEffect(() => {
    // const interval = setInterval(() => {
    //     setROIImages((prevImages) => [...prevImages, "./image/roi_not_found.jpg"])
    // }, 1000)
    // return () => clearInterval(interval)
    for (let i = 0; i < 10; i++) {
      setROIImages((prevImages) => [
        ...prevImages,
        "./assets/assets/image/roi_not_found.jpg",
      ])
    }
  }, [])

  // useEffect(() => {
  //     const interval = setInterval(() => {
  //         setLogs((prevLogs) => {
  //             const newLogs = [
  //                 ...prevLogs,
  //                 `${new Date().toLocaleTimeString()} [DEBUG] : Minimum euclidean distance: ${prevLogs.length + 1} (mock data)`,
  //             ]
  //             return newLogs.length > 50 ? newLogs.slice(newLogs.length - 50) : newLogs
  //         })
  //     }, 200)

  //     return () => clearInterval(interval)
  // }, [])

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

  return (
    <div className="container-fluid p-2">
      <div className="row g-2">
        <div className="col-md-7 col-12 image-container">
          <div className="row g-2">
            <div>
              <img src="./assets/image/not_found.jpg" alt="video_stream" />
            </div>
            <div>
              <div ref={roi_scroll} className="roi-container g-2">
                <div className="roi-scroll">
                  {roi_images.map((item, index) => (
                    <div key={index} className="roi-item">
                      <img src={item} />
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="col-md-5 col-12 log-container">
          <div ref={log_content} className="log-panel">
            {logs.map((log, index) => (
              <div key={index} className="log-item">
                {log}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default FaceRecognition
