FROM node:20-alpine

WORKDIR /app
EXPOSE 3000

RUN apk add --no-cache bash

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy project files
COPY . .

# Build for production
RUN npm run build

# Install serve to serve static files
# RUN npm install -g serve

# Serve the built application
CMD ["npm", "run", "dev"] 