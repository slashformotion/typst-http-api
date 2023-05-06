FROM python:3.11-buster
RUN apt update
RUN apt install cargo -y
RUN pip install --upgrade pip
# RUN groupadd -r typstuser && useradd -rm -g typstuser typstuser
# USER typstuser
WORKDIR /app
COPY ./typst-http-api/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./typst-http-api .
# equivalent to 'from hello import app'
RUN chmod +x gunicorn.sh
CMD ["sh", "gunicorn.sh"]
#Expose port 8000 of the container to the outside
EXPOSE 8000
