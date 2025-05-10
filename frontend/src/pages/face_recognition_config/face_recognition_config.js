import { cloneDeep } from "lodash"
import { Button } from "primereact/button"
import { Card } from "primereact/card"
import { InputText } from "primereact/inputtext"
import { SelectButton } from "primereact/selectbutton"
import { Toast } from "primereact/toast"
import React, { useEffect, useMemo, useRef, useState } from "react"

import ImageROI from "../../components/image_roi_canvas/image_roi"

import "./face_recognition_config.css"

function FaceRecognitionConfig() {
  const toast = useRef(null)
  const [set_debug_state, setDebugState] = useState(0)
  const [set_image, setImage] = useState(null)
  const empty_detection_range = {
    x1: 0,
    y1: 0,
    x2: 0,
    y2: 0,
  }
  const [detection_range, setDetectionRange] = useState(
    cloneDeep(empty_detection_range)
  )

  const debug_state = useMemo(() => {
    return [
      { code: 0, name: "OFF" },
      { code: 1, name: "NO" },
    ]
  }, [])

  const onDebugStateChange = (e) => {
    setDebugState(e.value)
  }

  useEffect(() => {
    console.log(detection_range)
  }, [detection_range])

  const onDetectionRangeChange = (e, name) => {
    const value = (e.target && e.target.value) || ""
    let _detectionRange = { ...detection_range }
    if (value < 0) {
      toast.current.show({
        severity: "warn",
        summary: "Warning",
        detail: `${name} must be greater than 0`,
      })
      return
    }
    if (name === "x2" && value < _detectionRange.x1) {
      toast.current.show({
        severity: "warn",
        summary: "Warning",
        detail: "x2 must be greater than x1",
      })
      return
    }
    if (name === "y2" && value < _detectionRange.y1) {
      toast.current.show({
        severity: "warn",
        summary: "Warning",
        detail: "y2 must be greater than y1",
      })
      return
    }
    if (name === "x1" && value < _detectionRange.x2) {
      toast.current.show({
        severity: "warn",
        summary: "Warning",
        detail: "x1 must be less than x2",
      })
      return
    }
    if (name === "y1" && value < _detectionRange.y2) {
      toast.current.show({
        severity: "warn",
        summary: "Warning",
        detail: "y1 must be less than y2",
      })
      return
    }

    _detectionRange[name] = value
    setDetectionRange(_detectionRange)
  }

  const video_footer = (
    <div className="d-flex d-flex-row justify-content-end">
      <Button
        icon="pi pi-eye"
        className="func-btn"
        label="Preview"
        onClick={() => {
          toast.current.show({
            severity: "info",
            summary: "Preview",
            detail: "Preview is not available yet.",
          })
        }}
      />
    </div>
  )

  const reco_footer = (
    <div className="d-flex d-flex-row justify-content-end">
      <Button
        icon="pi pi-check"
        className="func-btn"
        label="Apply"
        onClick={() => {
          toast.current.show({
            severity: "info",
            summary: "Save",
            detail: "Apply is not available yet.",
          })
        }}
      />
    </div>
  )

  return (
    <div className="container-layout general-page-layout">
      <Toast ref={toast} />
      <div className="facereco-content">
        <div className="col-5 col-lg-5">
          <Card
            className="config-card-container"
            title="Video"
            footer={video_footer}
          >
            <div>
              <label className="">RTSP</label>
              <InputText className="input-container" placeholder="" />
            </div>
            <div className="d-flex d-flex-row gap-2">
              <div className="w-100">
                <label className="">Width</label>
                <InputText className="input-container" placeholder="" />
              </div>
              <div className="w-100">
                <label className="">Height</label>
                <InputText className="input-container" placeholder="" />
              </div>
            </div>
            <div>
              <label className="item-title">Detection Range</label>
            </div>
            <div className="d-flex d-flex-row gap-2">
              <div className="w-100">
                <label className="">x1</label>
                <InputText
                  className="input-container"
                  onChange={(e) => onDetectionRangeChange(e, "x1")}
                  placeholder=""
                />
              </div>
              <div className="w-100">
                <label className="">y1</label>
                <InputText
                  className="input-container"
                  onChange={(e) => onDetectionRangeChange(e, "y1")}
                  placeholder=""
                />
              </div>
              <div className="w-100">
                <label className="">x2</label>
                <InputText
                  className="input-container"
                  onChange={(e) => onDetectionRangeChange(e, "x2")}
                  placeholder=""
                />
              </div>
              <div className="w-100">
                <label className="">y2</label>
                <InputText
                  className="input-container"
                  onChange={(e) => onDetectionRangeChange(e, "y2")}
                  placeholder=""
                />
              </div>
            </div>
          </Card>
          <Card
            className="config-card-container"
            title="Recognition"
            footer={reco_footer}
          >
            <div>
              <label>Debug</label>
              <SelectButton
                className="select-button"
                value={set_debug_state ? set_debug_state : 0}
                options={debug_state}
                optionValue="code"
                optionLabel="name"
                onChange={(e) => onDebugStateChange(e)}
              />
            </div>
            <div className="d-flex d-flex-row gap-2">
              <div className="w-100">
                <label className="">Dlib Model</label>
                <InputText className="input-container" placeholder="" />
              </div>
            </div>
            <div className="d-flex d-flex-row gap-2">
              <div className="w-100">
                <label className="">Reco Model</label>
                <InputText className="input-container" placeholder="" />
              </div>
            </div>
            <div className="d-flex d-flex-row gap-2">
              <div className="w-100">
                <label className="">Minimum bounding box height</label>
                <InputText className="input-container" placeholder="" />
              </div>
              <div className="w-100">
                <label className="">Minimum face detection score</label>
                <InputText className="input-container" placeholder="" />
              </div>
            </div>
            <div className="d-flex d-flex-row gap-2">
              <div className="w-100">
                <label className="">Eyes detection value (Brighter)</label>
                <InputText className="input-container" placeholder="" />
              </div>
              <div className="w-100">
                <label className="">Eyes detection value (Darker)</label>
                <InputText className="input-container" placeholder="" />
              </div>
            </div>
            <div className="d-flex d-flex-row gap-2">
              <div className="w-100">
                <label className="">Consecutive prediction intervals</label>
                <InputText className="input-container" placeholder="" />
              </div>
              <div className="w-100">
                <label className="">Sensitivity</label>
                <InputText className="input-container" placeholder="" />
              </div>
            </div>
          </Card>
        </div>
        <div className="col-7 col-lg-7">
          <div className="config-live-image-container">
            <ImageROI image={set_image} detectionRange={detection_range} />
          </div>
          <div className="d-flex">
            <div className="config-roi-image-container">
              <img src="/image/roi_not_found.jpg" alt="video_stream" />
            </div>
            <div className="config-roi-image-container">
              <img src="/image/roi_not_found.jpg" alt="video_stream" />
            </div>
            <div className="d-flex  justify-content-end align-items-end w-100 gap-2">
              <Button label="Stop" icon="pi pi-times" className="cancel-btn" />
              <Button label="Start" icon="pi pi-check" className="func-btn" />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default FaceRecognitionConfig
