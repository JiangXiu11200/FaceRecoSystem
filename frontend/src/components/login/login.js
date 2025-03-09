import React from "react"
import { Button } from "primereact/button"
import { InputText } from "primereact/inputtext"
import { Password } from "primereact/password"

import "./login.css"

function Login() {
    return (
        <div className="container">
            <div className="select-container">
                <div className="select-layout">
                    <div className="row">
                        <label className="select-label">Select Mode</label>
                        <div>
                            <div className="button-wrapper">
                                <Button label="Standard" className="select-btn" onClick={""} />
                            </div>
                            <div className="button-wrapper">
                                <Button label="Advanced" className="select-btn" onClick={""} />
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
                            <Button label="Login" className="select-btn" onClick={""} />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Login
