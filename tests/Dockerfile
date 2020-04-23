# our base image
FROM python:3.7
ENV FLASK_ENV development

# install Python modules needed by the Python app
# COPY requirements.txt /usr/src/app/

# copy files required for the app to run
COPY . /usr/src/app/
#RUN rm -rf .tox

# install tox

WORKDIR /usr/src/app/
#RUN pip install tox


# tell the port number the container should expose
EXPOSE 5000

# run the application
#CMD ["python", "/usr/src/app/app.py"]
#RUN tox -r -e build
#RUN pip install
RUN pip install -r requirements.txt
RUN python setup.py install
#RUN ls -lah
#RUN pip install dist/*.gz
#RUN source .tox/py37/bin/activate
CMD defang-server --host=0.0.0.0