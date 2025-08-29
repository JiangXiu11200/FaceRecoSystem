# Build the frontend
FROM node:20.11.0 as frontend


WORKDIR /app

COPY frontend/ ./

RUN npm install

RUN npm run build

# Serve with nginx
FROM nginx:stable-alpine

# remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

COPY --from=frontend /app/dist /frontend

COPY nginx/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 3001

CMD ["nginx", "-g", "daemon off;"]
