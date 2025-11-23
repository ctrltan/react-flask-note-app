FROM --platform=linux/amd64 node:22-alpine as build
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM --platform=linux/amd64 nginx:1.25-alpine
ENV PORT=3000
COPY --from=build /usr/src/app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/templates/default.conf.template
EXPOSE 3000
CMD [ "nginx", "-g", "daemon off;" ]