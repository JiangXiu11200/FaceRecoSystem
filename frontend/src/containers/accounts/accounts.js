import React, { useEffect, useRef, useState } from "react"

import clone from "clone-deep"
import { Button } from "primereact/button"
import { Dialog } from "primereact/dialog";
import { FileUpload } from "primereact/fileupload"
import { InputText } from "primereact/inputtext"
import { InputTextarea } from "primereact/inputtextarea"
import { MultiSelect } from "primereact/multiselect"
import { Password } from "primereact/password"
import { SelectButton } from "primereact/selectbutton"
import { Toast } from "primereact/toast"
import { Toolbar } from "primereact/toolbar"

import { accountsAPI } from "../../api/accounts"
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

const EMPTY_PASSWORD = {
  old_password: "",
  new_password: "",
}

const EMPTY_USER_DETAILS = {
  account: "",
  password: "",
  password_confirm: "",
  first_name: "",
  last_name: "",
  email: "",
  is_active: true,
  user_groups: [],
  description: "",
}

function Accounts() {
  const toast = useRef(null)
  const [accountDetailsDialog, setAccountDetailsDialog] = useState(false)
  const [deleteDialog, setDeleteDialog] = useState(false)
  const [passwordDialog, setPasswordDialog] = useState(false)
  const [changePassword, setChangePassword] = useState(clone(EMPTY_PASSWORD))

  const fileUploadRef = useRef(null)
  const [uploading, setUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [accountPhotoStickers, setAccountPhotoStickers] = useState(null)

  const [mode, setMode] = useState("create")
  const [userGroups, setUserGroups] = useState([])
  const [accountDetails, setAccountDetails] = useState(
    clone(EMPTY_USER_DETAILS)
  )
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
    { header: "User Groups", field: "user_group_labels" },
    { header: "Update Time", field: "update_time", type: "date" },
  ]

  const showToast = (severity, summary, detail, life = 3000) => {
    toast.current.show({ severity, summary, detail, life })
  }

  useEffect(() => {
    getAccounts()
    getUserGroups()
  }, [])

  useEffect(() => {}, [accountDetails])

  const getUserGroups = () => {
    accountsAPI("get", "/group/")
      .then((response) => {
        const groups = response.data.results.map((item) => ({
          name: item.group_name,
          code: item.id,
        }))
        setUserGroups(groups)
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  const getAccounts = () => {
    const url = searchUser ? `/?account=${searchUser}` : "/"

    accountsAPI("get", `/${url}`, tablePage)
      .then((response) => {
        setTableData(response.data.results)
        if (searchUser != "") {
          showToast(
            "success",
            "Success",
            `Found ${response.data.count} accounts`
          )
        }
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  const handleAction = ({ action, data }) => {
    setAccountDetails(data)
    setAccountPhotoStickers(data.profile_picture || null)
    setMode(action)

    if (action === ACTIONS.EDIT) {
      setAccountDetailsDialog(true)
    } else if (action === ACTIONS.DELETE) {
      setDeleteDialog(true)
    }
  }

  const handleSaveAccount = () => {
    if (!accountDetails.account.trim()) {
      showToast("error", "Error", "Account name cannot be empty.")
      return
    }

    if (mode === ACTIONS.CREATE || accountDetails.password) {
      if (!accountDetails.password) {
        showToast("error", "Error", "Password is required.")
        return
      }

      if (!accountDetails.password_confirm) {
        showToast("error", "Error", "Password confirmation is required.")
        return
      }

      if (accountDetails.password !== accountDetails.password_confirm) {
        showToast("error", "Error", "Passwords do not match.")
        return
      }
    }

    const action = mode === ACTIONS.CREATE ? "post" : "put"
    const url =
      mode === ACTIONS.CREATE ? "/register/" : `/${accountDetails.id}/`

    accountsAPI(action, url, accountDetails)
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

    accountsAPI("delete", `/${accountDetails.id}/`)
      .then(() => {
        showToast("success", "Success", "Account deleted successfully.")
        setDeleteDialog(false)
        getAccounts()
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  const handleChangePassword = () => {
    if (accountDetails.id === undefined) {
      showToast("error", "Error", "No account selected for password change.")
      return
    }
    if (
      changePassword.old_password === "" ||
      changePassword.new_password === ""
    ) {
      showToast("error", "Error", "Please fill in all password fields.")
      return
    }

    accountsAPI(
      "post",
      `/change-password/${accountDetails.id}/`,
      changePassword
    )
      .then(() => {
        showToast("success", "Success", "Password updated successfully.")
        setPasswordDialog(false)
        setChangePassword(clone(EMPTY_PASSWORD))
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
        return
      })
  }

  const handleUpload = async (event) => {
    if (!accountDetails?.id) {
      showToast("error", "Error", "No account selected for upload.")
      return
    }

    if (!event.files || !event.files.length) {
      showToast("error", "Error", "Please select a file to upload.")
      return
    }

    const file = event.files[0]
    const maxSize = 5 * 1024 * 1024
    if (file.size > maxSize) {
      showToast("error", "Error", "File size must be less than 5MB")
      return
    }

    const allowedTypes = ["image/jpeg", "image/jpg", "image/png"]
    if (!allowedTypes.includes(file.type)) {
      showToast(
        "error",
        "Error",
        "Please upload a valid image file (JPEG, JPG, PNG)"
      )
      return
    }

    setUploading(true)

    const formData = new FormData()
    formData.append("file", file)
    formData.append("user_id", accountDetails.id)
    formData.append("file_name", file.name)
    formData.append("file_type", file.type)
    formData.append("file_size", file.size)

    accountsAPI("post", `/upload-photo-stickers/`, formData)
      .then((response) => {
        showToast("success", "Success", "Image uploaded successfully!")
        setUploading(false)
        setAccountPhotoStickers(response.data.image_url || null)
      })
      .catch((err) => {
        console.error("Upload error:", err)
        showToast(
          "error",
          "Upload Failed",
          err.response?.data || "An error occurred during upload"
        )
      })
  }

  const createAccount = () => {
    setAccountDetailsDialog(true)
    setMode(ACTIONS.CREATE)
  }

  const closeUserDialog = () => {
    setAccountDetailsDialog(false)
    setDeleteDialog(false)
    setAccountDetails(clone(EMPTY_USER_DETAILS))
    setAccountPhotoStickers(null)
  }

  const closePasswordDialog = () => {
    setPasswordDialog(false)
    setChangePassword(clone(EMPTY_PASSWORD))
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
              label="Cancel"
              icon="pi pi-times"
              className="p-button-text cancel-btn"
              onClick={closeUserDialog}
            />
          </div>
          <div>
            <Button
              label="Save"
              icon="pi pi-check"
              className="p-button-text func-btn"
              onClick={handleSaveAccount}
            />
          </div>
        </div>
      </div>
    </React.Fragment>
  )

  const passwordDialogFooter = (
    <React.Fragment>
      <div className="d-flex justify-content-end">
        <div className="me-2">
          <Button
            label="Cancel"
            icon="pi pi-times"
            className="p-button-text cancel-btn"
            onClick={closePasswordDialog}
          />
        </div>
        <div>
          <Button
            label="Save"
            icon="pi pi-check"
            className="p-button-text func-btn"
            onClick={handleChangePassword}
          />
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
            <div className="d-flex flex-row">
              <div className="w-100 me-2">
                <label>Password</label>
                <span className="text-danger">*</span>
                <Password
                  placeholder={mode === ACTIONS.CREATE ? "" : "***************"}
                  feedback={false}
                  toggleMask={mode === ACTIONS.CREATE ? true : false}
                  disabled={mode === ACTIONS.EDIT}
                  onChange={(e) =>
                    setAccountDetails({
                      ...accountDetails,
                      password: e.target.value,
                    })
                  }
                />
              </div>
              <div className="align-self-end">
                <Button
                  className="func-btn"
                  label="Edit"
                  icon="pi pi-unlock"
                  onClick={() => setPasswordDialog(true)}
                  disabled={mode === ACTIONS.CREATE}
                />
              </div>
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
                    password_confirm: e.target.value,
                  })
                }
              />
            </div>
            <div className="row g-2">
              <div className="col-6 col-lg-6">
                <label>First Name </label>
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
              <img
                className="img-square"
                src={
                  accountPhotoStickers
                    ? accountPhotoStickers
                    : accountDetails.profile_picture_url
                      ? accountDetails.profile_picture_url
                      : "/image/roi_not_found.jpg"
                }
                alt=""
              />
            </div>
            <div className="account-dialog-right-content mt-2">
              <div className="upload-section">
                <FileUpload
                  ref={fileUploadRef}
                  name="file"
                  customUpload
                  auto
                  chooseLabel={uploading ? "Uploading..." : "Upload"}
                  mode="basic"
                  disabled={uploading}
                  className="upload-btn"
                  icon={uploading ? "pi pi-spin pi-spinner" : "pi pi-upload"}
                  accept="image/*"
                  maxFileSize={5000000}
                  uploadHandler={handleUpload}
                />
              </div>
            </div>
          </div>
        </div>
      </Dialog>

      <Dialog
        visible={passwordDialog}
        header={"Change Password"}
        footer={passwordDialogFooter}
        onHide={() => setPasswordDialog(false)}
      >
        <div className="">
          <div className="mb-2">
            <label>Old Password</label>
            <span className="text-danger">*</span>
            <Password
              placeholder=""
              feedback={false}
              toggleMask
              value={changePassword.old_password}
              onChange={(e) =>
                setChangePassword({
                  ...changePassword,
                  old_password: e.target.value,
                })
              }
            />
          </div>
          <div>
            <label>New Password</label>
            <span className="text-danger">*</span>
            <Password
              feedback={false}
              toggleMask
              value={changePassword.new_password}
              onChange={(e) =>
                setChangePassword({
                  ...changePassword,
                  new_password: e.target.value,
                })
              }
            />
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
