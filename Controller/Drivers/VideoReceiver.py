import subprocess as sp
from time import gmtime, strftime


class VideoReceiver:
    def __init__(self, hdm):
        self.hdm = hdm

    def start(self):
        port = str('port=' + self.hdm.config["network"]["platform_video_port"])
        date = str(strftime("%Y-%m-%d_%H-%M-%S", gmtime()))
        print(date)
        cmd = ['gst-launch-1.0', '-e', 'udpsrc', port, '!',
               'application/x-rtp,clock-rate=90000,encoding-name=JPEG,payload=26', '!', 'rtpjpegdepay', '!', 'jpegdec',
               '!', 'tee', 'name=t', '!', 'queue', '!', 'd3d11videosink', 'async=false', 't.', '!', 'queue', '!',
               'x264enc', 'pass=5', 'quantizer=25', 'speed-preset=6', '!', 'mp4mux', '!', 'filesink',
               'location="Video/platform_rec_' + date + '.mp4"', 'async=false']
        sp.Popen(
            cmd,
            shell=True, stdout=sp.PIPE)
        self.hdm.lg('CNTR', 0, 'Запуск обработчика стрима: успешно.')
        return self
