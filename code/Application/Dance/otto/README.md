# Micropython OTTO Ninjia Robot

基于 Micropython 和 ESP8266/ESP32 系列开发板开发的 OTTO Humanoid 和 OTTO Ninjia 机器人程序

## 目录结构
* /ottolib：基于精简后的 OTTO 官方的 Micropython 程序库封装的模块，封装了 OTTO 的核心运动逻辑，精简掉了声音、LED点阵屏等相关附加逻辑。
* /rklib: 自己封装的模块，里面有 LED、舵机、网络相关类
* /tests：各种简单的测试程序，主要供 main.py 引用
* /webroot：托管H5页面相关资源文件的目录
* /webserver：开源的Micropython Web服务器库
* /boot.py：Micropython 的启动程序
* /main.py：Micropython 的主程序
* /OTTOServer.py：基于开源的Micropython Web服务器库搭建的OTTO机器人Web服务器，里面指定了网站根目录，实现了一组控制机器人的HTTP接口。