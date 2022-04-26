import subprocess


class ManualCameraStreamer:
    def __init__(self):
        self.sp = subprocess
        self.proc = None

    def start(self):
        self.proc = self.sp.Popen([
            'gst-launch-1.0 v4l2src device=/dev/video0 ! "image/jpeg,width=800,height=600,framerate=30/1" ! '
            'rtpjpegpay ! udpsink host=192.168.31.32 port=5052'],
            shell=True, stdout=subprocess.PIPE)
        return self

