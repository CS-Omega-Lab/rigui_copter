from threading import Thread
import time

from flask import Flask, Response

frame = b'1'
app = Flask(__name__)

Thread(target=lambda: app.run(host='192.168.31.200', debug=True, use_reloader=False), daemon=True, args=()).start()


def switch(inp):
    global frame
    frame = inp


def gen():
    global frame
    while True:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
