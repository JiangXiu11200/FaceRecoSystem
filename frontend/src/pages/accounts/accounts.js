import React from "react"

import { TabPanel, TabView } from "primereact/tabview"

import AccountGroups from "../../containers/account_groups/account_groups"
import Account from "../../containers/accounts/accounts"

import "./accounts.css"

function Accounts() {
  return (
    <div className="container-layout tabview-layout">
      <TabView>
        <TabPanel header="Accounts" leftIcon="pi pi-calendar">
          <Account />
        </TabPanel>
        <TabPanel header="Account Groups" leftIcon="pi pi-calendar">
          <AccountGroups />
        </TabPanel>
      </TabView>
    </div>
  )
}

export default Accounts
