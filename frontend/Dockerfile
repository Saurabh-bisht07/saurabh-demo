FROM node:20-alpine

WORKDIR /usr/src/app

COPY package.json package-lock.json* ./. 
RUN npm install --silent || true

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]