FROM python:3.11-buster
RUN apt update
RUN apt install cargo -y
WORKDIR /app
COPY ./typst-http-api/requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./typst-http-api .
ENTRYPOINT ["python3"]
CMD ["app.py"]

 