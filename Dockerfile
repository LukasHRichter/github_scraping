FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./data_analysis ./data_analysis
COPY ./data_handling ./data_handling
COPY ./requirements.txt ./requirements.txt

#CMD [ "python", "./data_analysis/aggregate.py" ]