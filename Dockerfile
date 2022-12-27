FROM python:3.10

# Create app directory
WORKDIR /app

# Install app dependencies
#COPY src/requirements.txt ./

#RUN pip install -r requirements.txt
RUN pip install backtrader
RUN pip install matplotlib
RUN pip install panda

RUN pip install yfinance
RUN pip install wheel
RUN pip install ta-lib    

# Bundle app source
COPY src /app

EXPOSE 8080
CMD [ "python", "main.py" ]