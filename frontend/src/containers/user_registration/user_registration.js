import React from "react"
import { TabView, TabPanel } from "primereact/tabview"

import Register from "../../components/register/register"

import "./user_registration.css"

function UserRegistration() {
    return (
        <div className="container-fluid ms-0 pt-3 tabview-layout">
            <TabView>
                <TabPanel header="Register" leftIcon="pi pi-camera">
                    <Register />
                </TabPanel>
                <TabPanel header="Group" leftIcon="pi pi-users"></TabPanel>
                <TabPanel header="User" leftIcon="pi pi-user-plus"></TabPanel>
            </TabView>
        </div>
    )
}

export default UserRegistration
