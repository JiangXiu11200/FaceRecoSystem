import { TabPanel, TabView } from "primereact/tabview"
import React from "react"

import Group from "../../components/group/group"
import Register from "../../components/register/register"
import Users from "../../components/users/users"

import "./user_registration.css"

function UserRegistration() {
  return (
    <div className="container-fluid ms-0 pt-3 tabview-layout">
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
