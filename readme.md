# Rigui Copter
> Сергей, лезь в грёбанного робота!

# Установка:

## На роботе, RPI: 

```shell
curl -s https://raw.githubusercontent.com/CS-Omega-Lab/rigui_coter/master/Scripts/platform_install.sh | sudo bash -s
```

## На компьютере, Windows: 
Сначала скачиваем и устанавливаем:
```shell
https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe
https://gstreamer.freedesktop.org/data/pkg/windows/1.20.4/msvc/gstreamer-1.0-msvc-x86_64-1.20.4.msi
https://gstreamer.freedesktop.org/data/pkg/windows/1.20.4/msvc/gstreamer-1.0-devel-msvc-x86_64-1.20.4.msi
```
Затем:
```shell
git clone https://github.com/CS-Omega-Lab/rigui_copter
cd rigui_copter
./Scripts/controller_install.bat
```

## Для запуска системы управления на компьютере используем
```shell
./Scripts/controller_start.bat
```
Перетягиваем окно на левую сторону экрана и нажимаем Enter.
