from threading import Thread
import cv2


class StreamReader:
    def __init__(self):
        self.frame = None
        self.grabbed = None
        self.stream = None
        self.thread = Thread(target=self.update, daemon=True, args=())
        self.started = False
        self.thread.start()

    def instance(self):
        return self

    def start(self):
        self.started = True
        self.stream = cv2.VideoCapture(0)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        (self.grabbed, self.frame) = self.stream.read()
        return self

    def stop(self):
        self.stream.release()

    def update(self):
        while True:
            if self.started:
                (grabbed, frame) = self.stream.read()
                if grabbed:
                    self.grabbed, self.frame = grabbed, frame

    def read(self):
        return self.frame

    def __exit__(self):
        self.stream.release()
