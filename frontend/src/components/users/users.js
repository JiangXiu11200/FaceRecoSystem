import { Button } from "primereact/button"
import { Dialog } from "primereact/dialog"
import { InputText } from "primereact/inputtext"
import { MultiSelect } from "primereact/multiselect"
import { SelectButton } from "primereact/selectbutton"
import { Toast } from "primereact/toast"
import { Toolbar } from "primereact/toolbar"
import React, { useEffect, useMemo, useRef, useState } from "react"

import { Table } from "../data_table/data_table"

import "./users.css"

function Users() {
  const toast = useRef(null)
  const [table_data, setTableData] = useState([])
  const [set_action_event, setActionEvent] = useState({})
  const [set_user_state, setUserState] = useState(0)
  const [set_edit_user, setEditUser] = useState(false)
  const [set_delete_dialog, setDeleteDialog] = useState(false)

  const user_state = useMemo(() => {
    return [
      { code: 0, name: "No" },
      { code: 1, name: "Yes" },
    ]
  }, [])

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
      header: "Register Time",
      field: "register_time",
    },
    {
      header: "Enable",
      field: "enable",
    },
    {
      header: "Annotation",
      field: "annotation",
    },
  ]

  const _mock_data = Array.from({ length: 50 }, (_, i) => ({
    user: `User ${i + 1}`,
    group: `Group ${i + 1}`,
    register_time: `2023-10-01`,
    enable: i % 2 === 0 ? "Yes" : "No",
    annotation: `Annotation ${i + 1}`,
  }))

  useEffect(() => {
    setTableData(_mock_data)
  }, [])

  useEffect(() => {
    console.log("action event", set_action_event)
    switch (set_action_event.action) {
      case "edit":
        setEditUser(true)
        break
      case "delete":
        setDeleteDialog(true)
        break
      default:
        break
    }
  }, [set_action_event])

  const onUserStateChange = (e) => {
    setUserState(e.value)
  }

  const doSaveUser = () => {
    toast.current.show({
      severity: "success",
      summary: "Success",
      detail: "User saved successfully.",
    })
    setEditUser(false)
    setDeleteDialog(false)
  }

  const showDeleteUserDialog = () => {
    setDeleteDialog(true)
  }

  const doDeleteUser = () => {
    toast.current.show({
      severity: "success",
      summary: "Success",
      detail: "User deleted successfully.",
    })
    setDeleteDialog(false)
    setEditUser(false)
  }

  const hideEditUserDialog = () => {
    setEditUser(false)
  }

  const hideUserDetailDialog = () => {
    setDeleteDialog(false)
  }

  const leftContents = (
    <React.Fragment>
      <div className="toolbar-left">
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

  const editUserDialogFooter = (
    <React.Fragment>
      <div className="d-flex justify-content-between">
        <div className="d-flex">
          <Button
            label="Delete"
            icon="pi pi-times"
            className="p-button-text delete-btn"
            onClick={showDeleteUserDialog}
          />
        </div>
        <div className="d-flex">
          <div className="me-2">
            <Button
              label="Save"
              icon="pi pi-check"
              className="p-button-text func-btn"
              onClick={doSaveUser}
            />
          </div>
          <div>
            <Button
              label="Cancel"
              icon="pi pi-times"
              className="p-button-text cancel-btn"
              onClick={hideEditUserDialog}
            />
          </div>
        </div>
      </div>
    </React.Fragment>
  )

  const deleteUserDialogFooter = (
    <React.Fragment>
      <div className="d-flex flex-row justify-content-end">
        <div className="me-2">
          <Button
            label="Cancel"
            icon="pi pi-times"
            className="p-button-text cancel-btn"
            onClick={hideUserDetailDialog}
          />
        </div>
        <div>
          <Button
            label="Sure"
            icon="pi pi-times"
            className="p-button-text delete-btn"
            onClick={doDeleteUser}
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
        editFlag={true}
        deleteFlag={true}
        viewsFlag={false}
      />
      <Dialog
        visible={set_edit_user}
        className=""
        header="Edit User"
        footer={editUserDialogFooter}
        onHide={hideEditUserDialog}
      >
        <div className="edit-user-dialog">
          <div className="right-content">
            <div className="">
              <label>User Name</label>
              <InputText className="p-inputtext" placeholder="" />
            </div>
            <div className="">
              <label>Select Group</label>
              <MultiSelect
                className="w-100"
                placeholder="Select Group"
                options={[]}
                onChange={() => {}}
                optionLabel="name"
              />
            </div>
            <div>
              <label>Enable</label>
              <SelectButton
                className="w-100 select-button"
                value={set_user_state ? set_user_state : 0}
                options={user_state}
                optionValue="code"
                optionLabel="name"
                onChange={(e) => onUserStateChange(e)}
              />
            </div>
            <div>
              <label>Creation Date</label>
              <InputText
                className="p-inputtext"
                placeholder=""
                disabled={true}
              />
            </div>
          </div>
          <div className="left-content">
            <img src="./assets/image/roi_not_found.jpg" alt="" />
          </div>
        </div>
      </Dialog>
      <Dialog
        visible={set_delete_dialog}
        className=""
        header="Delete Group"
        footer={deleteUserDialogFooter}
        onHide={hideUserDetailDialog}
      >
        <div className="d-flex flex-row align-items-center">
          <div>
            <label>Are you sure you want to delete this user?</label>
          </div>
        </div>
      </Dialog>
    </div>
  )
}

export default Users
