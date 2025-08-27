# Build the frontend
FROM node:20.11.0 as frontend


COPY ./frontend ./frontend

WORKDIR /frontend

RUN npm install -g webpack

RUN npm run build

# Serve with nginx
FROM nginx:stable-alpine

# remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

COPY --from=frontend /frontend/dist /frontend

COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3001

CMD ["nginx", "-g", "daemon off;"]
