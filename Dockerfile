FROM python:3.8.0-alpine3.10
RUN mkdir -p /home/app/src
WORKDIR /home/app/src
COPY ./ /home/app/src
RUN pip3 install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0"]