import React, { useEffect, useRef, useState } from "react"

import { cloneDeep } from "lodash"
import { Button } from "primereact/button"
import { Dropdown } from "primereact/dropdown"
import { InputText } from "primereact/inputtext"
import { Toast } from "primereact/toast"
import { Toolbar } from "primereact/toolbar"

import { activityLogsApi } from "../../api/activity_logs"
import { userRegistrationApi } from "../../api/user_registration"
import { Table } from "../../components/data_table/data_table"

import "./facial_reco_logs.css"

const EMPTY_SEARCH = {
  name: "",
  group: "",
}

function FacialRecoLogs() {
  const toast = useRef(null)
  const [groups, setGroups] = useState([])
  const [searchUsers, setSearchUsers] = useState(cloneDeep(EMPTY_SEARCH))

  const [table_data, setTableData] = useState([])
  const [set_action_event, setActionEvent] = useState({})
  const [tablePage, setTablePage] = useState({
    page: 1,
    offset: 0,
    limit: 10,
  })

  const columns = [
    { header: "Account", field: "name" },
    { header: "Group", field: "group" },
    { header: "Status", field: "detection_results", type: "boolean" },
    { header: "Timestamp", field: "timestamp", type: "date" },
    { header: "Image", field: "minio_urls", type: "image" },
  ]

  const showToast = (severity, summary, detail, life = 3000) => {
    toast.current.show({ severity, summary, detail, life })
  }

  const fetchGroups = () => {
    userRegistrationApi("get", "/group/", tablePage)
      .then((response) => {
        const group = response.data.results.map((item) => ({
          name: item.group_name,
          code: item.group_name,
        }))
        group.unshift({ name: "All", code: "" })
        setGroups(group)
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  const handleSearchUsers = () => {
    let url = `/?name=${searchUsers.name || ""}&group=${searchUsers.group || ""}`

    activityLogsApi("get", `/face-recognition${url}`, tablePage)
      .then((response) => {
        setTableData(response.data.results)
        if (searchUsers.name !== "" || searchUsers.group !== "") {
          showToast(
            "success",
            "Search Results",
            `Found ${response.data.count} logs`
          )
        }
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  useEffect(() => {
    fetchGroups()
    handleSearchUsers()
  }, [])

  const leftContents = (
    <React.Fragment>
      <div className="facial-reco-toolbar-layout row g-2">
        <div className="col-4">
          <label>User Name</label>
          <InputText
            className="p-inputtext"
            placeholder="User Name"
            onChange={(e) =>
              setSearchUsers({ ...searchUsers, name: e.target.value })
            }
          />
        </div>
        <div className="col-4">
          <label>Group Name</label>
          <Dropdown
            className="w-100"
            placeholder="Select Group"
            options={groups}
            optionLabel="name"
            optionValue="code"
            value={searchUsers.group}
            onChange={(e) => setSearchUsers({ ...searchUsers, group: e.value })}
          />
        </div>
        <div className="col-4 align-self-end">
          <Button
            icon="pi pi-search"
            className="func-btn"
            label="Search"
            onClick={handleSearchUsers}
          />
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
        tableParams={setTablePage}
      />
    </div>
  )
}

export default FacialRecoLogs
