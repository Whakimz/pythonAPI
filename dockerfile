FROM python:3.8.1

RUN apt-get update
RUN apt-get install gcc
ADD /odbc/docker/odbcinst.ini /etc/odbcinst.ini
RUN apt-get install -y tdsodbc unixodbc-dev
RUN apt install unixodbc -y
RUN apt-get clean -y
RUN rm -rf /etc/localtime
RUN ln -s /usr/share/zoneinfo/Asia/Bangkok /etc/localtime

COPY . /app

EXPOSE 5001
ENV PORT 5001


WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt



ENTRYPOINT ["python"]
CMD ["app.py"]
