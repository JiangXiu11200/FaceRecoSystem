import { Button } from "primereact/button"
import { Dialog } from "primereact/dialog"
import { InputText } from "primereact/inputtext"
import { InputTextarea } from "primereact/inputtextarea"
import { MultiSelect } from "primereact/multiselect"
import { Password } from "primereact/password"
import { SelectButton } from "primereact/selectbutton"
import { Toast } from "primereact/toast"
import { Toolbar } from "primereact/toolbar"
import React, { useEffect, useMemo, useRef, useState } from "react"

import { Table } from "../../components/data_table/data_table"

import "./accounts.css"

function Accounts() {
  const toast = useRef(null)
  const [table_data, setTableData] = useState([])
  const [set_action_event, setActionEvent] = useState({})
  const [set_enable_state, setEnableState] = useState(0)
  const [set_account_dialog, setAccountDialog] = useState(false)
  const [set_dialog_mode, setDialogMode] = useState("create")
  const [set_delete_dialog, setDeleteDialog] = useState(false)

  const enable_state = useMemo(() => {
    return [
      { code: 0, name: "Inactive" },
      { code: 1, name: "Active" },
    ]
  }, [])

  const columns = [
    {
      header: "User",
      field: "user",
    },
    {
      header: "Email",
      field: "email",
    },
    {
      header: "Status",
      field: "status",
      type: "boolean",
    },
    {
      header: "Permission",
      field: "permission",
    },
    {
      header: "Change Time",
      field: "change_time",
    },
  ]

  const _mock_data = Array.from({ length: 30 }, (_, i) => ({
    user: `User ${i + 1}`,
    email: `user${i + 1}@example.com`,
    status: i % 2 === 0,
    permission: `Permission ${i + 1}`,
    change_time: `2023-10-01`,
  }))

  useEffect(() => {
    setTableData(_mock_data)
  }, [])

  useEffect(() => {
    console.log("action event", set_action_event)
    switch (set_action_event.action) {
      case "edit":
        setDialogMode("edit")
        setAccountDialog(true)
        break
      case "delete":
        setDeleteDialog(true)
        break
      default:
        break
    }
  }, [set_action_event])

  const doSaveAccount = () => {
    toast.current.show({
      severity: "success",
      summary: "Success",
      detail: "Account saved successfully.",
    })
    setAccountDialog(false)
    setDeleteDialog(false)
  }

  const doCreateAccount = () => {
    setAccountDialog(true)
    setDialogMode("create")
  }

  const doDeleteUser = () => {
    toast.current.show({
      severity: "success",
      summary: "Success",
      detail: "Account deleted successfully.",
    })
    setDeleteDialog(false)
    setAccountDialog(false)
  }

  const hideAccountDialog = () => {
    setAccountDialog(false)
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

  const rightContents = (
    <React.Fragment>
      <div className="toolbar-right">
        <Button
          icon="pi pi-plus"
          className="p-button-info func-btn"
          label="Create"
          onClick={doCreateAccount}
        />
      </div>
    </React.Fragment>
  )

  const accountDialogFooter = (
    <React.Fragment>
      <div className="d-flex justify-content-end">
        <div className="d-flex">
          <div className="me-2">
            <Button
              label="Save"
              icon="pi pi-check"
              className="p-button-text func-btn"
              onClick={doSaveAccount}
            />
          </div>
          <div>
            <Button
              label="Cancel"
              icon="pi pi-times"
              className="p-button-text cancel-btn"
              onClick={hideAccountDialog}
            />
          </div>
        </div>
      </div>
    </React.Fragment>
  )

  const onEnableStateChange = (e) => {
    setEnableState(e.value)
  }

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
    <div className="container-layout general-page-layout">
      <Toast ref={toast} />
      <Toolbar
        className="toolbar-layout"
        left={leftContents}
        right={rightContents}
      />
      <Table
        data={table_data}
        columns={columns}
        actnioEvent={setActionEvent}
        editFlag={true}
        deleteFlag={true}
        tableHeight="70vh"
      />
      <Dialog
        visible={set_account_dialog}
        className=""
        header={
          set_dialog_mode === "create" ? "Create Account" : "Edit Account"
        }
        footer={accountDialogFooter}
        onHide={hideAccountDialog}
      >
        <div className="account-dialog row">
          <div className="account-dialog-left-content col-8 col-lg-8">
            <div className="">
              <label>Account</label>
              <span className="text-danger">*</span>
              <InputText className="p-inputtext" placeholder="" />
            </div>
            <div className="">
              <label>Password</label>
              <span className="text-danger">*</span>
              <Password placeholder="" feedback={false} />
            </div>
            <div className="">
              <label>Confirm</label>
              <span className="text-danger">*</span>
              <Password placeholder="" feedback={false} />
            </div>
            <div className="row g-2">
              <div className="col-6 col-lg-6">
                <label>First Name </label>
                <span className="text-danger">*</span>
                <InputText className="p-inputtext" placeholder="" />
              </div>
              <div className="col-6 col-lg-6">
                <label>Last Name</label>
                <span className="text-danger">*</span>
                <InputText className="p-inputtext" placeholder="" />
              </div>
            </div>
            <div className="row g-2">
              <div className="col-6 col-lg-6">
                <label>Email </label>
                <InputText className="p-inputtext" placeholder="" />
              </div>
              <div className="col-6 col-lg-6">
                <label>Enable</label>
                <SelectButton
                  className="select-button"
                  value={set_enable_state ? set_enable_state : 0}
                  options={enable_state}
                  optionValue="code"
                  optionLabel="name"
                  onChange={(e) => onEnableStateChange(e)}
                />
              </div>
            </div>
            <div>
              <label>Select Applications</label>
              <MultiSelect
                className="w-100"
                placeholder="Select Applications"
                options={[]}
                onChange={() => {}}
                optionLabel="name"
              />
            </div>
            <div>
              <label>Description</label>
              <InputTextarea className="w-100" value={""} rows={3} />
            </div>
          </div>
          <div className="col-4 col-lg-4">
            <div className="account-dialog-right-img">
              <img src="/image/roi_not_found.jpg" alt="" />
            </div>
            <div className="account-dialog-right-content mt-2">
              <Button className="func-btn" label="Upload" icon="pi pi-upload" />
            </div>
          </div>
        </div>
      </Dialog>
      <Dialog
        visible={set_delete_dialog}
        className=""
        header="Delete Account"
        footer={deleteUserDialogFooter}
        onHide={hideUserDetailDialog}
      >
        <div className="d-flex flex-row align-items-center">
          <div>
            <label>Are you sure you want to delete this account?</label>
          </div>
        </div>
      </Dialog>
    </div>
  )
}

export default Accounts
