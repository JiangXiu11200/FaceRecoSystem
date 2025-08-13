import React, { useEffect, useRef, useState } from "react"
import cloneDeep from "lodash/cloneDeep"
import { Button } from "primereact/button"
import { Calendar } from "primereact/calendar"
import { Dialog } from "primereact/dialog"
import { InputText } from "primereact/inputtext"
import { MultiSelect } from "primereact/multiselect"
import { Toast } from "primereact/toast"
import { Toolbar } from "primereact/toolbar"
import { alarmLogsApi } from "../../api/alarm_logs"

import { Table } from "../../components/data_table/data_table"
import "./alarm_logs.css"

const LEVEL_CHOICES = [
  { code: 1, name: "Info" },
  { code: 2, name: "Warning" },
  { code: 3, name: "Critical" },
  { code: 4, name: "Error" },
  { code: 5, name: "Fatal" },
]

const INITIAL_SEARCH = {
  alarm_category: null,
  start_date: null,
  end_date: null,
}

const AlarmLogs = () => {
  const toast = useRef(null)

  const [tableData, setTableData] = useState([])
  const [alarmDetails, setAlarmDetails] = useState({})
  const [searchContent, setSearchContent] = useState(cloneDeep(INITIAL_SEARCH))
  const [showAlarmDetailsDialog, setShowAlarmDetailsDialog] = useState(false)
  const [tablePage, setTablePage] = useState({
    page: 1,
    offset: 0,
    limit: 10,
  })

  const columns = [
    { header: "No", field: "id" },
    { header: "Alarm Type", field: "alarm_type_name" },
    { header: "Alarm Message", field: "alarm_message" },
    { header: "Confirm", field: "confirm", type: "boolean" },
    { header: "Trigger Time", field: "create_time", type: "date" },
  ]

  const showToast = (severity, summary, detail, life = 3000) => {
    toast.current.show({ severity, summary, detail, life })
  }

  const getAlarmLogs = () => {
    alarmLogsApi("get", "/", tablePage)
      .then((response) => {
        const results = response.data.results.map((item) => ({
          ...item,
          alarm_type_name:
            LEVEL_CHOICES.find((level) => level.code === item.alarm_type)
              ?.name || "Unknown",
        }))
        setTableData(results)
      })
      .catch((error) => {
        showToast("error", "Error", err.response.data)
      })
  }

  const handleSearch = () => {
    let url = `/?alarm_category=${searchContent.alarm_category || ""}&start_date=${searchContent.start_date ? searchContent.start_date.toISOString() : ""}&end_date=${searchContent.end_date ? searchContent.end_date.toISOString() : ""}`

    alarmLogsApi("get", url, tablePage)
      .then((response) => {
        const results = response.data.results.map((item) => ({
          ...item,
          alarm_type_name:
            LEVEL_CHOICES.find((level) => level.code === item.alarm_type)
              ?.name || "Unknown",
        }))
        setTableData(results)
      })
      .catch((error) => {
        showToast("error", "Error", error.response.data)
      })
    setAlarmDetails({})
  }

  const handleConfirmAlarm = () => {
    const updatedAlarm = cloneDeep(alarmDetails)
    updatedAlarm.acknowledged = true
    alarmLogsApi("put", `/acknowledge/${alarmDetails.id}/`, updatedAlarm)
      .then(() => {
        showToast("success", "Success", "Alarm confirmed successfully.")
        setShowAlarmDetailsDialog(false)
        getAlarmLogs()
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  const handleAction = ({ action, data }) => {
    setAlarmDetails(data)
    if (action === "image") {
      setShowAlarmDetailsDialog(true)
    }
  }

  useEffect(() => {
    getAlarmLogs()
  }, [])

  const leftContents = (
    <React.Fragment>
      <div className="alarmlogs-toolbar">
        <div className="alarmlogs-form-field">
          <label>Alarm Type</label>
          <MultiSelect
            className="w-100"
            placeholder="Select Alarm Type"
            options={LEVEL_CHOICES}
            optionValue="code"
            optionLabel="name"
            value={searchContent.alarm_category}
            onChange={(e) =>
              setSearchContent((prev) => ({ ...prev, alarm_category: e.value }))
            }
            maxSelectedLabels={0}
          />
        </div>
        <div className="alarmlogs-form-field">
          <label>Start Date</label>
          <Calendar
            className="w-100"
            value={searchContent.start_date}
            maxDate={searchContent.end_date || null}
            onChange={(e) =>
              setSearchContent((prev) => ({ ...prev, start_date: e.value }))
            }
            showTime
            showSeconds
            hourFormat="24"
            dateFormat="yy-mm-dd"
            placeholder="Start Date"
          />
        </div>
        <div className="alarmlogs-form-field">
          <label>End Date</label>
          <Calendar
            className="w-100"
            value={searchContent.end_date}
            minDate={searchContent.start_date || null}
            onChange={(e) =>
              setSearchContent((prev) => ({ ...prev, end_date: e.value }))
            }
            showTime
            showSeconds
            hourFormat="24"
            dateFormat="yy-mm-dd"
            placeholder="End Date"
          />
        </div>
        <div className="d-flex align-items-end">
          <Button
            icon="pi pi-search"
            className="func-btn"
            label="Search"
            onClick={handleSearch}
          />
        </div>
      </div>
    </React.Fragment>
  )

  const alarmDialogFooter = (
    <div className="d-flex justify-content-end">
      <Button
        label="Confirm"
        icon="pi pi-check"
        className="p-button-text func-btn me-2"
        onClick={handleConfirmAlarm}
      />
      <Button
        label="Cancel"
        icon="pi pi-times"
        className="p-button-text cancel-btn"
        onClick={() => setShowAlarmDetailsDialog(false)}
      />
    </div>
  )

  return (
    <div className="d-flex flex-column">
      <Toast ref={toast} />
      <Toolbar className="toolbar-layout" left={leftContents} />
      <Table
        data={tableData}
        columns={columns}
        tableParams={setTablePage}
        actnioEvent={handleAction}
        imageFlag
      />
      <Dialog
        visible={showAlarmDetailsDialog}
        header="Alarm Details"
        footer={alarmDialogFooter}
        onHide={() => setShowAlarmDetailsDialog(false)}
      >
        <div className="alarm-details-dialog">
          <div className="alarm-details-right-content">
            <div>
              <label>Log Time</label>
              <InputText
                className="p-inputtext"
                value={
                  alarmDetails
                    ? new Date(alarmDetails.create_time).toLocaleString()
                    : ""
                }
                disabled
              />
            </div>
            <div>
              <label>Message</label>
              <InputText
                className="p-inputtext"
                value={alarmDetails ? alarmDetails.message : ""}
                disabled
              />
            </div>
          </div>
          <div className="alarm-details-left-content">
            <img src="/image/roi_not_found.jpg" alt="Alarm" />
          </div>
        </div>
      </Dialog>
    </div>
  )
}

export default AlarmLogs
