import subprocess


class CameraReader:
    def __init__(self, hdm):
        self.hdm = hdm
        self.sp = subprocess
        self.proc = None

    def start(self):
        self.proc = self.sp.Popen(
            ['gst-launch-1.0', 'udpsrc', 'port=5060', '!',
             'application/x-rtp, encoding-name=JPEG, payload=26', '!',
             'rtpjpegdepay', '!', 'jpegdec', '!', 'd3d11videosink'],
            shell=True, stdout=subprocess.PIPE)
        self.hdm.lg('HOST', 0, 'Запуск обработчика стрима: успешно.')
        return self
