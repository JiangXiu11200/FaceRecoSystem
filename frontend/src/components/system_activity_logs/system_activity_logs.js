import { Button } from "primereact/button"
import { Dialog } from "primereact/dialog"
import { InputText } from "primereact/inputtext"
import { MultiSelect } from "primereact/multiselect"
import { SelectButton } from "primereact/selectbutton"
import { Toast } from "primereact/toast"
import { Toolbar } from "primereact/toolbar"
import React, { useEffect, useMemo, useRef, useState } from "react"

import { Table } from "../data_table/data_table"

import "./system_activity_logs.css"

function SystemActivityLogs() {
  const toast = useRef(null)
  const [table_data, setTableData] = useState([])
  const [set_action_event, setActionEvent] = useState({})

  const columns = [
    {
      header: "User",
      field: "user",
    },
    {
      header: "Activity",
      field: "activity",
    },
    {
      header: "Infomation",
      field: "infomation",
    },
    {
      header: "Status",
      field: "status",
    },
    {
      header: "Log Time",
      field: "log_time",
    },
  ]

  const _mock_data = Array.from({ length: 50 }, (_, i) => ({
    user: `User ${i + 1}`,
    activity: `Activity ${i + 1}`,
    infomation: `Information ${i + 1}`,
    status: i % 2 === 0 ? "Active" : "Inactive",
    log_time: `2023-10-01 12:00:${i < 10 ? `0${i}` : i}`,
  }))

  useEffect(() => {
    setTableData(_mock_data)
  }, [])

  const leftContents = (
    <React.Fragment>
      <div className="activity-logs-toolbar-left">
        <div>
          <label>Log Retention</label>
          <InputText className="p-inputtext" placeholder="Log Retention" />
        </div>
      </div>
    </React.Fragment>
  )

  const rightContents = (
    <React.Fragment>
      <div className="activity-logs-toolbar-right">
        <div>
          <Button icon="pi pi-check" className="func-btn" label="Save" />
        </div>
      </div>
    </React.Fragment>
  )

  return (
    <div className="d-flex flex-column">
      <Toast ref={toast} />
      <Toolbar
        className="activity-logs-toolbar"
        left={leftContents}
        right={rightContents}
      />
      <Table data={table_data} columns={columns} actnioEvent={setActionEvent} />
    </div>
  )
}

export default SystemActivityLogs
