import { Button } from "primereact/button"
import { Dialog } from "primereact/dialog"
import { InputText } from "primereact/inputtext"
import { Toolbar } from "primereact/toolbar"
import React, { useEffect, useState, useMemo } from "react"
import { SelectButton } from "primereact/selectbutton"

import { Table } from "../data_table/data_table"

import "./group.css"

function Group() {
  const [products, setProducts] = useState([])
  const [set_action_event, setActionEvent] = useState({})
  const [set_group_dialog, setGroupDialog] = useState(false)
  const [set_delete_dialog, setDeleteDialog] = useState(false)
  const [set_group_state, setGroupState] = useState(0)
  const [edit_group, setEditGroup] = useState(false)
  const [create_group, setCreateGroup] = useState(false)

  const group_state = useMemo(() => {
    return [
      { code: 0, name: "No" },
      { code: 1, name: "Yes" },
    ]
  }, [])

  const columns = [
    { field: "code", header: "Code" },
    { field: "name", header: "Name" },
    { field: "category", header: "Category" },
    { field: "quantity", header: "Quantity" },
  ]

  const _mock_data = Array.from({ length: 110 }, (_, i) => ({
    code: `P${String(i + 1).padStart(3, "0")}`,
    name: `Product ${i + 1}`,
    category: `Category ${i + 1}`,
    quantity: (i + 1) * 10,
  }))

  useEffect(() => {
    setProducts(_mock_data)
  }, [])

  useEffect(() => {
    console.log("action event", set_action_event)
    switch (set_action_event.action) {
      case "edit":
        setEditGroup(true)
        setGroupDialog(true)
        break
      case "delete":
        setDeleteDialog(true)
        break
      case "view":
        setGroupDialog(true)
        break
      default:
        break
    }
  }, [set_action_event])

  const showCreateGroupDialog = () => {
    setGroupDialog(true)
    setCreateGroup(true)
  }

  const showEditGroupDialog = () => {
    setGroupDialog(true)
    setEditGroup(true)
  }

  const hideGroupDetailDialog = () => {
    setGroupDialog(false)
    setEditGroup(false)
    setCreateGroup(false)
  }

  const hideDeleteGroupDialog = () => {
    setDeleteDialog(false)
  }

  const onGroupStateChange = (e) => {
    setGroupState(e.value)
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
          label="Add Group"
          onClick={showCreateGroupDialog}
        />
      </div>
    </React.Fragment>
  )

  const groupDetailDialogFooter = (
    <React.Fragment>
      <div className="d-flex flex-row justify-content-end">
        <div className="me-2">
          <Button
            label="Cancel"
            icon="pi pi-times"
            className="p-button-text cancel-btn"
            onClick={hideGroupDetailDialog}
          />
        </div>
        <div>
          {!edit_group && !create_group ? null : create_group ? (
            <Button
              label="Create"
              icon="pi pi-check"
              className="p-button-text func-btn"
              onClick={hideGroupDetailDialog}
            />
          ) : (
            <Button
              label="Save"
              icon="pi pi-check"
              className="p-button-text func-btn"
              onClick={hideGroupDetailDialog}
            />
          )}
        </div>
      </div>
    </React.Fragment>
  )

  const deleteGroupDialogFooter = (
    <React.Fragment>
      <div className="d-flex flex-row justify-content-end">
        <div className="me-2">
          <Button
            label="Cancel"
            icon="pi pi-times"
            className="p-button-text cancel-btn"
            onClick={hideGroupDetailDialog}
          />
        </div>
        <div>
          <Button
            label="Delete"
            icon="pi pi-times"
            className="p-button-text delete-btn"
            onClick={hideGroupDetailDialog}
          />
        </div>
      </div>
    </React.Fragment>
  )

  return (
    <div className="d-flex flex-column">
      <Toolbar
        className="toolbar-layout"
        left={leftContents}
        right={rightContents}
      />
      <Table
        data={products}
        columns={columns}
        actnioEvent={setActionEvent}
        editFlag={true}
        deleteFlag={true}
        viewsFlag={true}
      />
      <Dialog
        visible={set_group_dialog}
        className=""
        header={
          create_group
            ? "Create Group"
            : edit_group
              ? "Edit Group"
              : "Group Details"
        }
        footer={groupDetailDialogFooter}
        onHide={hideGroupDetailDialog}
      >
        <div className="d-flex flex-row align-items-center">
          <div className="me-4">
            <label>Group Name</label>
            <span className="text-danger">*</span>
            <InputText className="p-inputtext" placeholder="Group name" />
          </div>
          <div>
            <label>Enable</label>
            <span className="text-danger">*</span>
            <SelectButton
              className="w-100 select-button"
              value={set_group_state ? set_group_state : 0}
              options={group_state}
              optionValue="code"
              optionLabel="name"
              onChange={(e) => onGroupStateChange(e)}
              disabled={!edit_group && !create_group}
            />
          </div>
        </div>
      </Dialog>
      <Dialog
        visible={set_delete_dialog}
        className=""
        header="Delete Group"
        footer={deleteGroupDialogFooter}
        onHide={hideDeleteGroupDialog}
      >
        <div className="d-flex flex-row align-items-center">
          <div>
            <label>Are you sure you want to delete this group?</label>
          </div>
        </div>
      </Dialog>
    </div>
  )
}

export default Group
