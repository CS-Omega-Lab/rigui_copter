from threading import Thread

import cv2
from flask import Flask, Response
from pyzbar import pyzbar

from Robot.Drivers.VideoReader import VideoReader


class QReader:
    def __init__(self, rdm):
        self.lgm = rdm.lgm
        self.host = rdm.local_address
        self.thread = Thread(target=self.stream, daemon=True, args=())
        self.reader = VideoReader(rdm.config['devices']['video_dev'])
        self.counter = 0
        self.decoded = None
        self.found = False
        self.app = None

    # def __init__(self):
    #     self.lgm = None
    #     self.host = 'localhost'
    #     self.thread = Thread(target=self.stream, daemon=True, args=())
    #     self.reader = VideoReader(0).start()
    #     self.counter = 0
    #     self.decoded = None
    #     self.found = False

    def stop(self):
        pass

    def start(self):
        self.thread.start()
        return self

    def decode(self, in_image):
        image = in_image
        im_height, im_width, im_channel = image.shape
        det_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        det_image = cv2.threshold(det_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        det_image = cv2.morphologyEx(det_image, cv2.MORPH_CLOSE, kernel, iterations=1)
        det_image = cv2.bitwise_not(det_image)

        decoded_objects = pyzbar.decode(det_image)
        if len(decoded_objects) >= 1:
            self.decoded = decoded_objects[0]
            self.found = True
            for decoded in decoded_objects:
                self.draw(decoded, image, im_width)
        else:
            if self.counter > 10:
                self.counter = 0
                self.found = False
            else:
                if self.found:
                    self.counter += 1
                    self.draw(self.decoded, image, im_width)
        return image

    @staticmethod
    def draw(decoded, image, im_width):
        n_points = len(decoded.polygon)
        for i in range(n_points):
            image = cv2.line(
                img=image,
                pt1=decoded.polygon[i],
                pt2=decoded.polygon[(i + 1) % n_points],
                color=(0, 255, 0),
                thickness=2)
        image = cv2.rectangle(
            img=image,
            pt1=(decoded.rect.left, decoded.rect.top),
            pt2=(decoded.rect.left + decoded.rect.width, decoded.rect.top + decoded.rect.height),
            color=(255, 0, 255),
            thickness=2
        )
        txt_size = cv2.getTextSize(
            text=str(decoded.data.decode('utf-8')),
            fontFace=cv2.FONT_HERSHEY_COMPLEX,
            fontScale=0.5,
            thickness=1
        )

        text_top = decoded.rect.top - (txt_size[0][1] * 2)
        if text_top - txt_size[0][1] < 0:
            text_top = txt_size[0][1]

        text_left = decoded.rect.left
        if text_left + txt_size[0][0] + 10 > im_width:
            text_left = im_width - txt_size[0][0] - 10

        text_right = text_left + txt_size[0][0] + 10

        text_bottom = text_top + (txt_size[0][1] * 2)

        image = cv2.rectangle(
            img=image,
            pt1=(text_left, text_top),
            pt2=(text_right, text_bottom),
            color=(255, 255, 255),
            thickness=-1
        )
        image = cv2.putText(
            img=image,
            text=decoded.data.decode('utf-8'),
            org=(text_left + 5, text_bottom - 5),
            fontFace=cv2.FONT_HERSHEY_COMPLEX,
            fontScale=0.5,
            color=(255, 0, 0),
            thickness=1,
            lineType=cv2.LINE_AA
        )
        # print("Type:", decoded.type)
        # print("Data:", decoded.data.decode('utf-8'))
        # print()

    def gen(self):
        while True:
            frame = self.reader.read()
            frame = self.decode(frame)
            ret, jpeg = cv2.imencode('.jpg', frame)
            image = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n\r\n')

    def stream(self):
        self.reader.start()
        self.app = Flask(__name__)

        @self.app.route('/')
        @self.app.route('/video_feed')
        def video_feed():
            return Response(self.gen(),
                            mimetype='multipart/x-mixed-replace; boundary=frame')

        self.app.run(host=str(self.host), debug=False)

