import React, { useEffect, useRef, useState } from "react"

import { Button } from "primereact/button"
import { Dialog } from "primereact/dialog"
import { InputText } from "primereact/inputtext"
import { InputTextarea } from "primereact/inputtextarea"
import { MultiSelect } from "primereact/multiselect"
import { Password } from "primereact/password"
import { SelectButton } from "primereact/selectbutton"
import { Toast } from "primereact/toast"
import { Toolbar } from "primereact/toolbar"

import { accointsAPI } from "../../api/accounts"
import { Table } from "../../components/data_table/data_table"

import "./accounts.css"

const ENABLE_STATE = [
  { code: 0, name: "Inactive" },
  { code: 1, name: "Active" },
]

const ACTIONS = {
  CREATE: "create",
  EDIT: "edit",
  DELETE: "delete",
}

function Accounts() {
  const toast = useRef(null)
  const [accountDetailsDialog, setAccountDetailsDialog] = useState(false)
  const [deleteDialog, setDeleteDialog] = useState(false)
  const [editingPassword, setEditingPassword] = useState(true)

  const [mode, setMode] = useState("create")

  const [systemApps, setSystemApps] = useState([])
  const [userGroups, setUserGroups] = useState([])
  const [accountDetails, setAccountDetails] = useState({})
  const [searchUser, setSearchUser] = useState("")

  const [table_data, setTableData] = useState([])
  const [tablePage, setTablePage] = useState({
    page: 1,
    offset: 0,
    limit: 10,
  })

  const columns = [
    { header: "Account", field: "account" },
    { header: "Email", field: "email" },
    { header: "Enable", field: "is_active", type: "boolean" },
    { header: "User Groups", field: "user_groups_labels" },
    { header: "Update Time", field: "update_time", type: "date" },
  ]

  const showToast = (severity, summary, detail, life = 3000) => {
    toast.current.show({ severity, summary, detail, life })
  }

  useEffect(() => {
    getAccounts()
    getUserGroups()
    // getSystemApps()
  }, [])

  useEffect(() => {
    console.log("userDetails: ", accountDetails)
  }, [accountDetails])

  const getUserGroups = () => {
    accointsAPI("get", "/group/")
      .then((response) => {
        const groups = response.data.results.map((item) => ({
          name: item.group_name,
          code: item.id,
        }))
        console.log("User Groups: ", response.data.results)
        setUserGroups(groups)
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  const getSystemApps = () => {
    accointsAPI("get", "/systemapps/")
      .then((response) => {
        const apps = response.data.results.map((item) => ({
          name: item.label,
          code: item.id,
        }))
        setSystemApps(apps)
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  const getAccounts = () => {
    const url = searchUser ? `/?account=${searchUser}` : "/"

    accointsAPI("get", `/${url}`, tablePage)
      .then((response) => {
        setTableData(response.data.results)
        if (searchUser != "") {
          showToast(
            "success",
            "Success",
            `Found ${response.data.count} accounts`
          )
        }
        console.log("Accounts data: ", response.data.results)
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  const handleAction = ({ action, data }) => {
    setAccountDetails(data)
    setMode(action)

    if (action === ACTIONS.EDIT) {
      setEditingPassword(false)
      setAccountDetailsDialog(true)
    } else if (action === ACTIONS.DELETE) {
      setDeleteDialog(true)
    }
  }

  const handleSaveAccount = () => {
    console.log("Saving account with details:", accountDetails, mode)

    const action = mode === ACTIONS.CREATE ? "post" : "put"
    const url =
      mode === ACTIONS.CREATE ? "/register/" : `/${accountDetails.id}/`

    accointsAPI(action, url, accountDetails)
      .then(() => {
        showToast("success", "Success", "Account saved successfully.")
        setAccountDetailsDialog(false)
        getAccounts()
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  const headleDeleteUser = () => {
    if (accountDetails.id === undefined) {
      showToast("error", "Error", "No account selected for deletion.")
      return
    }
    if (accountDetails.id === 1) {
      showToast("error", "Error", "Cannot delete the default admin account.")
      return
    }

    accointsAPI("delete", `/${accountDetails.id}/`)
      .then(() => {
        showToast("success", "Success", "Account deleted successfully.")
        setDeleteDialog(false)
        getAccounts()
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  const createAccount = () => {
    setAccountDetailsDialog(true)
    setMode(ACTIONS.CREATE)
  }

  const closeUserDialog = () => {
    setAccountDetailsDialog(false)
    setDeleteDialog(false)
    setAccountDetails({})
    setEditingPassword(true)
  }

  const leftContents = () => (
    <React.Fragment>
      <div className="row g-2">
        <div className="col-8">
          <label>User Account</label>
          <InputText
            className="p-inputtext"
            placeholder="Search for account"
            onChange={(e) => setSearchUser(e.target.value)}
          />
        </div>
        <div className="col-4 align-self-end">
          <Button
            icon="pi pi-search"
            className="func-btn"
            label="Search"
            onClick={getAccounts}
          />
        </div>
      </div>
    </React.Fragment>
  )

  const rightContents = () => (
    <React.Fragment>
      <div className="toolbar-right-content">
        <Button
          icon="pi pi-plus"
          className="p-button-info func-btn "
          label="Create"
          onClick={createAccount}
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
              onClick={handleSaveAccount}
            />
          </div>
          <div>
            <Button
              label="Cancel"
              icon="pi pi-times"
              className="p-button-text cancel-btn"
              onClick={closeUserDialog}
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
            onClick={closeUserDialog}
          />
        </div>
        <div>
          <Button
            label="Sure"
            icon="pi pi-times"
            className="p-button-text delete-btn"
            onClick={headleDeleteUser}
          />
        </div>
      </div>
    </React.Fragment>
  )

  return (
    <div className="general-page-layout">
      <Toast ref={toast} />
      <Toolbar
        className="toolbar-layout"
        left={leftContents}
        right={rightContents}
      />
      <Table
        data={table_data}
        columns={columns}
        tableParams={setTablePage}
        actnioEvent={handleAction}
        editFlag={true}
        deleteFlag={true}
      />
      <Dialog
        visible={accountDetailsDialog}
        className=""
        header={mode == ACTIONS.CREATE ? "Create Account" : "Edit Account"}
        footer={accountDialogFooter}
        onHide={closeUserDialog}
      >
        <div className="account-dialog row">
          <div className="account-dialog-left-content col-8 col-lg-8">
            <div className="">
              <label>Account</label>
              <span className="text-danger">*</span>
              <InputText
                className="p-inputtext"
                placeholder=""
                value={accountDetails ? accountDetails.account : ""}
                onChange={(e) =>
                  setAccountDetails({
                    ...accountDetails,
                    account: e.target.value,
                  })
                }
              />
            </div>
            <div className="">
              <label>Password</label>
              <span className="text-danger">*</span>
              {editingPassword ? (
                <Password
                  placeholder=""
                  feedback={false}
                  toggleMask
                  onChange={(e) =>
                    setAccountDetails({
                      ...accountDetails,
                      password: e.target.value,
                    })
                  }
                />
              ) : (
                <InputText
                  className="p-inputtext"
                  placeholder="********"
                  value={accountDetails ? accountDetails.password : ""}
                  onClick={() => setEditingPassword(true)}
                />
              )}
            </div>
            <div className="">
              <label>Confirm</label>
              <span className="text-danger">*</span>
              <Password
                placeholder=""
                feedback={false}
                toggleMask
                onChange={(e) =>
                  setAccountDetails({
                    ...accountDetails,
                    password: e.target.value,
                  })
                }
              />
            </div>
            <div className="row g-2">
              <div className="col-6 col-lg-6">
                <label>First Name </label>
                <span className="text-danger">*</span>
                <InputText
                  className="p-inputtext"
                  placeholder=""
                  value={accountDetails ? accountDetails.first_name : ""}
                  onChange={(e) =>
                    setAccountDetails({
                      ...accountDetails,
                      first_name: e.target.value,
                    })
                  }
                />
              </div>
              <div className="col-6 col-lg-6">
                <label>Last Name</label>
                <span className="text-danger">*</span>
                <InputText
                  className="p-inputtext"
                  placeholder=""
                  value={accountDetails ? accountDetails.last_name : ""}
                  onChange={(e) =>
                    setAccountDetails({
                      ...accountDetails,
                      last_name: e.target.value,
                    })
                  }
                />
              </div>
            </div>
            <div className="row g-2">
              <div className="col-6 col-lg-6">
                <label>Email </label>
                <InputText
                  className="p-inputtext"
                  placeholder=""
                  value={accountDetails ? accountDetails.email : ""}
                  onChange={(e) =>
                    setAccountDetails({
                      ...accountDetails,
                      email: e.target.value,
                    })
                  }
                />
              </div>
              <div className="col-6 col-lg-6">
                <label>Enable</label>
                <SelectButton
                  className="select-button"
                  value={accountDetails.is_active ? 1 : 0}
                  options={ENABLE_STATE}
                  optionValue="code"
                  optionLabel="name"
                  onChange={(e) =>
                    setAccountDetails({ ...accountDetails, is_active: e.value })
                  }
                />
              </div>
            </div>
            <div>
              <label>Select User Groups</label>
              <MultiSelect
                className="w-100"
                placeholder="Select Groups"
                options={userGroups}
                value={accountDetails.user_groups || []}
                optionValue="code"
                optionLabel="name"
                onChange={(e) =>
                  setAccountDetails({ ...accountDetails, user_groups: e.value })
                }
                maxSelectedLabels={0}
              />
            </div>
            <div>
              <label>Description</label>
              <InputTextarea
                className="w-100"
                value={accountDetails.description}
                row={3}
              />
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
        visible={deleteDialog}
        className=""
        header="Delete Account"
        footer={deleteUserDialogFooter}
        onHide={() => setDeleteDialog(false)}
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
