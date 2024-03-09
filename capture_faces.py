from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Directory to save captured images
TRAINING_IMAGES_DIR = 'train_img'


# Route to capture images
@app.route('/')
def capture_images():
    return render_template('capture.html')


# Route to save captured images
@app.route('/save_images', methods=['POST'])
def save_images():
    label = request.form.get('admission')
    if not label:
        return jsonify({'message': 'Label not provided.'}), 400

    images = request.files.getlist('images')
    if len(images) != 20:
        return jsonify({'message': 'Exactly 20 images are required.'}), 400

    label_dir = os.path.join(TRAINING_IMAGES_DIR, label)
    if not os.path.exists(label_dir):
        os.makedirs(label_dir)

    for i, image in enumerate(images):
        image.save(os.path.join(label_dir, f'image_{i + 1}.jpg'))

    return jsonify({'message': 'Images saved successfully.'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5060, debug=True)
