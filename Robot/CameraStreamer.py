import subprocess
import os


class CameraStreamer:
    def __init__(self, rdm, dev_id):
        self.rdm = rdm
        self.dev_id = dev_id
        self.allowed = True
        if not os.path.exists(rdm.devices['video_dev_' + str(dev_id)]):
            rdm.lg('ROBOT', 1, 'Устройство v4l2 на ' + rdm.devices['video_dev_' + str(dev_id)] + ' не подключено.')
            self.rdm.update_init_data(dev_id, 2)
            self.allowed = False
        else:
            self.rdm.update_init_data(dev_id, 1)
        self.sp = subprocess
        self.proc = None

    def start(self):
        if self.allowed:
            self.proc = self.sp.Popen([
                'gst-launch-1.0 v4l2src device=/dev/video0 ! "image/jpeg,width=800,height=600,framerate=30/1" ! '
                'rtpjpegpay ! udpsink host=' + self.rdm.config['network'][
                    'client'] + ' port=' + str(self.rdm.config['network']['video_port_0'])],
                shell=True, stdout=subprocess.PIPE)
        return self
