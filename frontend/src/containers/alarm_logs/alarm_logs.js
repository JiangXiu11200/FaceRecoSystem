import { TabPanel, TabView } from "primereact/tabview"
import React from "react"

import AlarmLogsPage from "../../components/alarm_logs/alarm_logs"

import "./alarm_logs.css"

function AlarmLogs() {
    return (
        <div className="container-fluid ms-0 pt-3 tabview-layout">
            <TabView>
                <TabPanel header="Alarm Logs" leftIcon="pi pi-calendar">
                    <AlarmLogsPage />
                </TabPanel>
            </TabView>
        </div>
    )
}

export default AlarmLogs
