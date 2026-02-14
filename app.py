from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64


app = Flask(__name__)

# Load Haar Cascade files from OpenCV
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

smile_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_smile.xml'
)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/go_index')
def go_index():
    return render_template('index.html')

@app.route('/go_stressed')
def go_stressed():
    return render_template('stressed.html')

@app.route('/journal')
def go_journal():
    return render_template('journal.html')

@app.route('/go_happy')
def go_happy():
    return render_template('happy.html')


@app.route('/breathe')
def go_breathe():
    return render_template('breathe.html')


@app.route('/dumb')
def go_dumb():
    return render_template('dumb.html')

@app.route('/game')
def go_game():
    return render_template('game.html')


@app.route('/last')
def go_last():
    return render_template('last.html')

@app.route('/detect', methods=['POST'])
def detect():
    try:
        data = request.get_json()

        if not data or 'image' not in data:
            return jsonify({"mood": "No image received"})

        image_data = data['image']

        # Remove header (data:image/jpeg;base64,)
        encoded_data = image_data.split(',')[1]

        # Convert base64 to numpy array
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({"mood": "Image decode failed"})

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) == 0:
            return jsonify({"mood": "No Face Detected 😶"})

        mood = "Stressed 😣"   # Default mood

        for (x, y, w, h) in faces:
            face_gray = gray[y:y+h, x:x+w]

            smiles = smile_cascade.detectMultiScale(
                face_gray,
                scaleFactor=1.7,
                minNeighbors=20
            )

            if len(smiles) > 0:
                mood = "Happy 😊"

        return jsonify({"mood": mood})

    except Exception as e:
        print("Error:", e)
        return jsonify({"mood": "Server Error"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
