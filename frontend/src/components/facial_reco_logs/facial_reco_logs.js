import { Button } from "primereact/button"
import { InputText } from "primereact/inputtext"
import { MultiSelect } from "primereact/multiselect"
import { Toast } from "primereact/toast"
import { Toolbar } from "primereact/toolbar"
import React, { useEffect, useRef, useState } from "react"

import { Table } from "../data_table/data_table"

import "./facial_reco_logs.css"

function FacialRecoLogs() {
  const toast = useRef(null)
  const [table_data, setTableData] = useState([])
  const [set_action_event, setActionEvent] = useState({})

  const columns = [
    {
      header: "User",
      field: "user",
    },
    {
      header: "Group",
      field: "group",
    },
    {
      header: "Category",
      field: "category",
    },
    {
      header: "Log Time",
      field: "log_time",
    },
    {
      header: "Image",
      field: "image",
      type: "image",
    },
  ]

  const _mock_data = Array.from({ length: 50 }, (_, i) => ({
    user: `User ${i + 1}`,
    group: `Group ${i + 1}`,
    category: `Category ${i + 1}`,
    log_time: `2023-10-01`,
    image: `Image ${i + 1}`,
  }))

  useEffect(() => {
    setTableData(_mock_data)
  }, [])

  const leftContents = (
    <React.Fragment>
      <div className="facial-reco-toolbar-left">
        <div>
          <InputText
            className="p-inputtext"
            placeholder="Search for groups.."
          />
        </div>
        <div>
          <MultiSelect
            className="w-100"
            placeholder="Select Group"
            options={[]}
            onChange={() => {}}
            optionLabel="name"
          />
        </div>
        <div>
          <Button icon="pi pi-search" className="func-btn" label="Search" />
        </div>
      </div>
    </React.Fragment>
  )

  return (
    <div className="d-flex flex-column">
      <Toast ref={toast} />
      <Toolbar className="facial-reco-oolbar-layout" left={leftContents} />
      <Table data={table_data} columns={columns} actnioEvent={setActionEvent} />
    </div>
  )
}

export default FacialRecoLogs
