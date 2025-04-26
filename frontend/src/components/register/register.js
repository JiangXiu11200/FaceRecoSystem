import cloneDeep from "lodash/cloneDeep"
import { Button } from "primereact/button"
import { Dropdown } from "primereact/dropdown"
import { InputText } from "primereact/inputtext"
import { Toast } from "primereact/toast"
import React, { useRef, useState } from "react"

import "./register.css"

function register() {
  const toast = useRef(null)
  const empty_user_details = {
    user_name: "",
    group: "",
  }
  const [new_user_details, setNewUserDetails] = useState(
    cloneDeep(empty_user_details)
  )
  const [user_groups, setUserGroups] = useState([])

  const onInputChange = (e, name) => {
    const value = (e.target && e.target.value) || ""
    let _new_user_details = { ...new_user_details }
    _new_user_details[name] = value
    setNewUserDetails(_new_user_details)
  }

  const onClear = () => {
    setNewUserDetails(cloneDeep(empty_user_details))
    toast.current.show({
      severity: "info",
      summary: "Cleared",
      detail: "Cleared all fields.",
    })
  }

  return (
    <div className="content-layout">
      <Toast ref={toast} />
      <div className="image-layout">
        <img src="./image/not_found.jpg" alt="video_stream" />
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
            />
          </div>
        </div>
        <div>
          <div className="form-group">
            <Button
              label="Register"
              icon="pi pi-check"
              className="p-button-success func-btn"
              onClick={() => handleRegister()}
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
            />
          </div>
        </div>
      </div>
    </div>
  )
}

export default register
