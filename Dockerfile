FROM python:3.8-slim-buster
RUN apt update
RUN apt install git-all -y
WORKDIR /app
COPY . /app/rm-sec-toolkit
RUN pip3 install -r /app/rm-sec-toolkit/requirements.txt
RUN pip3 install /app/rm-sec-toolkit
RUN rm-sec-toolkit -v
ENTRYPOINT ["rm-sec-toolkit"]
CMD ["-i"]