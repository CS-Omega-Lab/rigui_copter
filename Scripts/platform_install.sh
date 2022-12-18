#!/bin/bash
apt update
apt install -y toilet figlet
toilet -f mono12 -F metal RiGUI
toilet -f pagga -F metal Installing...
apt install -y libx264-dev libjpeg-dev libopencv-dev libatlas-base-dev
apt install -y libgstreamer1.0-dev \
     libgstreamer-plugins-base1.0-dev \
     libgstreamer-plugins-bad1.0-dev \
     gstreamer1.0-plugins-ugly \
     gstreamer1.0-tools \
     gstreamer1.0-gl \
     gstreamer1.0-gtk3
su -c "pip3 install --upgrade --user pip" pi
su -c "pip3 install --upgrade --user rich pythonping netifaces pyzbar opencv-python numpy flask pyzbar" pi
setcap cap_net_raw+ep $(readlink -f $(which python3))
git clone https://github.com/CS-Omega-Lab/rigui_copter
cd rigui_copter
