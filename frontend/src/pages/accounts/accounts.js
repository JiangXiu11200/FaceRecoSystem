import React from "react"

import { TabPanel, TabView } from "primereact/tabview"

import Account from "../../containers/accounts/accounts"

import "./accounts.css"

function Accounts() {
  return (
    <div className="container-layout tabview-layout">
      <TabView>
        <TabPanel header="Accounts" leftIcon="pi pi-calendar">
          <Account />
        </TabPanel>
      </TabView>
    </div>
  )
}

export default Accounts
