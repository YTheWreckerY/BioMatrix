from flask import Flask, render_template, Response, jsonify
import cv2
import tensorflow as tf
import numpy as np

app = Flask(__name__)

# Load model & labels
MODEL_PATH = 'Wasteseg/Model/keras_model.h5'
LABELS_PATH = 'Wasteseg/Model/labels.txt'
model = tf.keras.models.load_model(MODEL_PATH)

with open(LABELS_PATH, 'r') as f:
    labels_list = [line.strip() for line in f.readlines()]

# Webcam
cap = cv2.VideoCapture(1)

# Label + strategy mapping
def get_label_and_strategy(classID):
    categories = {
        1: ('Cardboard-Biodegradable', 'Recycle by composting or repurposing.'),
        2: ('Glass-Solid Waste', 'Clean and place in the recycling bin for glass.'),
        3: ('Footwear-Textile waste', 'Donate or recycle through a textile recycling center.'),
        4: ('Clothes-Textile waste', 'Donate or repurpose as cleaning rags.'),
        5: ('Metal-Non-Biodegradable', 'Recycle at a metal collection facility.'),
        6: ('Paper-Biodegradable', 'Recycle in the paper recycling bin.'),
        7: ('Battery-Hazardous', 'Dispose at designated battery recycling centers.'),
        8: ('Organic Waste-Biodegradable', 'Compost to create natural fertilizer.'),
        9: ('Toothbrush-Non-Biodegradable', 'Reuse creatively or place in non-recyclable waste.'),
        10: ('Diaper/Pads-Rejected Waste', 'Wrap and place in non-recyclable waste.'),
        11: ('Mask-Household waste', 'Dispose of in household waste with proper containment.'),
        12: ('Plastic-Non-biodegradable', 'Check the type and recycle or dispose accordingly.'),
        13: ('Phone-E-waste', 'Take to an electronic recycling facility.')
    }
    return categories.get(classID, ('Unknown', 'No strategy available.'))

def preprocess_frame(frame):
    img = cv2.resize(frame, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = (img / 255.0 - 0.5) * 2  # scale to [-1,1]
    return img

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            continue

        # Prediction
        img_input = preprocess_frame(frame)
        preds = model.predict(img_input)
        classID = int(np.argmax(preds[0])) + 1
        label, _ = get_label_and_strategy(classID)

        # Overlay label
        cv2.putText(frame, label, (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 0), 2, cv2.LINE_AA)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_result')
def get_result():
    success, frame = cap.read()
    if success:
        img_input = preprocess_frame(frame)
        preds = model.predict(img_input)
        classID = int(np.argmax(preds[0])) + 1
        label, strategy = get_label_and_strategy(classID)
        return jsonify({'label': label, 'strategy': strategy})
    return jsonify({'label': 'No result', 'strategy': 'No data'})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Use host='0.0.0.0' so it works on local network too
    app.run(debug=True, threaded=True, host='0.0.0.0')
