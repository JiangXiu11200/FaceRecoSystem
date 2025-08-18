import React, { useEffect, useRef, useState } from "react"

import { cloneDeep } from "lodash"
import { Button } from "primereact/button"
import { Card } from "primereact/card"
import { InputText } from "primereact/inputtext"
import { SelectButton } from "primereact/selectbutton"
import { Toast } from "primereact/toast"

import ImageROI from "../../components/image_roi_canvas/image_roi"

import "./face_recognition_config.css"

const ENABLE_STATE = [
  { code: 0, name: "OFF" },
  { code: 1, name: "ON" },
]

const EMPTY_DETECTION_CONFIG = {
  debug: 0,
  rtsp: "",
  image_width: 0,
  image_height: 0,
  dlib_predictor_path: "",
  dlib_recognition_model_path: "",
  detection_range_start_point_x: 0,
  detection_range_start_point_y: 0,
  detection_range_end_point_x: 0,
  detection_range_end_point_y: 0,
  minimum_bounding_box_height: 0,
  minimum_face_detection_score: 0,
  eyes_detection_brightness_threshold: 0,
  eyes_detection_brightness_value_min: 0,
  eyes_detection_brightness_value_max: 0,
  sensitivity: 0,
  consecutive_prediction_intervals_frame: 90,
}

const EMPTY_DETECTION_RANGE = {
  x1: 0,
  y1: 0,
  x2: 0,
  y2: 0,
}

function FaceRecognitionConfig() {
  const toast = useRef(null)
  const [cameraImage, setCameraImage] = useState(null)
  const [detectionConfig, setDetectionConfig] = useState(
    cloneDeep(EMPTY_DETECTION_CONFIG)
  )
  const [detection_range, setDetectionRange] = useState(
    cloneDeep(EMPTY_DETECTION_RANGE)
  )

  const showToast = (severity, summary, detail, life = 3000) => {
    toast.current.show({ severity, summary, detail, life })
  }

  useEffect(() => {
    console.log(detection_range)
  }, [detection_range])

  const video_footer = (
    <div className="d-flex d-flex-row justify-content-end">
      <Button
        icon="pi pi-eye"
        className="func-btn"
        label="Preview"
        onClick={() => {}}
      />
    </div>
  )

  const reco_footer = (
    <div className="d-flex d-flex-row justify-content-end">
      <Button
        icon="pi pi-check"
        className="func-btn"
        label="Apply"
        onClick={() => {}}
      />
    </div>
  )

  return (
    <div className="general-page-layout">
      <Toast ref={toast} />
      <div className="facereco-content">
        <div className="col-5 col-lg-5">
          <Card
            className="config-card-container"
            title="Video"
            footer={video_footer}
          >
            <div>
              <label className="">RTSP / Web cam path / ...</label>
              <InputText
                className="input-container"
                value={detectionConfig ? detectionConfig.rtsp : ""}
                onChange={(e) => {
                  setDetectionConfig({
                    ...detectionConfig,
                    rtsp: e.target.value,
                  })
                }}
              />
            </div>
            <div className="d-flex d-flex-row gap-2">
              <div className="w-100">
                <label className="">Image Width</label>
                <InputText
                  className="input-container"
                  value={detectionConfig ? detectionConfig.image_width : 0}
                  onChange={(e) => {
                    setDetectionConfig({
                      ...detectionConfig,
                      image_width: e.target.value,
                    })
                  }}
                />
              </div>
              <div className="w-100">
                <label className="">Image Height</label>
                <InputText
                  className="input-container"
                  value={detectionConfig ? detectionConfig.image_height : 0}
                  onChange={(e) => {
                    setDetectionConfig({
                      ...detectionConfig,
                      image_height: e.target.value,
                    })
                  }}
                />
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
                  value={
                    detectionConfig
                      ? detectionConfig.detection_range_start_point_x
                      : 0
                  }
                  onChange={(e) =>
                    setDetectionConfig(
                      {
                        ...detection_range,
                        detection_range_start_point_x: e.target.value,
                      },
                      setDetectionRange({
                        ...detection_range,
                        x1: e.target.value,
                      })
                    )
                  }
                />
              </div>
              <div className="w-100">
                <label className="">y1</label>
                <InputText
                  className="input-container"
                  value={
                    detectionConfig
                      ? detectionConfig.detection_range_start_point_y
                      : 0
                  }
                  onChange={(e) => {
                    setDetectionConfig(
                      {
                        ...detection_range,
                        detection_range_start_point_y: e.target.value,
                      },
                      setDetectionRange({
                        ...detection_range,
                        y1: e.target.value,
                      })
                    )
                  }}
                />
              </div>
              <div className="w-100">
                <label className="">x2</label>
                <InputText
                  className="input-container"
                  value={
                    detectionConfig
                      ? detectionConfig.detection_range_end_point_x
                      : 0
                  }
                  onChange={(e) => {
                    setDetectionConfig(
                      {
                        ...detection_range,
                        detection_range_end_point_x: e.target.value,
                      },
                      setDetectionRange({
                        ...detection_range,
                        x2: e.target.value,
                      })
                    )
                  }}
                />
              </div>
              <div className="w-100">
                <label className="">y2</label>
                <InputText
                  className="input-container"
                  value={
                    detectionConfig
                      ? detectionConfig.detection_range_end_point_y
                      : 0
                  }
                  onChange={(e) => {
                    setDetectionConfig(
                      {
                        ...detection_range,
                        detection_range_end_point_y: e.target.value,
                      },
                      setDetectionRange({
                        ...detection_range,
                        y2: e.target.value,
                      })
                    )
                  }}
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
                value={detectionConfig ? detectionConfig.debug : 0}
                options={ENABLE_STATE}
                optionValue="code"
                optionLabel="name"
                onChange={(e) =>
                  setDetectionConfig({
                    ...detectionConfig,
                    debug: e.value,
                  })
                }
              />
            </div>
            <div className="d-flex d-flex-row gap-2">
              <div className="w-100">
                <label className="">Predictor Model</label>
                <InputText
                  className="input-container"
                  value={
                    detectionConfig ? detectionConfig.dlib_predictor_path : ""
                  }
                  onChange={(e) => {
                    setDetectionConfig({
                      ...detectionConfig,
                      dlib_predictor_path: e.target.value,
                    })
                  }}
                />
              </div>
            </div>
            <div className="d-flex d-flex-row gap-2">
              <div className="w-100">
                <label className="">Recognition Model</label>
                <InputText
                  className="input-container"
                  value={
                    detectionConfig
                      ? detectionConfig.dlib_recognition_model_path
                      : ""
                  }
                  onChange={(e) => {
                    setDetectionConfig({
                      ...detectionConfig,
                      dlib_recognition_model_path: e.target.value,
                    })
                  }}
                />
              </div>
            </div>
            <div className="d-flex d-flex-row gap-2">
              <div className="w-100">
                <label className="">Minimum bounding box height</label>
                <InputText
                  className="input-container"
                  value={
                    detectionConfig
                      ? detectionConfig.minimum_bounding_box_height
                      : 0
                  }
                  onChange={(e) => {
                    setDetectionConfig({
                      ...detectionConfig,
                      minimum_bounding_box_height: e.target.value,
                    })
                  }}
                />
              </div>
              <div className="w-100">
                <label className="">Minimum face detection score</label>
                <InputText
                  className="input-container"
                  value={
                    detectionConfig
                      ? detectionConfig.minimum_face_detection_score
                      : 0
                  }
                  onChange={(e) => {
                    setDetectionConfig({
                      ...detectionConfig,
                      minimum_face_detection_score: e.target.value,
                    })
                  }}
                />
              </div>
            </div>
            <div className="d-flex d-flex-row gap-2">
              <div className="w-100">
                <label className="">Eyes detection value (Brighter)</label>
                <InputText
                  className="input-container"
                  value={
                    detectionConfig
                      ? detectionConfig.eyes_detection_brightness_value_max
                      : 0
                  }
                  onChange={(e) => {
                    setDetectionConfig({
                      ...detectionConfig,
                      eyes_detection_brightness_threshold: e.target.value,
                    })
                  }}
                />
              </div>
              <div className="w-100">
                <label className="">Eyes detection value (Darker)</label>
                <InputText
                  className="input-container"
                  value={
                    detectionConfig
                      ? detectionConfig.eyes_detection_brightness_value_min
                      : 0
                  }
                  onChange={(e) => {
                    setDetectionConfig({
                      ...detectionConfig,
                      eyes_detection_brightness_value_min: e.target.value,
                    })
                  }}
                />
              </div>
            </div>
            <div className="d-flex d-flex-row gap-2">
              <div className="w-100">
                <label className="">Consecutive prediction intervals</label>
                <InputText
                  className="input-container"
                  value={
                    detectionConfig
                      ? detectionConfig.consecutive_prediction_intervals_frame
                      : 0
                  }
                  onChange={(e) => {
                    setDetectionConfig({
                      ...detectionConfig,
                      consecutive_prediction_intervals_frame: e.target.value,
                    })
                  }}
                />
              </div>
              <div className="w-100">
                <label className="">Sensitivity</label>
                <InputText
                  className="input-container"
                  value={detectionConfig ? detectionConfig.sensitivity : 0}
                  onChange={(e) => {
                    setDetectionConfig({
                      ...detectionConfig,
                      sensitivity: e.target.value,
                    })
                  }}
                />
              </div>
            </div>
          </Card>
        </div>
        <div className="col-7 col-lg-7">
          <div className="config-live-image-container">
            <ImageROI image={cameraImage} detectionRange={detection_range} />
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
