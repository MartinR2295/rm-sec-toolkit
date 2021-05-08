FROM python:3.8-slim-buster
RUN apt update
RUN apt install git-all -y
RUN pip3 install rm-sec-toolkit