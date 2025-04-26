import { TabPanel, TabView } from "primereact/tabview"
import React from "react"

import FacialRecognition from "../../components/facial_reco_logs/facial_reco_logs"

import "./activity_logs.css"

function ActivityLogs() {
    return (
        <div className="container-fluid ms-0 pt-3 tabview-layout">
            <TabView>
                <TabPanel header="Facial Recognition" leftIcon="pi pi-calendar">
                    <FacialRecognition />
                </TabPanel>
            </TabView>
        </div>
    )
}

export default ActivityLogs
