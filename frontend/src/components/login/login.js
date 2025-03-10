import React, { useState, useRef } from "react"
import { Button } from "primereact/button"
import { Toast } from "primereact/toast"
import { InputText } from "primereact/inputtext"
import { Password } from "primereact/password"

import "./login.css"

function Login() {
    const toast = useRef(null)
    const [select_mode, setSelectedMode] = useState("")

    const handleSelectMode = (mode) => {
        setSelectedMode(mode)
    }

    const handleLogin = () => {
        if (select_mode === "") {
            toast.current.show({ severity: "error", summary: "Error", detail: "Please select mode." })
            return
        }
    }

    return (
        <div className="container">
            <Toast ref={toast} />
            <div className="select-container">
                <div className="select-layout">
                    <div className="row">
                        <label className="select-label">Select Mode</label>
                        <div>
                            <div className="button-wrapper">
                                <Button
                                    label="Standard"
                                    className="p-button-info select-btn"
                                    onClick={() => handleSelectMode("Standard")}
                                    disabled={select_mode == "Standard"}
                                />
                            </div>
                            <div className="button-wrapper">
                                <Button
                                    label="Advanced"
                                    className="p-button-info select-btn"
                                    onClick={() => handleSelectMode("Advanced")}
                                    disabled={select_mode == "Advanced"}
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div className="login-container">
                <div className="login-layout">
                    <div className="label-layout">
                        <label className="login-label">Welcome</label>
                    </div>
                    <div className="form-layout">
                        <div className="mb-2">
                            <InputText id="user_name" name="user_name" keyfilter={/[^\s]/} placeholder="User Name" />
                        </div>
                        <div className="mb-2">
                            <Password id="password" name="password" feedback={false} placeholder="Password" />
                        </div>
                    </div>
                    <div className="button-layout">
                        <div className="col-8"></div>
                        <div className="col-4">
                            <Button label="Login" className="select-btn" onClick={handleLogin} />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Login
