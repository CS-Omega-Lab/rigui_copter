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
setcap cap_net_raw+ep "$(readlink -f "$(which python3)")"
su -c "git clone https://github.com/CS-Omega-Lab/rigui_copter" pi
su -c "cd rigui_copter" pi || exit
apt install -y npm
sudo npm install pm2 -g
su -c "pm2 startup" pi
sudo env PATH="$PATH":/usr/bin /usr/local/lib/node_modules/pm2/bin/pm2 startup systemd -u pi --hp /home/pi
su -c "pm2 ls" pi
su -c "pm2 start Startup/PlatformStartup.py" pi
su -c "pm2 save" pi
