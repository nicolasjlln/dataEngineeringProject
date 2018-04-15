FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install python3
RUN apt-get install python3-pip

RUN pip3 install Flask


RUN apt-get install virtualenv
RUN virtualenv venv
RUN . venv/bin/activate