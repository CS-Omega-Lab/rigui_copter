## EXPLORA
> Велосипеды это конечно круто, но если не работает чужой велосипед, на душе как-то приятнее...

## Для использования необходимы библиотеки: 

TODO: добавить gstreamer
```shell
sudo apt update
sudo apt upgrade
sudo apt install libopencv-dev
sudo pip3 install opencv-python
sudo pip3 install rich
sudo pip3 install keyboard
```
## Для установки используем (обязательно!):
```shell
git clone https://github.com/Hexerpowers/bass
sudo python3 install.py
```

## Для запуска используем
```shell
explora-cli -start
```

## Для проверки состояния
```shell
explora-cli -check
```

## Если запускается сервер с винды, то просто запустить файл
```shell
python3 HostBootstrap.py
```