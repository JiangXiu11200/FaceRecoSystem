import { TabPanel, TabView } from "primereact/tabview"
import React from "react"

import AlarmLogsPage from "../../containers/alarm_logs/alarm_logs"
import SystemActivityLogsPage from "../../containers/system_activity_logs/system_activity_logs"

import "./alarm_logs.css"

function AlarmLogs() {
  return (
    <div className="tabview-layout">
      <TabView>
        <TabPanel header="Alarm Logs" leftIcon="pi pi-calendar">
          <AlarmLogsPage />
        </TabPanel>
        <TabPanel header="System Activity" leftIcon="pi pi-calendar">
          <SystemActivityLogsPage />
        </TabPanel>
      </TabView>
    </div>
  )
}

export default AlarmLogs
