import React from "react"

import { TabPanel, TabView } from "primereact/tabview"

import Group from "../../containers/group/group"
import Register from "../../containers/user_register/user_register"
import Users from "../../containers/users/users"

import "./user_registration.css"

function UserRegistration() {
  return (
    <div className="tabview-layout">
      <TabView>
        <TabPanel header="Register" leftIcon="pi pi-camera">
          <Register />
        </TabPanel>
        <TabPanel header="Group" leftIcon="pi pi-users">
          <Group />
        </TabPanel>
        <TabPanel header="User" leftIcon="pi pi-user-plus">
          <Users />
        </TabPanel>
      </TabView>
    </div>
  )
}

export default UserRegistration
