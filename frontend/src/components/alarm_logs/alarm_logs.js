import cloneDeep from "lodash/cloneDeep"
import { Button } from "primereact/button"
import { Calendar } from "primereact/calendar"
import { Dialog } from "primereact/dialog"
import { InputText } from "primereact/inputtext"
import { MultiSelect } from "primereact/multiselect"
import { Toast } from "primereact/toast"
import { Toolbar } from "primereact/toolbar"

import React, { useEffect, useRef, useState } from "react"

import { Table } from "../data_table/data_table"

import "./alarm_logs.css"

function AlarmLogs() {
  const toast = useRef(null)
  const [table_data, setTableData] = useState([])
  const [set_action_event, setActionEvent] = useState({})
  const empty_search_content = {
    alarm_category: null,
    start_date: null,
    end_date: null,
    confirm: false,
  }
  const [search_content, setSearchContent] = useState(
    cloneDeep(empty_search_content)
  )
  const [set_confirm_alarm_details, setConfirmAlarmDetails] = useState(false)

  const columns = [
    {
      header: "No",
      field: "number",
    },
    {
      header: "Log Time",
      field: "log_time",
    },
    {
      header: "Message",
      field: "message",
    },
    {
      header: "Confirm",
      field: "confirm",
      type: "boolean",
    },
  ]

  const _mock_data = Array.from({ length: 20 }, (_, i) => ({
    number: i + 1,
    log_time: `2023-10-01 12:00:00`,
    message: `Alarm message ${i + 1}`,
    confirm: i % 2 === 0,
  }))

  useEffect(() => {
    setTableData(_mock_data)
  }, [])

  useEffect(() => {
    switch (set_action_event.action) {
      case "image":
        setConfirmAlarmDetails(true)
        break
      default:
        break
    }
  }, [set_action_event])

  const onSearchContentChange = (e, name) => {
    const val = (e.target && e.target.value) || ""
    let _search_content = { ...search_content }
    _search_content[name] = val
    setSearchContent(_search_content)
  }

  const doConfirm = () => {
    toast.current.show({
      severity: "success",
      summary: "Success",
      detail: "Alarm confirmed successfully",
      life: 3000,
    })
    setConfirmAlarmDetails(false)
  }

  const hideConfirmAlarmDialog = () => {
    setConfirmAlarmDetails(false)
  }

  const leftContents = (
    <React.Fragment>
      <div className="row g-2">
        <div className="col-4">
          <label>Alarm Category</label>
          <div className="field-group">
            <MultiSelect
              className="w-100"
              placeholder="Alarm Category"
              options={[]}
              onChange={() => {}}
              optionLabel="name"
            />
          </div>
        </div>
        <div className="col-4">
          <label>Start Date</label>
          <Calendar
            id="start_date"
            className="w-100"
            value={search_content.start_date}
            maxDate={search_content.end_date ? search_content.end_date : null}
            onChange={(e) => onSearchContentChange(e, "start_date")}
            showTime
            showSeconds
            hourFormat="24"
            dateFormat="yy-mm-dd"
            placeholder="Start Date"
          />
        </div>
        <div className="col-4">
          <label>End Date</label>
          <Calendar
            id="end_date"
            className="w-100"
            value={search_content.end_date}
            minDate={
              search_content.start_date ? search_content.start_date : null
            }
            onChange={(e) => onSearchContentChange(e, "end_date")}
            showTime
            showSeconds
            hourFormat="24"
            dateFormat="yy-mm-dd"
            placeholder="End Date"
          />
        </div>
      </div>
    </React.Fragment>
  )

  const confirmAlarmDialogFooter = (
    <React.Fragment>
      <div className="d-flex justify-content-end">
        <div className="d-flex">
          <div className="me-2">
            <Button
              label="Confirm"
              icon="pi pi-check"
              className="p-button-text func-btn"
              onClick={doConfirm}
            />
          </div>
          <div>
            <Button
              label="Cancel"
              icon="pi pi-times"
              className="p-button-text cancel-btn"
              onClick={hideConfirmAlarmDialog}
            />
          </div>
        </div>
      </div>
    </React.Fragment>
  )

  return (
    <div className="d-flex flex-column">
      <Toast ref={toast} />
      <Toolbar className="toolbar-layout" left={leftContents} />
      <Table
        data={table_data}
        columns={columns}
        actnioEvent={setActionEvent}
        imageFlag={true}
      />
      <Dialog
        visible={set_confirm_alarm_details}
        className=""
        header="Alarm Details"
        footer={confirmAlarmDialogFooter}
        onHide={hideConfirmAlarmDialog}
      >
        <div className="edit-user-dialog">
          <div className="right-content">
            <div className="">
              <label>Log Time</label>
              <InputText
                className="p-inputtext"
                placeholder=""
                disabled={true}
              />
            </div>
            <div className="">
              <label>Message</label>
              <InputText
                className="p-inputtext"
                placeholder=""
                disabled={true}
              />
            </div>
          </div>
          <div className="left-content">
            <img src="./image/roi_not_found.jpg" alt="" />
          </div>
        </div>
      </Dialog>
    </div>
  )
}

export default AlarmLogs
