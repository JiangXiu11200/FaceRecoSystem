import React, { useEffect, useRef, useState } from "react"

import { cloneDeep } from "lodash"
import { Button } from "primereact/button"
import { Dialog } from "primereact/dialog"
import { Dropdown } from "primereact/dropdown"
import { InputText } from "primereact/inputtext"
import { MultiSelect } from "primereact/multiselect"
import { SelectButton } from "primereact/selectbutton"
import { Toast } from "primereact/toast"
import { Toolbar } from "primereact/toolbar"

import { userRegistrationApi } from "../../api/user_registration"
import { Table } from "../../components/data_table/data_table"

import "./users.css"

const GROUP_STATE_OPTIONS = [
  { code: 0, name: "No" },
  { code: 1, name: "Yes" },
]

const EMPTY_USER = {
  name: "",
  register_group: "",
  is_active: 0,
  annotations: "",
}

const DEFAULT_GROUP = {
  code: "",
  name: "None",
}

const SEARCH_GROUPS = {
  register_group: [],
  name: "",
}

const ACTIONS = {
  VIEW: "view",
  EDIT: "edit",
  CREATE: "create",
  DELETE: "delete",
}

function Users() {
  const toast = useRef(null)
  const [table_data, setTableData] = useState([])
  const [userDetails, setUserDetails] = useState(cloneDeep(EMPTY_USER))
  const [groupDetails, setGroupDetails] = useState({})
  const [searchGroupsList, setSearchGroupsList] = useState([])
  const [searchGroups, setSearchGroups] = useState(cloneDeep(SEARCH_GROUPS))

  const [editUserVisible, setEditUserVisible] = useState(false)
  const [deleteDialogVisible, setDeleteDialogVisible] = useState(false)
  const [tablePage, setTablePage] = useState({
    page: 1,
    offset: 0,
    limit: 10,
  })

  const columns = [
    { field: "name", header: "User" },
    { field: "register_group_name", header: "Group" },
    { field: "register_time", header: "Register Time", type: "date" },
    { field: "update_time", header: "Update Time", type: "date" },
    { field: "is_active", header: "Enable", type: "boolean" },
    { field: "annotations", header: "Annotations" },
  ]

  const showToast = (severity, summary, detail, life = 3000) => {
    toast.current.show({ severity, summary, detail, life })
  }

  const getUserList = () => {
    const queryGroups = searchGroups.register_group.join(",")

    userRegistrationApi(
      "get",
      `/?name=${searchGroups.name}&register_group=${queryGroups}`,
      tablePage
    )
      .then((response) => {
        setTableData(response.data.results)
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  const getGroupList = () => {
    userRegistrationApi("get", "/group/")
      .then((response) => {
        const groups = response.data.results.map((group) => ({
          code: group.id,
          name: group.group_name,
        }))
        const forUserDetails = [DEFAULT_GROUP, ...groups]
        setSearchGroupsList(groups)
        setGroupDetails(forUserDetails)
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  const updateUserDetails = () => {
    if (!validateUser()) return

    userRegistrationApi("put", `/${userDetails.id}/`, userDetails)
      .then(() => {
        showToast("success", "Success", "User updated successfully.")
        getUserList()
        setEditUserVisible(false)
        setDeleteDialogVisible(false)
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  const deleteUser = () => {
    userRegistrationApi("delete", `/${userDetails.id}/`)
      .then(() => {
        showToast("success", "Success", "User deleted successfully.")
        getUserList()
        setEditUserVisible(false)
        setDeleteDialogVisible(false)
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  const validateUser = () => {
    const validations = [
      {
        cond: userDetails.name.trim() === "",
        msg: "User name cannot be empty.",
      },
      {
        cond: /^\d/.test(userDetails.name),
        msg: "User name cannot start with a number.",
      },
      {
        cond: userDetails.is_active === undefined,
        msg: "Please select if the user is active.",
      },
    ]

    for (const { cond, msg } of validations) {
      if (cond) {
        showToast("error", "Error", msg)
        return false
      }
    }
    return true
  }

  const handleAction = ({ action, data }) => {
    setUserDetails(data)
    if (action === ACTIONS.DELETE) {
      setDeleteDialogVisible(true)
    } else {
      setEditUserVisible(true)
    }
  }

  const showDeleteUserDialog = () => {
    setDeleteDialogVisible(true)
  }

  const hideEditUserDialog = () => {
    setEditUserVisible(false)
  }

  const hideUserDetailDialog = () => {
    setDeleteDialogVisible(false)
  }

  useEffect(() => {
    getUserList()
    getGroupList()
  }, [])

  const leftContents = (
    <React.Fragment>
      <div className="user-toolbar-layout row g-2">
        <div className="col-4">
          <InputText
            className=""
            placeholder="Search for groups.."
            onChange={(e) =>
              setSearchGroups({ ...searchGroups, name: e.target.value })
            }
          />
        </div>
        <div className="col-4">
          <MultiSelect
            className="w-100"
            placeholder="Select Group"
            value={
              searchGroups.register_group ? searchGroups.register_group : []
            }
            options={searchGroupsList || []}
            onChange={(e) =>
              setSearchGroups({ ...searchGroups, register_group: e.value })
            }
            optionLabel="name"
            optionValue="code"
            maxSelectedLabels={1}
          />
        </div>
        <div className="col-4">
          <Button
            icon="pi pi-search"
            className="func-btn"
            label="Search"
            onClick={getUserList}
          />
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
              label="Cancel"
              icon="pi pi-times"
              className="p-button-text cancel-btn"
              onClick={hideEditUserDialog}
            />
          </div>
          <div>
            <Button
              label="Save"
              icon="pi pi-check"
              className="p-button-text func-btn"
              onClick={updateUserDetails}
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
            label="Delete"
            icon="pi pi-times"
            className="p-button-text delete-btn"
            onClick={deleteUser}
          />
        </div>
      </div>
    </React.Fragment>
  )

  return (
    <div className="d-flex flex-column">
      <Toast ref={toast} />
      <Toolbar className="toolbar-layout " left={leftContents} />
      <Table
        data={table_data}
        columns={columns}
        tableParams={setTablePage}
        actnioEvent={handleAction}
        editFlag
        deleteFlag
      />
      <Dialog
        visible={editUserVisible}
        className=""
        header="Edit User"
        footer={editUserDialogFooter}
        onHide={hideEditUserDialog}
      >
        <div className="edit-user-dialog">
          <div className="right-content">
            <div className="">
              <label>User Name</label>
              <InputText
                className="p-inputtext"
                placeholder=""
                value={userDetails.name}
                onChange={(e) =>
                  setUserDetails({ ...userDetails, name: e.target.value })
                }
              />
            </div>
            <div className="">
              <label>Select Group</label>
              <Dropdown
                className="w-100"
                placeholder="Select Group"
                value={userDetails ? userDetails.register_group : ""}
                options={groupDetails}
                optionValue="code"
                optionLabel="name"
                onChange={(e) =>
                  setUserDetails({
                    ...userDetails,
                    register_group: e.value,
                  })
                }
              />
            </div>
            <div>
              <label>Enable</label>
              <SelectButton
                className="w-100 select-button"
                value={userDetails.is_active ? 1 : 0}
                options={GROUP_STATE_OPTIONS}
                optionValue="code"
                optionLabel="name"
                onChange={(e) =>
                  setUserDetails({ ...userDetails, is_active: e.value })
                }
              />
            </div>
            <div>
              <label>Creation Date</label>
              <InputText
                className="p-inputtext"
                placeholder=""
                value={new Date(userDetails.register_time).toLocaleString()}
                disabled={true}
              />
            </div>
          </div>
          <div className="left-content">
            <img
              src={
                userDetails.register_picture_url
                  ? userDetails.register_picture_url
                  : "/static/image/roi_not_found.jpg"
              }
              alt="User"
            />
          </div>
        </div>
      </Dialog>
      <Dialog
        visible={deleteDialogVisible}
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
