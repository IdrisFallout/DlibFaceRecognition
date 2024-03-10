FROM python:3.8.0-alpine3.10
RUN mkdir -p /home/app/src
WORKDIR /home/app/src
COPY ./ /home/app/src
RUN pip3 install scikit-learn
RUN pip3 install face-recognition
RUN pip3 install opencv-contrib-python
RUN pip3 install Flask
EXPOSE 5000
ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0"]