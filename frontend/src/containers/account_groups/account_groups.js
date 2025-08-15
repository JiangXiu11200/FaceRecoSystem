import React, { useEffect, useRef, useState } from "react"

import { cloneDeep } from "lodash"
import { Button } from "primereact/button"
import { Dialog } from "primereact/dialog"
import { InputText } from "primereact/inputtext"
import { MultiSelect } from "primereact/multiselect"
import { SelectButton } from "primereact/selectbutton"
import { Toast } from "primereact/toast"
import { Toolbar } from "primereact/toolbar"

import { accountsAPI } from "../../api/accounts"
import { Table } from "../../components/data_table/data_table"

import "./account_groups.css"

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

function AccountGroups() {
  const toast = useRef(null)
  const [groupDetails, setGroupDetails] = useState(cloneDeep(EMPTY_GROUP))
  const [groupName, setGroupsName] = useState("")
  const [systemApps, setSystemApps] = useState([])
  const [dialogVisible, setDialogVisible] = useState(false)
  const [deleteDialogVisible, setDeleteDialogVisible] = useState(false)
  const [mode, setMode] = useState(null)

  const [tableGroups, setTableGroups] = useState([])
  const [tablePage, setTablePage] = useState({
    page: 1,
    offset: 0,
    limit: 10,
  })

  const columns = [
    { field: "group_name", header: "Group Name" },
    { field: "apps_name_list", header: "Permissions", type: "array" },
    { field: "is_active", header: "Enable", type: "boolean" },
    { field: "update_time", header: "Update Time", type: "date" },
    { field: "create_time", header: "Create Time", type: "date" },
  ]

  const showToast = (severity, summary, detail, life = 3000) => {
    toast.current.show({ severity, summary, detail, life })
  }

  const getGroups = () => {
    accountsAPI("get", "/group/", tablePage)
      .then((response) => {
        const systemApps = systemAppsFilter(response.data.results)
        setTableGroups(systemApps)
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  const getSystemApps = () => {
    accountsAPI("get", "/systemapps/")
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

  const saveGroup = () => {
    if (!validateGroup()) return

    const isEdit = mode === ACTIONS.EDIT
    const method = isEdit ? "put" : "post"
    const url = isEdit ? `/group/${groupDetails.id}/` : "/group/"

    if (groupDetails.id == 1 && mode == ACTIONS.DELETE) {
      showToast("error", "Error", "Cannot delete the default group.")
      return
    }

    accountsAPI(method, url, groupDetails)
      .then(() => {
        if (groupName) {
          searchGroups()
        } else {
          getGroups()
        }
        showToast("success", "Success", "Group saved successfully")
        closeGroupDialog()
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  const searchGroups = () => {
    accountsAPI("get", `/group/?group_name=${groupName}`, tablePage)
      .then((response) => {
        let _group_count = response.data.count
        const systemApps = systemAppsFilter(response.data.results)
        setTableGroups(systemApps)
        showToast("success", "Success", `Found ${_group_count} matching groups`)
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

  const deleteGroup = () => {
    if (groupDetails.id == 1) {
      showToast("error", "Error", "Cannot delete the default group.")
      return
    }

    accountsAPI("delete", `/group/${groupDetails.id}/`)
      .then(() => {
        showToast("success", "Success", "Group deleted successfully")
        getGroups()
        if (groupName) {
          searchGroups()
        } else {
          getGroups()
        }
        setDeleteDialogVisible(false)
      })
      .catch((err) => {
        showToast("error", "Error", err.response.data)
      })
  }

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

  const systemAppsFilter = (groupData) => {
    return groupData.map((item) => {
      let appsNameDisplay = "Not set"

      if (item.apps_name && item.apps_name.length > 0) {
        if (item.apps_name.length === 1) {
          appsNameDisplay = item.apps_name[0]
        } else {
          appsNameDisplay = `${item.apps_name[0]} ...and ${item.apps_name.length - 1} apps`
        }
      }

      return {
        ...item,
        apps_name_list: appsNameDisplay,
      }
    })
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
    getGroups()
    getSystemApps()
  }, [])

  const leftToolbar = (
    <div className="row g-2 account-group-toolbar-layout">
      <div className="col-6">
        <InputText
          className="p-inputtext"
          placeholder="Search for groups.."
          onChange={(e) => setGroupsName(e.target.value)}
        />
      </div>
      <div className="col-6">
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
    <div>
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
        className="toolbar-layout "
        left={leftToolbar}
        right={rightToolbar}
      />

      <Table
        data={tableGroups}
        columns={columns}
        tableParams={setTablePage}
        actnioEvent={handleAction}
        editFlag
        deleteFlag
      />

      <Dialog
        visible={dialogVisible}
        header={mode === ACTIONS.CREATE ? "Create Group" : "Edit Group"}
        footer={groupDialogFooter}
        onHide={closeGroupDialog}
      >
        <div className="row g-3">
          <div className="col-8">
            <div className="mb-2">
              <label>
                Group Name<span className="text-danger">*</span>
              </label>
              <InputText
                className="p-inputtext"
                placeholder="Group name"
                value={groupDetails.group_name}
                onChange={(e) =>
                  setGroupDetails({
                    ...groupDetails,
                    group_name: e.target.value,
                  })
                }
                disabled={mode === ACTIONS.VIEW}
              />
            </div>
            <div>
              <label>Select Apps</label>
              <MultiSelect
                className="w-100"
                placeholder="Select Apps"
                options={systemApps}
                value={groupDetails ? groupDetails.apps : []}
                optionValue="code"
                optionLabel="name"
                onChange={(e) =>
                  setGroupDetails({ ...groupDetails, apps: e.value })
                }
                maxSelectedLabels={0}
              />
            </div>
          </div>

          <div className="col-4">
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

export default AccountGroups
