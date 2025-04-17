import { Button } from "primereact/button"
import { InputText } from "primereact/inputtext"
import { Toolbar } from "primereact/toolbar"
import React, { useEffect, useState } from "react"
import { MultiSelect } from "primereact/multiselect"
import { Table } from "../data_table/data_table"

import "./users.css"

function Users() {
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

    const leftContents = (
        <React.Fragment>
            <div className="toolbar-left">
                <div className="field-group">
                    <InputText className="p-inputtext" placeholder="Search for groups.." />
                </div>
                <div>
                    <div className="field-group">
                        <MultiSelect className="w-100" placeholder="Select Group" options={[]} onChange={() => {}} optionLabel="name" />
                    </div>
                </div>
                <div className="field-group">
                    <Button icon="pi pi-search" className="func-btn" label="Search" />
                </div>
            </div>
        </React.Fragment>
    )

    return (
        <div className="d-flex flex-column">
            <Toolbar className="toolbar-layout" left={leftContents} />
            <Table data={table_data} columns={columns} actnioEvent={setActionEvent} editFlag={true} deleteFlag={true} viewsFlag={false} />
        </div>
    )
}

export default Users
