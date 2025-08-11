import { Button } from "primereact/button"
import { Column } from "primereact/column"
import { DataTable } from "primereact/datatable"
import React, { useEffect, useState } from "react"
import { Image } from "primereact/image"

import "./data_table.css"

function Table({
  data,
  actnioEvent,
  columns,
  actionsHeader = "",
  viewsFlag = false,
  editFlag = false,
  deleteFlag = false,
  imageFlag = false,
  tableHeight = "60vh",
}) {
  const [window_width, setWindowWidth] = useState(window.innerWidth)
  const [selectedRows, setSelectedRows] = useState([])

  useEffect(() => {
    setSelectedRows([])
  }, [data])

  useEffect(() => {
    function windowResize() {
      setWindowWidth(window.innerWidth)
    }
    window.addEventListener("resize", windowResize)
  })

  const imageBodyTemplate = (image) => {
    return (
      <div className="table-image">
        <Image
          className="table-image-layout"
          src={
            image && image.startsWith("http")
              ? image
              : "/image/roi_not_found.jpg"
          }
          alt="headshot"
          preview={true}
        />
      </div>
    )
  }

  const actionTemplate = (data) => {
    return (
      <React.Fragment>
        <div className="d-flex flex-row justify-content-center align-items-center">
          {viewsFlag ? (
            <div className="me-2">
              <Button
                icon="pi pi-ellipsis-h"
                className="p-button-info action-btn"
                onClick={() => actnioEvent({ action: "view", data })}
              />
            </div>
          ) : (
            ""
          )}
          {editFlag ? (
            <div className="me-2">
              <Button
                icon="pi pi-user-edit"
                className="p-button-info action-btn"
                onClick={() => actnioEvent({ action: "edit", data })}
              />
            </div>
          ) : (
            ""
          )}
          {deleteFlag ? (
            <div className="me-2">
              <Button
                icon="pi pi-trash"
                className="p-button-info action-btn"
                onClick={() => actnioEvent({ action: "delete", data })}
              />
            </div>
          ) : (
            ""
          )}
          {imageFlag ? (
            <div className="me-2">
              <Button
                icon="pi pi-image"
                className="p-button-info action-btn"
                onClick={() => actnioEvent({ action: "image", data })}
              />
            </div>
          ) : (
            ""
          )}
        </div>
      </React.Fragment>
    )
  }

  return (
    <DataTable
      className="w-100"
      value={data}
      selection={selectedRows}
      dataKey="id"
      paginator={true}
      rows={10}
      rowsPerPageOptions={[10, 50, 100]}
      scrollHeight={window_width > 992 ? tableHeight : "60vh"}
    >
      {columns.map((col, index) => {
        if (col.type === "boolean") {
          return (
            <Column
              className="data-column"
              key={index}
              field={col.field}
              header={col.header}
              body={(rowData) =>
                rowData[col.field] ? (
                  <i
                    className="pi pi-check-circle"
                    style={{ color: "green" }}
                  ></i>
                ) : (
                  <i
                    className="pi pi-times-circle"
                    style={{ color: "red" }}
                  ></i>
                )
              }
            />
          )
        }
        if (col.type === "image") {
          return (
            <Column
              className="image-column"
              header={col.header}
              body={(rowData) => imageBodyTemplate(rowData[col.field])}
            />
          )
        }
        if (col.type === "date") {
          return (
            <Column
              className="data-column"
              key={index}
              field={col.field}
              header={col.header}
              body={(rowData) => new Date(rowData[col.field]).toLocaleString()}
            />
          )
        }
        return (
          <Column
            className="data-column"
            key={index}
            field={col.field}
            header={col.header}
          />
        )
      })}

      {(viewsFlag || editFlag || deleteFlag || imageFlag) && (
        <Column
          className="action-btn-column"
          header={actionsHeader}
          body={actionTemplate}
          exportable={false}
        />
      )}
    </DataTable>
  )
}

export { Table }
