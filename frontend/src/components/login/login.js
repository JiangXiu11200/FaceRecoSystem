import React, { useState, useRef } from "react"
import { Button } from "primereact/button"
import { Toast } from "primereact/toast"
import { InputText } from "primereact/inputtext"
import { Password } from "primereact/password"

import "./login.css"

function Login() {
    const toast = useRef(null)
    const [select_mode, setSelectedMode] = useState("")
    const [input_error, setInputError] = useState(false)
    const [password_error, setPasswordError] = useState(false)
    const [login_error, setLoginError] = useState("")
    const [userName, setUserName] = useState(null)
    const [password, setPassword] = useState(null)

    const handleSelectMode = (mode) => {
        setSelectedMode(mode)
    }

    const onInputChange = (e, name) => {
        const value = (e.target && e.target.value) || ""
        if (name == "user_name") {
            setUserName(value)
        }
        if (name == "password") {
            setPassword(value)
        }
        clearError()
    }

    const handleLogin = () => {
        if (select_mode === "") {
            toast.current.show({ severity: "error", summary: "Error", detail: "Please select mode." })
            return
        }
        if (!userName) {
            setInputError(true)
            setLoginError("Please enter your username.")
            return
        }
        if (!password) {
            setPasswordError(true)
            setLoginError("Please enter your password.")
            return
        }

        if (password !== "123123") {
            // for testing
            setLoginError("Incorrect username or password.")
            return
        }

        clearError()
    }

    const clearError = () => {
        setLoginError("")
        setInputError(false)
        setPasswordError(false)
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
                                    className="p-button-info select-mode-btn"
                                    onClick={() => handleSelectMode("Standard")}
                                    disabled={select_mode == "Standard"}
                                />
                            </div>
                            <div className="button-wrapper">
                                <Button
                                    label="Advanced"
                                    className="p-button-info select-mode-btn"
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
                            <InputText
                                id="user_name"
                                name="user_name"
                                className={`input-field ${input_error ? "username-error" : ""}`}
                                value={userName}
                                keyfilter={/[^\s]/}
                                placeholder="User Name"
                                onChange={(e) => onInputChange(e, "user_name")}
                            />
                        </div>
                        <div className="mb-2">
                            <Password
                                id="password"
                                name="password"
                                inputClassName={password_error ? "password-error" : ""}
                                value={password}
                                feedback={false}
                                placeholder="Password"
                                onChange={(e) => onInputChange(e, "password")}
                            />
                        </div>
                        <div>
                            {login_error && (
                                <div>
                                    <label className="error-message">{login_error}</label>
                                </div>
                            )}
                        </div>
                    </div>
                    <div className="button-layout">
                        <div className="col-8"></div>
                        <div className="col-4">
                            <Button label="Login" className="select-mode-btn" onClick={handleLogin} />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Login
