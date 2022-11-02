# Rigui legacy
> Кирилл, лезь в грёбанного робота!

# Установка:

## На роботе, RPI: 

```shell
sudo apt-get install libx264-dev libjpeg-dev
sudo apt-get install libgstreamer1.0-dev \
     libgstreamer-plugins-base1.0-dev \
     libgstreamer-plugins-bad1.0-dev \
     gstreamer1.0-plugins-ugly \
     gstreamer1.0-tools \
     gstreamer1.0-gl \
     gstreamer1.0-gtk3
pip3 install --upgrade --user pip
pip3 install rich pythonping netifaces pyzbar
git clone https://github.com/Hexerpowers/rigui_legacy
cd rigui_legacy
sudo python3 install.py
```

## На компьютере, Windows: 
Сначала устанавливаем:
```shell
https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe
https://gstreamer.freedesktop.org/data/pkg/windows/1.20.4/msvc/gstreamer-1.0-msvc-x86_64-1.20.4.msi
https://gstreamer.freedesktop.org/data/pkg/windows/1.20.4/msvc/gstreamer-1.0-devel-msvc-x86_64-1.20.4.msi
```
Затем модули Python:
```shell
pip3 install --upgrade --user pip
pip3 install rich pythonping netifaces inputs keyboard py_win_keyboard_layout
```

## Для запуска системы управления на компьютере используем
```shell
START.bat
```
Перетягиваем окно на левую сторону экрана и нажимаем Enter

## Для проверки состояния процесса на роботе
```shell
$/ rigui-check
```

## Для принудительной перезагрузки
```shell
$/ rigui-restart
```