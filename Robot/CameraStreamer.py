import subprocess as sp
import os


class CameraStreamer:
    def __init__(self, rdm, client, lgm):
        self.rdm = rdm
        self.lgm = lgm
        self.allowed = True
        self.client = client
        if not os.path.exists(rdm.devices['video_dev']):
            self.lgm.dlg('ROBOT', 1, 'Устройство v4l2 на ' + rdm.devices['video_dev'] + ' не подключено.')
            self.rdm.update_init_data(0, 2)
            self.allowed = False
        else:
            self.lgm.dlg('ROBOT', 0, 'Устройство v4l2 на ' + rdm.devices['video_dev'] + ' подключено.')
            self.rdm.update_init_data(0, 1)

    def start(self):
        device = self.rdm.devices['video_dev']
        if self.allowed:
            sp.Popen([
                'gst-launch-1.0 v4l2src device=' + device +
                ' ! "image/jpeg,width=800,height=600,framerate=30/1" ! rtpjpegpay ! udpsink host=' +
                self.client['address'] + ' port=' + str(self.client['port'])],
                shell=True, stdout=sp.PIPE)
        return self
