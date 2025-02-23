import React from "react"
import { BreadCrumb } from "primereact/breadcrumb"
import { LiaUserCircle } from "react-icons/lia"
import { Menu } from "primereact/menu"
import { useState, useRef } from "react"
import "./header.css"
import { Button } from "primereact/button"

function Header() {
    const home = { icon: "pi pi-home", url: "/" }
    const items = [{ label: "FaceRecognition" }]
    const menuRight = useRef(null)
    const menu_item = [
        { label: "New", icon: "pi pi-fw pi-plus" },
        { label: "Delete", icon: "pi pi-fw pi-trash" },
    ]
    return (
        <div className="row header-container">
            <div className="col left-layout">
                <BreadCrumb className="custom-breadcrumb" model={items} home={home} />
            </div>
            <div className="col right-layout">
                <div>
                    <Menu id="user_menu" model={menu_item} popup ref={menuRight} popupAlignment="right" />
                    <Button
                        id="user_menu"
                        className="header-button p-button-rounded p-button-text p-button-icon-only p-0"
                        icon={<LiaUserCircle className="user-icon" />}
                        onClick={(event) => menuRight.current.toggle(event)}
                        aria-controls="user_menu"
                    />
                </div>
            </div>
        </div>
    )
}

export default Header
