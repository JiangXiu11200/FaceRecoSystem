# Face Recognition System

<p align="center">
  <a href="https://www.python.org/downloads/release/python-3100/">
    <img src="https://img.shields.io/badge/Python-v3.10-356d9f?logo=python" alt="Python"/>
  </a>
  <a href="https://nodejs.org/en">
    <img src="https://img.shields.io/badge/Node.js-v10.2-%235FA04E?logo=node.js" alt="nodejs"/>
  </a>
  <a href="https://www.django-rest-framework.org/">
    <img src="https://img.shields.io/badge/Django%20DRF-v3.16-%23092E20?logo=django&logoColor=django"
     alt="DjangoDRF"/>
  </a>
  <a href="https://primereact.org/">
    <img src="https://img.shields.io/badge/PrimeReact-v10.9-%2303C4E8?logo=PrimeReact" alt="primereact">
  </a>
  <a href="https://www.min.io/">
    <img src="https://img.shields.io/badge/MinIO-v7.2-C52944?logo=minio" alt="MinIO"/>
  </a>
  <a href="https://www.postgresql.org/">
    <img src="https://img.shields.io/badge/PostgreSQL-v16-%230064a5?logo=postgresql" alt="PostgreSQL"/>
  </a>

  <a href="https://nginx.org/">
    <img src="https://img.shields.io/badge/NGINX-v1.28-%23009639?logo=nginx" alt="nginx">
  </a>
  <a href="https://docs.celeryq.dev/en/stable/#">
    <img src="https://img.shields.io/badge/Celery-v5.5-%2337814A?logo=Celery&logoColor=%2337814A" alt="celery">
  </a>
  <a href="https://www.docker.com/">
  <img src="https://img.shields.io/badge/Docker-v28.3-%232496ED?style=flat&logo=docker&logoColor=docker" alt="docker">
  </a>
</p>

<p align="center">
Readme Languages: <a href="./README_en.md">English 🇺🇸</a> / <a href="./README.md">繁體中文版 🇹🇼</a>
</p>
<p align="center">
Development started, please see: <a href="./frontend/">Frontend </a> and <a href="./backend/">Backend </a>
</a>
<p align="center">
GUI User Guide: <a href="https://hackmd.io/@MV1MNu9pSWqPmTx9CRvHbA/Hy-MD0mqgg">Face Recognition System GUI 操作指南 (Hackmd.io) </a>
</a>


## 描述

本系統為一套 **人臉辨識系統**，採前後端分離架構：

前端(React) 提供即時影像串流顯示、操作介面與各項管理頁面；後端(Django) 負責帳號權限管理、人臉註冊資料、告警日誌與 API服務；人臉辨識核心，則與 [FaceRecognition](https://github.com/JiangXiu11200/FaceRecognition) 服務整合，透過 API 與 WebSocket 實現即時影像串流、臉部偵測、特徵計算等。整體系統透過 Docker 部署於本地端。


## 功能

#### 核心功能：
- 登入驗證：採用 JWT 進行身份與權限驗證，使用者依所屬群組自動分配 API 使用權限，確保資料安全與權限隔離。
- 即時影像串流：支援即時影像輸入(Webcam / IPCAM)，並提供 WebSocket 推送辨識資訊。
- 辨識告警日誌：自動記錄未經授權的人臉 ROI 影像與時間戳，並可供後續調閱。
- 活動日誌：區分為人臉辨日誌與系統日誌，前者記載成功登入的人臉 ROI 影像、時間戳與事件，後者則紀錄系統操作行為。
- 辨識參數設定：管理員可調整辨識框座標、門檻、靈敏度等系統參數，並取得當前影像即時對比。

#### 系統特性
- 前後端分離架構，具備良好的維護性與擴展性。
- 非同步任務：透過 Celery 進行週期性任務排程，清理 S3 暫存與過期的系統日誌。
- 容器化部署：以 Docker compose 多服務同時運行，未來可與 CI/CD 整合。
- API 測試： Django 透過 Unit test 進行正向、反向、邊緣、Monkey 測試，確保品質。


## 系統架構

### Use Case

本系統的用例圖依功能與關注點分為三張，以便清楚呈現不同層面的業務流程與系統互動：

#### JWT Authentication (JWTAuth) Use Case Diagram

![Image](./assets/images/UseCase_JWTAuth.jpg)

- 描述使用者操作系統前與過程中的驗證流程，包括登入與每支 API 的權限檢查。
- 目的是確保系統安全與隔離用戶權限。
- 系統透過 Refresh Token 定期更新 Access Token，保障持續存取的安全性。

#### Main Function Use Case Diagram

![Image](./assets/images/UseCase_InternalFunc.jpg)

- 描述系統內部的核心業務流程，包括人臉用戶註冊、告警/系統日誌調閱、系統用戶管理、系統參數設定等。
- 目的是呈現主要業務邏輯，清楚區分各功能間的流程與責任。

#### External Access Use Case Diagram

![Image](./assets/images/UseCase_ExternalAccess.jpg)

- 描述系統與外部服務的互動流程。
  - Face Recognition Service：提供特徵擷取與比對服務，供 User Registration 調用。
  - Alarm Logs / Activity Logs：接收外部服務觸發的事件資料。
  - System Config：更新外部服務的參數配置。
- 目的是呈現外部依賴與系統邊界，方便設計 API 介面與資料流。


### High-Level-Desgin

![Image](./assets/images/HLD.jpg)

- Client 端透過 Nginx 反向代理來存取 Web Server、App Server 與 S3 資源。
- Storage 用於存放註冊的人臉影像、告警/活動日誌的人臉影像、用戶大頭貼。
- App Server：FaceRecognition 為人臉辨識核心，透過 Uvicorn 部署 FastAPI，瀏覽器會與其透過 WebSocket 連線，實現即時串流與通訊。詳細可造訪 [FaceRecognition](https://github.com/JiangXiu11200/FaceRecognition)。
- App Server：FaceRecoSystem 為主要的控制系統，透過 Uvicorn 部署 Django，並建置 JWT 登入與驗證流程。
- Redis：Redis 作為 Celery 的訊息中介(Broker)，負責任務排程與傳遞。
- Celery：FaceRecoSystem 的排程任務程序，負責週期性清理 S3 暫存檔與資料庫已過期的系統日誌。
- Flower：Celery 的監控工具，可由內部網路存取，僅用於監控 Celery 狀態。


### Database ER Diagram

![Image](./assets/images/ERD.jpg)

資料庫部分依功能分類，如上圖所示。其中：

- UserProfile 與 UserGroup 建立多對多表：一個用戶可被指派在一個或多個用戶群組，用於設定該用戶的應用程式訪問權限。若無設定，則表示該用戶沒有任何應用程式訪問權限。
- UserGroup 與 SystemApps 建立多對多表：一個用戶群組可以有一個或多個應用程式訪問權限。
- SystemActivityLogs：存放系統活動日誌。
- FaceRecognitionActivityLogs：存放人臉辨識日誌。
- AlarmLogs：存放人臉辨識失敗時的告警日誌。
- SystemActivityLogsRetention：設定系統活動日誌保存天數。
- FaceRecognitionActivityLogsRetention：設定人臉辨識日誌的保存天數。
- DebugConfig、VideoConfig、RecognitionConfig：人臉辨識服務的系統參數。


### Swagger API

透過 Swagger API 建立 API 文件。

![Image](./assets/images/Swagger_API.png)

- **Accounts**
  - GET /api/accounts/ - Retrieve User Accounts
  - GET /api/accounts/{id}/ - Retrieve User Account
  - PUT /api/accounts/{id}/ - Update User Account
  - PATCH /api/accounts/{id}/ - Partially Update User Account
  - DELETE /api/accounts/{id}/ - Delete User Account
  - GET /api/accounts/avatars/ - Get the Presigned URL of the profile picture from MinIO S3
  - POST /api/accounts/change-password/{user_id}/ - Change User Password
  - GET /api/accounts/group/ - List User Groups
  - POST /api/accounts/group/ - Create User Group
  - GET /api/accounts/group/{id}/ - Retrieve User Group
  - PUT /api/accounts/group/{id}/ - Update User Group
  - PATCH /api/accounts/group/{id}/ - Partially Update User Group
  - DELETE /api/accounts/group/{id}/ - Delete User Group by ID
  - POST /api/accounts/register/ - Register New User Account
  - GET /api/accounts/systemapps/ - List System Applications
  - POST /api/accounts/upload-profile-picture/ - Upload Profile Picture
- **Activity Logs**
  - GET /api/activity-logs/face-recognition/ - List facial recognition activity logs and obtain MinIO S3 face image Presigned URLs
  - POST /api/activity-logs/face-recognition/ - Create a new system activity log entry
  - GET /api/activity-logs/face-recognition/{id}/ - Retrieve a specific facial recognition activity log entry
  - DELETE /api/activity-logs/face-recognition/{id}/ - Delete a facial recognition activity log entry
  - GET /api/activity-logs/face-recognition/retention/ - Retrieve facial recognition activity logs retention settings
  - PUT /api/activity-logs/face-recognition/retention/{id}/ - Update facial recognition activity logs retention settings and reschedule cleanup task
  - PATCH /api/activity-logs/face-recognition/retention/{id}/ - Update facial recognition activity logs retention settings and reschedule cleanup task
  - GET /api/activity-logs/system/ - List system activity logs
  - POST /api/activity-logs/system/ - Create a new system activity log entry
  - GET /api/activity-logs/system/{id}/ - Retrieve a specific system activity log entry
  - DELETE /api/activity-logs/system/{id}/ - Delete a system activity log entry
  - GET /api/activity-logs/system/retention/ - Retrieve system activity logs retention settings
  - PUT /api/activity-logs/system/retention/{id}/ - Update system activity logs retention settings and reschedule cleanup task
  - PATCH /api/activity-logs/system/retention/{id}/ - Update system activity logs retention settings and reschedule cleanup task
- **Alarm Logs**
  - GET /api/alarm-logs/ - List Alarm Logs
  - POST /api/alarm-logs/ - Create Alarm Log
  - GET /api/alarm-logs/{id}/ - Retrieve Alarm Log
  - DELETE /api/alarm-logs/{id}/ - Delete Alarm Log
  - PUT /api/alarm-logs/acknowledge/{id}/ - Acknowledge Alarm Log
  - PATCH /api/alarm-logs/acknowledge/{id}/ - Acknowledge Alarm Log Partially
- **Auth**
  - POST /api/auth/login/ - User Login
  - POST /api/auth/logout/ - User Logout
- **Face Recognition Config**
  - GET /api/face-recognition-config/debug/ - List Debug Configuration
  - PUT /api/face-recognition-config/debug/{id}/ - Update Debug Configuration, ID is always 1
  - PATCH /api/face-recognition-config/debug/{id}/ - Partially Update Debug Configuration, ID is always 1
  - GET /api/face-recognition-config/preview/ - Get one preview image from the camera
  - GET /api/face-recognition-config/recognition/ - List Configuration
  - GET /api/face-recognition-config/recognition/{id}/
  - PUT /api/face-recognition-config/recognition/{id}/ - Update Configuration, ID is always 1
  - PATCH /api/face-recognition-config/recognition/{id}/ - Partially Update Configuration, ID is always 1
  - GET /api/face-recognition-config/video/ - List Video Configuration
  - GET /api/face-recognition-config/video/{id}/
  - PUT /api/face-recognition-config/video/{id}/ - Update Video Configuration, ID is always 1
  - PATCH /api/face-recognition-config/video/{id}/ - Partially Update Video Configuration, ID is always 1
- **Token**
  - POST /api/token/refresh/ - Refresh Access Token
- **User Registration**
  - GET /api/user-registration/ - List Registered Users
  - POST /api/user-registration/ - Register a New User
  - GET /api/user-registration/{id}/ - Retrieve Registered User
  - PUT /api/user-registration/{id}/ - Update Registered User
  - PATCH /api/user-registration/{id}/ - Partially Update Registered User
  - DELETE /api/user-registration/{id}/ - Delete a Registered User
  - GET /api/user-registration/group/ - List User Registration Groups
  - POST /api/user-registration/group/ - Create User Registration Group
  - GET /api/user-registration/group/{id}/ - Retrieve User Registration Group
  - PUT /api/user-registration/group/{id}/ - Update User Registration Group
  - PATCH /api/user-registration/group/{id}/ - Partially Update User Registration Group
  - DELETE /api/user-registration/group/{id}/ - Delete User Registration Group


### Tests

為了確保系統穩定性與安全性，本專案建立了全面的 API 測試，包括：

- 正向測試 (Positive Test)：驗證 API 在正常輸入與預期使用情境下能正確運作。
- 反向測試 (Negative Test)：檢查異常或錯誤輸入是否被妥善處理，防止系統崩潰或資料不一致。
- 邊界測試 (Boundary Test)：驗證 API 在參數極限值或邊界條件下的行為是否正確。
- Monkey 測試 (Monkey Test)：隨機或非結構化輸入測試，模擬不可預期的操作，評估系統穩定性與容錯能力。

綜合以上測試，能有效保障系統在各種操作情境下的穩定性、安全性與可靠性。

![Image](./assets/images/tests-1.png)
![Image](./assets/images/tests-2.png)


## 安裝與部署

開始前，請先安裝 Python 3.10 版本、 uv 套件管理工具與 Docker 環境。

### Docker build

前端

```bash
DOCKER_BUILDKIT=1 docker build --no-cache -f frontend/Dockerfile -t facereco-frontend:1.0.0 .
```

後端

```bash
DOCKER_BUILDKIT=1 docker build --no-cache -f backend/Dockerfile -t facereco-backend:1.0.0 .
```

> NOTE: DOCKER_BUILDKIT=1 用來啟用 Docker 的 BuildKit 建構引擎，使 docker build 更快、更高效並支援安全的秘密管理。

### Docker compose 啟動

```bash
docker-compose up
```
