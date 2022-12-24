#!/bin/bash

apt update
apt install -y toilet figlet
toilet -f pagga -F metal RiGUI
toilet -f pagga -F metal Installing...
apt install -y libx264-dev libjpeg-dev libopencv-dev libatlas-base-dev
apt install -y libgstreamer1.0-dev \
     libgstreamer-plugins-base1.0-dev \
     libgstreamer-plugins-bad1.0-dev \
     gstreamer1.0-plugins-ugly \
     gstreamer1.0-tools \
     gstreamer1.0-gl \
     gstreamer1.0-gtk3
su -c "python3 -m pip install --upgrade --user pip" pi
su -c "python3 -m pip install --upgrade --user rich pythonping netifaces pyzbar opencv-python numpy flask pyzbar" pi
setcap cap_net_raw+ep $(readlink -f $(which python3))
git clone https://github.com/CS-Omega-Lab/rigui_copter
cd rigui_copter
apt install -y npm
npm install pm2 -g
pm2 start Startup/PlatformStartup.py
pm2 startup
env PATH="$PATH":/usr/bin /usr/local/lib/node_modules/pm2/bin/pm2 startup systemd -u pi --hp /home/pi
pm2 save
