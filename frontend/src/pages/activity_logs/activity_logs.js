import React from "react"

import { TabPanel, TabView } from "primereact/tabview"

import FacialRecognition from "../../containers/facial_reco_logs/facial_reco_logs"
import SystemActivityLogs from "../../containers/system_activity_logs/system_activity_logs"

import "./activity_logs.css"

function ActivityLogs() {
  return (
    <div className="container-layout tabview-layout">
      <TabView>
        <TabPanel header="Facial Recognition" leftIcon="pi pi-calendar">
          <FacialRecognition />
        </TabPanel>
        <TabPanel header="System Activity" leftIcon="pi pi-calendar">
          <SystemActivityLogs />
        </TabPanel>
      </TabView>
    </div>
  )
}

export default ActivityLogs
