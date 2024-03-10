FROM python:3.10.12-alpine3.18
RUN mkdir -p /home/app/src
WORKDIR /home/app/src
COPY ./ /home/app/src
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0"]