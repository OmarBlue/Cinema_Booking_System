FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./

# Install mysqlclient dependencies
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential

# Install Python dependencies
RUN pip install -r requirements.txt

# Install Pillow
RUN pip install Pillow

# Install Request
RUN pip install requests

# Install dateutil
RUN pip install python-dateutil

COPY . .

# Set environment variables for MySQL connection
ENV MYSQL_HOST localhost
ENV MYSQL_PORT 3306
ENV MYSQL_DATABASE DESD
ENV MYSQL_USER root
ENV MYSQL_PASSWORD password

# Install mysqlclient
RUN pip install mysqlclient

EXPOSE 8000     

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
