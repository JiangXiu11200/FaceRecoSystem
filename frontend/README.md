# Face Recognition System (Frontend)

Readme Languages: <a href="./README_en.md">English 🇺🇸</a> / <a href="./README.md">繁體中文版 🇹🇼</a>

## 開發環境安裝

開始前，請先安裝 npm v10.2

#### 設定環境變數

在開發模式下，請修改 `.env` 檔案：

```
REACT_APP_DEV_BYPASS_AUTH=true
NODE_ENV=development
```
- `NODE_ENV = development`：啟用 Webpack 的開發模式，包含自動代理功能，方便本地測試。
- `REACT_APP_DEV_BYPASS_AUTH = True`：開發期間可略過 JWT 驗證，允許直接透過 URL 存取所有頁面，相當於擁有完整頁面權限。

> 注意：此設定僅用於開發環境，請勿在生產環境中啟用。

#### 安裝與啟動

安裝相依項

```bash
npm install
```

透過 Webpack 將前端程式碼打包

```bash
npm run build
```

啟動前端 Web Server

```bash
npm run start
```

## 專案目錄結構說明

```bash
xiu@jiangchengxiudeMacBook-Air frontend % tree -L 1
.
├── Dockerfile
├── README.md
├── dist  # Webpack 打包後的產出檔案，可直接部署至伺服器。
├── node_modules  # npm 安裝的套件依賴資料夾
├── package-lock.json  # 鎖定套件版本，確保不同環境安裝一致性
├── package.json  # 專案套件依賴與 npm 腳本定義
├── src  # 前端主要程式碼資料夾
│   ├── api  # 封裝各應用程式 API 請求方法
│   ├── app.css
│   ├── app.js  # 前端入口與核心初始化程式
│   ├── components  # 最小可重複使用的 UI 元件
│   ├── containers  # 頁面容器元件，本專案用於存放子頁面
│   ├── contexts
│   │   └── token_provider.js  # Access Token 刷新與過期自動登出機制
│   ├── hooks
│   ├── index.css  # 定義專案共用元件 css
│   ├── index.js  # 前端入口與核心初始化程式
│   ├── pages  # 每個 App 頁面主要中面入口
│   ├── routes
│   │   └── private_route.js  # 路由配置，包含 Token 驗證
│   └── utils  # 頁面共用工具
├── static  # 靜態資源
├── template  # HTML 模板
└── webpack.config.js  # Webpack 設定檔，定義打包規則與 Plugin 等配置
```

## NPM Script

```json
{
  "name": "facereco-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    ...
  },
  "scripts": {
    "start": "webpack-dev-server --config webpack.config.js",  // 啟動開發伺服器
    "build": "webpack --config webpack.config.js",  // 程式碼打包
    "format": "prettier --write \"src/**/*.{js,jsx,ts,tsx,css,md,json}\" ",  // 自動格式化程式碼與樣式檔案
    "format:check": "prettier --check \"src/**/*.{js,jsx,ts,tsx,css,md,json}\" "  // 檢查程式碼與樣式檔案是否符合 Prettier 格式規範
  },
  ...
}

```
