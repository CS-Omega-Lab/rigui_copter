import subprocess


class CameraReader:
    def __init__(self, hdm, port):
        self.hdm = hdm
        self.sp = subprocess
        self.proc = None
        self.port = port

    def start(self):
        self.proc = self.sp.Popen(
            ['gst-launch-1.0', 'udpsrc', 'port=' + str(self.port), '!',
             'application/x-rtp, encoding-name=JPEG, payload=26', '!',
             'rtpjpegdepay', '!', 'jpegdec', '!', 'd3d11videosink'],
            shell=True, stdout=subprocess.PIPE)
        self.hdm.lg('HOST', 0, 'Запуск обработчика стрима: успешно.')
        return self
