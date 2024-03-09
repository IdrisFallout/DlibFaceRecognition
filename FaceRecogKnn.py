import cv2
import time
import pickle
import face_recognition
import numpy as np
from face_recognition.face_recognition_cli import image_files_in_folder
from Streamer import streamer  # Assuming you have a Streamer module
from flask import Flask, Response

app = Flask(__name__)

# Set the desired frames per second
fps = 24
frame_delay = 1 / fps

# Set the desired window size
window_width = 800
window_height = 600


def predict(img_path, knn_clf=None, model_path=None, threshold=0.6):
    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either through knn_clf or model_path")
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)
    img = img_path
    face_box = face_recognition.face_locations(img)
    if len(face_box) == 0:
        return []
    faces_encodings = face_recognition.face_encodings(img, known_face_locations=face_box)
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=2)
    matches = [closest_distances[0][i][0] <= threshold for i in range(len(face_box))]
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in
            zip(knn_clf.predict(faces_encodings), face_box, matches)]


def generate_frames():
    while True:
        start_time = time.time()
        frame = np.asarray(bytearray(streamer.get_feed()), dtype="uint8")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        frame = cv2.resize(frame, (window_width, window_height))
        frame = cv2.flip(frame, 1)
        frame_copy = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        frame_copy = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGB)
        predictions = predict(frame_copy, model_path="classifier/trained_knn_model.clf")
        font = cv2.FONT_HERSHEY_DUPLEX
        for name, (top, right, bottom, left) in predictions:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255), 2)
            cv2.putText(frame, name, (left - 10, top - 6), font, 0.8, (255, 255, 255), 1)

        _, jpeg = cv2.imencode('.jpg', frame)
        frame_bytes = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        end_time = time.time()
        processing_time = end_time - start_time
        if processing_time < frame_delay:
            time.sleep(frame_delay - processing_time)


@app.route('/feed')
def feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True, port=5050)
