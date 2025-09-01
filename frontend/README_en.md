# Face Recognition System (Frontend)

Readme Languages: <a href="./README_en.md">English 🇺🇸</a> / <a href="./README.md">繁體中文版 🇹🇼</a>


## Development Environment Setup

Before starting, please install npm v10.2

#### Set Environment Variables

In development mode, modify the `.env` file as follows:
```
REACT_APP_DEV_BYPASS_AUTH=true
NODE_ENV=development
```
- `NODE_ENV = development`: Enables Webpack development mode, including proxy support for easier local testing.
- `REACT_APP_DEV_BYPASS_AUTH = true`: Skips JWT authentication during development, allowing direct access to all pages via URL, equivalent to having full page permissions.

> Note: This configuration is for development purposes only. Do not enable it in production.

#### Install and Start

Install dependencies:

Install dependencies:

```bash
npm install
```

Build the frontend code using Webpack:

```bash
npm run build
```

Start the frontend web server:

```bash
npm run start
```

## Project Directory Structure

```
xiu@jiangchengxiudeMacBook-Air frontend % tree -L 1
.
├── Dockerfile
├── README.md
├── dist  # Output files after Webpack build, can be deployed to server
├── node_modules  # Installed npm dependencies
├── package-lock.json  # Locks dependency versions for consistent installations across environments
├── package.json  # Project dependencies and npm script definitions
├── src  # Main source code folder
│   ├── api  # Encapsulated API request methods
│   ├── app.css
│   ├── app.js  # Entry point and core initialization
│   ├── components  # Reusable UI components
│   ├── containers  # Page container components, used for subpages
│   ├── contexts
│   │   └── token_provider.js  # Handles Access Token refresh and auto-logout on expiration
│   ├── hooks
│   ├── index.css  # Global/shared CSS
│   ├── index.js  # Main entry point and app bootstrap
│   ├── pages  # Main entry point for each app page
│   ├── routes
│   │   └── private_route.js  # Route configuration, including token validation
│   └── utils  # Shared utilities
├── static  # Static assets
├── template  # HTML templates
└── webpack.config.js  # Webpack configuration (build rules and plugins)
```

## NPM Scripts

```json
{
  "name": "facereco-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    ...
  },
  "scripts": {
    "start": "webpack-dev-server --config webpack.config.js",  // Start development server
    "build": "webpack --config webpack.config.js",  // Build frontend code
    "format": "prettier --write \"src/**/*.{js,jsx,ts,tsx,css,md,json}\" ",  // Auto-format code and styles
    "format:check": "prettier --check \"src/**/*.{js,jsx,ts,tsx,css,md,json}\" "  // Check code and styles against Prettier rules
  },
  ...
}
```
