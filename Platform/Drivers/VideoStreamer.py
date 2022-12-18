import subprocess as sp
import os


class VideoStreamer:
    def __init__(self, rdm):
        self.rdm = rdm
        self.lgm = rdm.lgm
        self.allowed = True
        self.client = [
            rdm.remote_address,
            rdm.config['network']['platform_video_port']
        ]
        if not os.path.exists(rdm.devices['platform_video_dev']):
            self.lgm.dlg('PLTF', 1, 'Устройство v4l2 на ' + rdm.devices['platform_video_dev'] + ' не подключено.')
            self.rdm.update_init_data(0, 2)
            self.allowed = False
        else:
            self.lgm.dlg('PLTF', 0, 'Устройство v4l2 на ' + rdm.devices['platform_video_dev'] + ' подключено.')
            self.rdm.update_init_data(0, 1)

        self.process = None

    def start(self):
        device = self.rdm.devices['platform_video_dev']
        if self.allowed:
            self.process = sp.Popen([
                'gst-launch-1.0 v4l2src device=' + device +
                ' ! "image/jpeg,width=1280, height=720,framerate=30/1" ! rtpjpegpay ! udpsink host=' +
                self.client[0] + ' port=' + str(self.client[1])],
                shell=True, stdout=sp.PIPE)
        return self

    def stop(self):
        self.process.terminate()
