# Dockerfile for the frontend
# Use an official Node runtime as the base image
FROM node AS build

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json for using npm
COPY package*.json ./

# Install the required npm packages
RUN npm install

# Copy the current directory contents into the container at /app
COPY . .

# Set the argument for the build-time environment variable
ARG REACT_APP_BACKEND_URL

# Set the build-time environment variable that will be used by React
ENV REACT_APP_BACKEND_URL=$REACT_APP_BACKEND_URL

# Build the React app
RUN npm run build

# Use nginx to serve the React app
FROM nginx:alpine

# Copy the build app to the nginx container
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Run nginx
CMD ["nginx", "-g", "daemon off;"]

