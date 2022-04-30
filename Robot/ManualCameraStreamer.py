import subprocess
import os


class ManualCameraStreamer:
    def __init__(self, rdm):
        self.rdm = rdm
        if not os.path.exists(rdm.devices['video_dev']):
            rdm.lg('ROBOT', 1, 'Устройство v4l2 на '+rdm.devices['video_dev']+' не подключено.')
        self.sp = subprocess
        self.proc = None

    def start(self):
        self.proc = self.sp.Popen([
            'gst-launch-1.0 v4l2src device=/dev/video0 ! "image/jpeg,width=800,height=600,framerate=30/1" ! '
            'rtpjpegpay ! udpsink '+self.rdm.config['general']['host']+' port=5052'],
            shell=True, stdout=subprocess.PIPE)
        return self

