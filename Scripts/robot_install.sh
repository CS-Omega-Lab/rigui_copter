#!/bin/bash
apt-get install libx264-dev libjpeg-dev libopencv-dev libatlas-base-dev
apt-get install libgstreamer1.0-dev \
     libgstreamer-plugins-base1.0-dev \
     libgstreamer-plugins-bad1.0-dev \
     gstreamer1.0-plugins-ugly \
     gstreamer1.0-tools \
     gstreamer1.0-gl \
     gstreamer1.0-gtk3
apt install toilet figlet
toilet -f small Installing...
toilet -f mono12 -F metal RiGUI
pip3 install --upgrade --user pip
pip3 install --upgrade rich pythonping netifaces pyzbar opencv-python numpy flask pyzbar
setcap cap_net_raw+ep $(readlink -f $(which python))
git clone https://github.com/CS-Omega-Lab/rigui_copter
cd rigui_copter