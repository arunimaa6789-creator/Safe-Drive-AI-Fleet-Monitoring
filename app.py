from flask import Flask, render_template, Response, jsonify
import cv2

app = Flask(__name__)

camera = cv2.VideoCapture(0)

def generate_frames():

    while True:
        success, frame = camera.read()

        if not success:
            break

        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/status")
def status():

    driver_status = "ACTIVE"

    try:
        with open("driver_status.txt", "r") as file:
            driver_status = file.read().strip()
    except:
        driver_status = "ACTIVE"

    fatigue_level = "LOW"
    alert = "No Alerts"
    fleet_risk = "LOW"

    if driver_status == "DROWSY":
        fatigue_level = "HIGH"
        alert = "Fatigue Detected!"
        fleet_risk = "HIGH"

    return jsonify({
        "driver_status": driver_status,
        "fatigue_level": fatigue_level,
        "alert": alert,
        "fleet_risk": fleet_risk
    })
if __name__ == "__main__":
 app.run(host="127.0.0.1", port=5000, debug=True)