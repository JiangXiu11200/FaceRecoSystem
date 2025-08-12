import React, { useEffect, useMemo, useState, useRef } from "react"
import { Button } from "primereact/button"
import { Dialog } from "primereact/dialog"
import { InputText } from "primereact/inputtext"
import { SelectButton } from "primereact/selectbutton"
import { Toolbar } from "primereact/toolbar"
import { Toast } from "primereact/toast"
import { cloneDeep } from "lodash"

import { userRegistrationApi } from "../../api/user_registration"
import { Table } from "../../components/data_table/data_table"
import "./group.css"

const GROUP_STATE_OPTIONS = [
  { code: 0, name: "No" },
  { code: 1, name: "Yes" },
]

const EMPTY_GROUP = {
  group_name: "",
  is_active: 0,
}

const ACTIONS = {
  VIEW: "view",
  EDIT: "edit",
  CREATE: "create",
  DELETE: "delete",
}

function Group() {
  const toast = useRef(null)

  // State
  const [products, setProducts] = useState([])
  const [dialogVisible, setDialogVisible] = useState(false)
  const [deleteDialogVisible, setDeleteDialogVisible] = useState(false)
  const [mode, setMode] = useState(null) // "view" | "edit" | "create" | null
  const [groupDetails, setGroupDetails] = useState(cloneDeep(EMPTY_GROUP))
  const [groupName, setGroupsName] = useState("")
  const [tablePage, setTablePage] = useState({
    page: 1,
    offset: 0,
    limit: 10,
  })

  const columns = [
    { field: "group_name", header: "Group Name" },
    { field: "user_count", header: "User counts" },
    { field: "is_active", header: "Enable", type: "boolean" },
    { field: "update_time", header: "Update Time", type: "date" },
  ]

  // Toast helper
  const showToast = (severity, summary, detail, life = 3000) => {
    toast.current.show({ severity, summary, detail, life })
  }

  // API: Fetch group list
  const fetchGroups = () => {
    userRegistrationApi("get", "/group/", tablePage)
      .then((response) => {
        setProducts(response.data.results)
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  // API: Create or update group
  const saveGroup = () => {
    if (!validateGroup()) return

    const isEdit = mode === ACTIONS.EDIT
    const method = isEdit ? "put" : "post"
    const url = isEdit ? `/group/${groupDetails.id}/` : "/group/"

    userRegistrationApi(method, url, groupDetails)
      .then(() => {
        if (groupName) {
          searchGroups()
        } else {
          fetchGroups()
        }
        closeGroupDialog()
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  // API: Group name fuzzy search
  const searchGroups = () => {
    userRegistrationApi("get", `/group/?group_name=${groupName}`, tablePage)
      .then((response) => {
        let _group_count = response.data.count
        setProducts(response.data.results)
        showToast("success", "Success", `Found ${_group_count} matching groups`)
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  // API: Delete group
  const deleteGroup = () => {
    userRegistrationApi("delete", `/group/${groupDetails.id}/`)
      .then(() => {
        showToast("success", "Success", "Group deleted successfully")
        fetchGroups()
        if (groupName) {
          searchGroups()
        } else {
          fetchGroups()
        }
        setDeleteDialogVisible(false)
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  // Validation
  const validateGroup = () => {
    const validations = [
      {
        cond: groupDetails.group_name.trim() === "",
        msg: "Please enter group name.",
      },
      {
        cond: /^\d/.test(groupDetails.group_name),
        msg: "Group name cannot start with a number.",
      },
      {
        cond: /[^a-zA-Z0-9\s]/.test(groupDetails.group_name),
        msg: "Group name cannot contain special characters.",
      },
      {
        cond: groupDetails.is_active === undefined,
        msg: "Please select group status.",
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
    setGroupDetails(cloneDeep(data))
    setMode(action)

    if (action === ACTIONS.DELETE) {
      setDeleteDialogVisible(true)
    } else {
      setDialogVisible(true)
    }
  }

  const closeGroupDialog = () => {
    setDialogVisible(false)
    setMode(null)
    setGroupDetails(cloneDeep(EMPTY_GROUP))
  }

  useEffect(() => {
    fetchGroups()
  }, [tablePage])

  const leftToolbar = (
    <div className="toolbar-left">
      <div>
        <InputText
          className="p-inputtext"
          placeholder="Search for groups.."
          onChange={(e) => setGroupsName(e.target.value)}
        />
      </div>
      <div>
        <Button
          icon="pi pi-search"
          className="func-btn"
          label="Search"
          onClick={searchGroups}
        />
      </div>
    </div>
  )

  const rightToolbar = (
    <div className="toolbar-right">
      <Button
        icon="pi pi-plus"
        className="p-button-info func-btn"
        label="Add Group"
        onClick={() => {
          setMode(ACTIONS.CREATE)
          setDialogVisible(true)
        }}
      />
    </div>
  )

  const groupDialogFooter = (
    <div className="d-flex flex-row justify-content-end">
      <div className="me-2">
        <Button
          label="Cancel"
          icon="pi pi-times"
          className="p-button-text cancel-btn"
          onClick={closeGroupDialog}
        />
      </div>
      {(mode === ACTIONS.CREATE || mode === ACTIONS.EDIT) && (
        <div>
          <Button
            label={mode === ACTIONS.CREATE ? "Create" : "Save"}
            icon="pi pi-check"
            className="p-button-text func-btn"
            onClick={saveGroup}
          />
        </div>
      )}
    </div>
  )

  const deleteDialogFooter = (
    <div className="d-flex flex-row justify-content-end">
      <div className="me-2">
        <Button
          label="Cancel"
          icon="pi pi-times"
          className="p-button-text cancel-btn"
          onClick={() => setDeleteDialogVisible(false)}
        />
      </div>
      <div>
        <Button
          label="Delete"
          icon="pi pi-times"
          className="p-button-text delete-btn"
          onClick={deleteGroup}
        />
      </div>
    </div>
  )

  return (
    <div className="d-flex flex-column">
      <Toast ref={toast} />
      <Toolbar
        className="toolbar-layout"
        left={leftToolbar}
        right={rightToolbar}
      />

      <Table
        data={products}
        columns={columns}
        tableParams={setTablePage}
        actnioEvent={handleAction}
        editFlag
        deleteFlag
        viewsFlag
      />

      <Dialog
        visible={dialogVisible}
        header={
          mode === ACTIONS.CREATE
            ? "Create Group"
            : mode === ACTIONS.EDIT
              ? "Edit Group"
              : "Group Details"
        }
        footer={groupDialogFooter}
        onHide={closeGroupDialog}
      >
        <div className="d-flex flex-row align-items-center">
          <div className="me-4">
            <label>
              Group Name<span className="text-danger">*</span>
            </label>
            <InputText
              className="p-inputtext"
              placeholder="Group name"
              value={groupDetails.group_name}
              onChange={(e) =>
                setGroupDetails({ ...groupDetails, group_name: e.target.value })
              }
              disabled={mode === ACTIONS.VIEW}
            />
          </div>
          <div>
            <label>
              Enable<span className="text-danger">*</span>
            </label>
            <SelectButton
              className="w-100 select-button"
              value={groupDetails.is_active ? 1 : 0}
              options={GROUP_STATE_OPTIONS}
              optionValue="code"
              optionLabel="name"
              onChange={(e) =>
                setGroupDetails({ ...groupDetails, is_active: e.value })
              }
              disabled={mode === ACTIONS.VIEW}
              unselectable={false}
            />
          </div>
        </div>
      </Dialog>

      <Dialog
        visible={deleteDialogVisible}
        header="Delete Group"
        footer={deleteDialogFooter}
        onHide={() => setDeleteDialogVisible(false)}
      >
        <label>Are you sure you want to delete this group?</label>
      </Dialog>
    </div>
  )
}

export default Group
