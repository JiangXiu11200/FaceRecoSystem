import React from "react"
import ReactDOM from "react-dom/client"
import "./index.css"

import App from "./containers/app"

import "primereact/resources/primereact.min.css"
import "primereact/resources/themes/lara-light-indigo/theme.css"
import "bootstrap/dist/css/bootstrap.min.css"
import "primeicons/primeicons.css"

const root = ReactDOM.createRoot(document.getElementById("app"))
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
// ReactDOM.render(<App />, document.getElementById("app"))
