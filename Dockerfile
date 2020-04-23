# our base image
FROM python:3.7

# set env vars
ENV FLASK_ENV development

# copy source
COPY . /usr/src/app/
# install tox

WORKDIR /usr/src/app/
RUN pip install tox


# tell the port number the container should expose
EXPOSE 5000

# run the application
#CMD ["python", "/usr/src/app/app.py"]

RUN tox -e run