import subprocess as sp


class CameraReader:
    def __init__(self, hdm):
        self.hdm = hdm

    def start(self):
        port = str('port=' + self.hdm.config["network"]["platform_video_port"])
        sp.Popen(
            ['gst-launch-1.0', 'udpsrc', port, '!',
             'application/x-rtp,encoding-name=JPEG,payload=26', '!',
             'rtpjpegdepay', '!', 'jpegdec', '!', 'd3d11videosink'],
            shell=True, stdout=sp.PIPE)
        self.hdm.lg('CNTR', 0, 'Запуск обработчика стрима: успешно.')
        return self
