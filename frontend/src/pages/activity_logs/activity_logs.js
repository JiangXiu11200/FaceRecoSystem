import { TabPanel, TabView } from "primereact/tabview"
import React from "react"

import FacialRecognition from "../../containers/facial_reco_logs/facial_reco_logs"
import SystemActivityLogs from "../../containers/system_activity_logs/system_activity_logs"

import "./activity_logs.css"

function ActivityLogs() {
  return (
    <div className="container-fluid ms-0 pt-3 tabview-layout">
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
