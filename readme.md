# Rigui Copter
> Сергей, лезь в грёбанного робота!

# Установка:

## На роботе, RPI: 

```shell
sudo Scripts/robot_install.sh
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
pip3 install rich pythonping netifaces inputs keyboard py_win_keyboard_layout flask opencv-python pyzbar
```

## Для запуска системы управления на компьютере используем
```shell
host_start.bat
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