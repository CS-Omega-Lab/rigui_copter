from threading import Thread
import cv2


class VideoReader:
    def __init__(self, source):
        self.thread = Thread(target=self.update, daemon=True, args=())
        self.stream = None
        self.source = source
        self.grabbed = False
        self.frame = cv2.imread('assets/test_qr.jpg')
        self.stream = None

    def start(self):
        self.stream = cv2.VideoCapture(self.source)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        self.thread.start()
        print("StreamReader started")
        return self

    def stop(self):
        print("closing_stream")
        self.stream.release()

    def update(self):
        while True:
            (grabbed, frame) = self.stream.read()
            if grabbed:
                self.grabbed, self.frame = grabbed, frame

    def read(self):
        return self.frame.copy()

    def __del__(self):
        self.stream.release()
