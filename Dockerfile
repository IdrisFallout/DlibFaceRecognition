FROM idrisfallout/python-dlib:1.0
RUN mkdir -p /home/app/src
WORKDIR /home/app/src
COPY ./ /home/app/src
RUN pip install scikit-learn face-recognition opencv-contrib-python
EXPOSE 5000
ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0"]