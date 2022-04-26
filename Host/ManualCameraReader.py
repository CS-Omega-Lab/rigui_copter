import subprocess


class ManualCameraReader:
    def __init__(self, srs):
        self.srs = srs
        self.sp = subprocess
        self.proc = None

    def start(self):
        self.proc = self.sp.Popen(
            ['gst-launch-1.0', 'udpsrc', 'port=5052', '!', 'application/x-rtp, encoding-name=JPEG, payload=26', '!',
             'rtpjpegdepay', '!', 'jpegdec', '!', 'd3d11videosink'],
            shell=True, stdout=subprocess.PIPE)
        self.srs.lg('HOST', 0, 'Запуск обработчика стрима: успешно.')
        return self
