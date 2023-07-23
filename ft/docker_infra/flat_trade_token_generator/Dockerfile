
ARG base_python_latest_tag
FROM base_python:${base_python_latest_tag}

RUN npm --global --loglevel info install crypto 
RUN npm --global --loglevel info install sha256
RUN npm --global --loglevel info install eslint-config-standard-with-typescript  @typescript-eslint/eslint-plugin@^5.50.0 eslint@^8.0.1 eslint-plugin-import@^2.25.2 eslint-plugin-n@^15.0.0 eslint-plugin-promise@^6.0.0 typescript
#RUN npm --global config set user root 
RUN npm --global --loglevel info install express 
RUN npm --global --loglevel info install request 
RUN npm --global --loglevel info install totp-generator 
RUN npm --global --loglevel info install zombie 
RUN npm --global --loglevel info install puppeteer 
RUN apt-get install -y libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2
RUN npm --global --loglevel info install websocket 
RUN npm --global --loglevel info install pine 
ENV NODE_PATH=/usr/local/lib/node_modules/
RUN npm --global --loglevel info install pino 
RUN npm --global --loglevel info install pino-pretty 
RUN npm --global --loglevel info install moment 
RUN pip3 install asyncio
RUN pip3 install telegram
#RUN pip3 install 
#RUN pip3 install 
