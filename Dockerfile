# pull official base image
FROM python:3.7.3-alpine

# set work directory
WORKDIR /libraryapp

# set environment variables
ENV PYTHONUNBUFFERED 1


RUN apk update \
  && apk add --virtual build-dependencies gcc python3-dev musl-dev \
  && apk add jpeg-dev zlib-dev libjpeg \
  && pip install Pillow \
  && apk del build-dependencies

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /libraryapp/
RUN pip install -r requirements.txt

# copy project
COPY . /libraryapp/

#set environment vars to be used
ENV AUTHOR="Philip"

#port from the container to expose to host
EXPOSE 8000

#Tell image what to do when it starts as a container
CMD /libraryapp/start.sh