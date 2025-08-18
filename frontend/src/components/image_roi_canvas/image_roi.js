import React, { useEffect, useRef, useState } from "react"

const ImageROI = ({ image, image_width, image_height, detectionRange }) => {
  const canvasRef = useRef(null)
  const imgRef = useRef(null)
  const [points, setPoints] = useState([
    { x: 0, y: 0 },
    { x: 0, y: 0 },
  ])

  useEffect(() => {
    setPoints([
      { x: detectionRange.x1 || 0, y: detectionRange.y1 || 0 },
      { x: detectionRange.x2 || 0, y: detectionRange.y2 || 0 },
    ])
  }, [detectionRange])

  useEffect(() => {
    const img = imgRef.current
    if (!img.complete) {
      img.onload = () => drawCanvas()
    } else {
      drawCanvas()
    }
  }, [points, image])

  const drawCanvas = () => {
    const canvas = canvasRef.current
    const ctx = canvas.getContext("2d")
    const img = imgRef.current

    if (!img || !canvas) return

    const canvasWidth = img.clientWidth
    const canvasHeight = img.clientHeight

    canvas.width = canvasWidth
    canvas.height = canvasHeight
    const scaleX = canvasWidth / image_width
    const scaleY = canvasHeight / image_height

    const topLeft = {
      x: points[0].x * scaleX,
      y: points[0].y * scaleY,
    }
    const bottomRight = {
      x: points[1].x * scaleX,
      y: points[1].y * scaleY,
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height)

    ctx.strokeStyle = "red"
    ctx.lineWidth = 2
    ctx.strokeRect(
      topLeft.x,
      topLeft.y,
      bottomRight.x - topLeft.x,
      bottomRight.y - topLeft.y
    )

    const corners = [topLeft, bottomRight]

    corners.forEach((pt, idx) => {
      ctx.beginPath()
      ctx.arc(pt.x, pt.y, 2, 0, 2 * Math.PI)
      ctx.fillStyle = "red"
      ctx.fill()
      ctx.fillStyle = "red"
      ctx.font = "bold 16px Arial"
      ctx.fillText(idx === 0 ? "(x1, y1)" : "(x2, y2)", pt.x + 5, pt.y - 5)
      ctx.strokeStyle = "yellow"
      ctx.lineWidth = 1
      ctx.strokeText(idx === 0 ? "(x1, y1)" : "(x2, y2)", pt.x + 5, pt.y - 5)
    })
  }

  return (
    <div style={{ position: "relative", display: "inline-block" }}>
      <img
        ref={imgRef}
        src={image || "/image/not_found.jpg"}
        alt="roi_canvas"
        style={{ display: "block", width: "100%", height: "auto" }}
      />
      <canvas
        ref={canvasRef}
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          pointerEvents: "none",
        }}
      />
    </div>
  )
}

export default ImageROI