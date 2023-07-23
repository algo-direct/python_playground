FROM node:20.1.0-bullseye

# One of the simplest things you can do to improve performance is to set NODE_ENV to production.
#ENV NODE_ENV=production 


WORKDIR /app

#COPY ["package.json", "package-lock.json*", "./"]

#RUN npm install --production

#COPY . .

#CMD ["node", "server.js"]

RUN apt-get update

RUN apt-get install -y build-essential cmake git openssh-server gdb pkg-config valgrind systemd-coredump

