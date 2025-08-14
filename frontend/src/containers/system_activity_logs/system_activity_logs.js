import React, { useEffect, useMemo, useRef, useState } from "react"

import { Button } from "primereact/button"
import { Dialog } from "primereact/dialog"
import { Dropdown } from "primereact/dropdown"
import { InputText } from "primereact/inputtext"
import { MultiSelect } from "primereact/multiselect"
import { SelectButton } from "primereact/selectbutton"
import { Toast } from "primereact/toast"
import { Toolbar } from "primereact/toolbar"

import { activityLogsApi } from "../../api/activity_logs"
import { Table } from "../../components/data_table/data_table"

import "./system_activity_logs.css"

function SystemActivityLogs() {
  const toast = useRef(null)
  const [logRetention, setLogRetention] = useState(0)
  const [table_data, setTableData] = useState([])
  const [serachUsers, setSearchUsers] = useState("")
  const [set_action_event, setActionEvent] = useState({})
  const [tablePage, setTablePage] = useState({
    page: 1,
    offset: 0,
    limit: 10,
  })

  const columns = [
    { header: "Accounts", field: "account" },
    { header: "Activity", field: "activity" },
    { header: "Message", field: "message" },
    { header: "Status", field: "status", type: "boolean" },
    { header: "Status Code", field: "status_code" },
    { header: "Log Time", field: "timestamp", type: "date" },
  ]

  const showToast = (severity, summary, detail, life = 3000) => {
    toast.current.show({ severity, summary, detail, life })
  }

  const getSystemActivityLogs = () => {
    activityLogsApi("get", `/system/?account=${serachUsers}`, tablePage)
      .then((response) => {
        setTableData(response.data.results)
        if (serachUsers !== "") {
          showToast(
            "success",
            "Search Results",
            `Found ${response.data.count} logs for user: ${serachUsers}`
          )
        }
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  const getRetention = () => {
    activityLogsApi("get", "/system/retention/")
      .then((response) => {
        setLogRetention(response.data.results[0].retention_days)
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  const changeRetentionDays = () => {
    activityLogsApi("put", "/system/retention/1/", {
      retention_days: logRetention,
    })
      .then(() => {
        showToast(
          "success",
          "Success",
          "Log retention days updated successfully"
        )
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  useEffect(() => {
    getSystemActivityLogs()
    getRetention()
  }, [])

  const leftContents = (
    <React.Fragment>
      <div className="row g-2">
        <div className="col-8">
          <label>User Account</label>
          <InputText
            className="p-inputtext"
            placeholder="User Account"
            onChange={(e) => setSearchUsers(e.target.value)}
          />
        </div>
        <div className="col-4 align-self-end">
          <Button
            icon="pi pi-search"
            className="func-btn"
            label="Search"
            onClick={getSystemActivityLogs}
          />
        </div>
      </div>
    </React.Fragment>
  )

  const rightContents = (
    <React.Fragment>
      <div className="row g-2 justify-content-end">
        <div className="col-4">
          <label>Log Retention</label>
          <InputText
            className="p-inputtext"
            placeholder="Log Retention"
            value={logRetention}
            onChange={(e) => setLogRetention(e.target.value)}
          />
        </div>
        <div className="col-3 align-self-end">
          <Button
            icon="pi pi-check"
            className="func-btn"
            label="Save"
            onClick={changeRetentionDays}
          />
        </div>
      </div>
    </React.Fragment>
  )

  return (
    <div className="d-flex flex-column">
      <Toast ref={toast} />
      <Toolbar
        className="toolbar-layout activity-logs-toolbar justify-content-between"
        left={leftContents}
        right={rightContents}
      />
      <Table
        data={table_data}
        columns={columns}
        actnioEvent={setActionEvent}
        tableParams={setTablePage}
      />
    </div>
  )
}

export default SystemActivityLogs
