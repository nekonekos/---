#说明：本代码为主程序，其他库需要导入
#代码中的邮箱，密码，API密钥，私钥等不方便透露，如要编译，请自行注册平台并购买服务取得密钥
#文件夹中的points.txt,log.txt分别为积分文件和日志文件。SOS.wav和chat.wav为上一次SOS录音/聊天录音
from mpython import *

import network

my_wifi = wifi()

my_wifi.connectWiFi("你的WiFi名称", "你的WiFi密码")

import ntptime

from machine import RTC

def RTCdate(flag):
   rtc = RTC()
   dt = rtc.datetime()
   date_str = "{}年{}月{}日".format(dt[0], dt[1], dt[2])
   time_str = "{}时:{}分:{}秒".format(dt[4], dt[5], dt[6])
   if flag == 0:
       return date_str
   else:
       return time_str

def write_data_to_file(_path, _data, _sep):
    f = open(_path, 'a')
    f.write(_data + _sep)
    f.close()

IsSOS = None

LastMSG = None

import json

import urequests

from umail import *

import time

import framebuf

import font.dvsm_21

import audio

import music

def get_list_from_file(_path, _sep):
    f = open(_path, 'r')
    result = f.read().split(_sep)
    f.close()
    return result

points = None

import font.digiface_21

def init_text_file(_path):
    f = open(_path, 'w')
    f.close()

hwpage = None

import math

def get_seni_weather(_url, _location):
    _url = _url + "&location=" + _location.replace(" ", "%20")
    response = urequests.get(_url)
    json = response.json()
    response.close()
    return json

image_picture = Image()

def display_font(_font, _str, _x, _y, _wrap, _z=0):
    _start = _x
    for _c in _str:
        _d = _font.get_ch(_c)
        if _wrap and _x > 128 - _d[2]: _x = _start; _y += _d[1]
        if _c == '1' and _z > 0: oled.fill_rect(_x, _y, _d[2], _d[1], 0)
        oled.blit(framebuf.FrameBuffer(bytearray(_d[0]), _d[2], _d[1],
        framebuf.MONO_HLSB), (_x+int(_d[2]/_z)) if _c=='1' and _z>0 else _x, _y)
        _x += _d[2]

my_wifi = wifi()

myUI = UI(oled)
ntptime.settime(8, "time.windows.com")
write_data_to_file('log.txt', str(RTCdate(0)) + str(str(RTCdate(1)) + str(str(':') + str('WLAN Connected!'))), '\r\n')
write_data_to_file('log.txt', str(RTCdate(0)) + str(str(RTCdate(1)) + str(str(':') + str('SOS Status=0'))), '\r\n')
IsSOS = 0
LastMSG = '无'
w1 = get_seni_weather("https://api.seniverse.com/v3/weather/now.json?key=心知天气API密钥", "wuhan")
w2 = get_seni_weather("https://api.seniverse.com/v3/weather/daily.json?key=心知天气API密钥", "wuhan")
oled.fill(0)
oled.blit(image_picture.load('face/System/Accept_2.pbm', 0), 0, 0)
oled.DispChar(str('WLAN连接成功'), 0, 18, 1)
oled.DispChar(str('正在发送初始化信息...'), 0, 35, 1)
oled.show()
send_email('发送用邮箱','smtp密钥','接收者(老师)邮箱',2,'学生 艾马仕 的设备初始化成功!','邮件来自学生设备')
time.sleep(0.2)
oled.fill(0)
while True:
    oled.DispChar(str('^SOS                   FUNC^'), 0, 0, 1)
    display_font(font.dvsm_21, RTCdate(1), 0, 16, False)
    oled.DispChar(str(str(str(RTCdate(0)) + str(str('周') + str(time.localtime()[6]+1))) + str(str(' ') + str(''))), 0, 35, 1)
    oled.DispChar(str(str(w1["results"][0]["location"]["name"]) + str(str(' 今:') + str(str(w1["results"][0]["now"]["text"]) + str(str(' 明:') + str(w2["results"][0]["daily"][1]["text_day"]))))), 0, 48, 1)
    if button_a.is_pressed():
        time.sleep(1)
        if button_a.is_pressed():
            oled.fill(0)
            send_email('发送用邮箱','smtp密钥','接收者(老师)邮箱',2,str('[严重警告]学生艾马仕') + str('遇到了危险'),str('学生设备于') + str(str(RTCdate(0)) + str(str(RTCdate(1)) + str('发起了紧急呼叫，请根据Wifi AP信号进行搜索'))))
            write_data_to_file('log.txt', str(RTCdate(0)) + str(str(RTCdate(1)) + str(str(':') + str('Student SOS Pressed!Message sended.'))), '\r\n')
            oled.DispChar(str('<返回(5s)'), 0, 0, 1)
            IsSOS = 1
            oled.blit(image_picture.load('face/System/Alert.pbm', 0), 0, 0)
            oled.DispChar(str('已呼叫老师，日志已记录'), 0, 37, 1)
            oled.DispChar(str('请注意保护好自己'), 0, 55, 1)
            oled.show()
            rgb.fill((int(255), int(0), int(0)))
            rgb.write()
            time.sleep_ms(1)
            oled.DispChar(str('已开始录音'), 65, 0, 1)
            oled.show()
            audio.recorder_init(i2c)
            audio.record('SOS.wav', 2)
            audio.recorder_deinit()
            rgb.fill((int(51), int(255), int(51)))
            rgb.write()
            time.sleep_ms(1)
            oled.DispChar(str('已结束录音'), 65, 0, 1)
            oled.show()
            xunfei_params = {"APPID":'讯飞APPID', "APISecret":'讯飞APISecret', "APIKey":'讯飞APIKey'}
            _rsp = urequests.post("http://119.23.66.134:8085/xunfei_iat", files={"file":('SOS.wav', "audio/wav")}, params=xunfei_params)
            try:
                xunfei_iat_result = _rsp.json()
            except:
                xunfei_iat_result = {"text":""}
            my_wifi.enable_APWiFi('学生 艾马仕 的设备', 'x5yafyu4', channel=11)
            time.sleep(1)
            rgb.fill( (0, 0, 0) )
            rgb.write()
            time.sleep_ms(1)
            send_email('发送用邮箱','smtp密钥','接收者(老师)邮箱',2,str('[信息]学生艾马仕') + str('的设备已录音'),str(RTCdate(0)) + str(str(RTCdate(1)) + str(str(':') + str((xunfei_iat_result["text"])))))
            write_data_to_file('log.txt', str(RTCdate(0)) + str(str(RTCdate(1)) + str(str(':StudentSOSRecord:') + str((xunfei_iat_result["text"])))), '\r\n')
            oled.fill(0)
            oled.show()
    if button_b.is_pressed():
        if IsSOS == 1:
            send_email('发送用邮箱','smtp密钥','接收者(老师)邮箱',2,str('[警告]学生艾马仕') + str('已开启设备鸣叫'),str('学生设备于') + str(str(RTCdate(0)) + str(str(RTCdate(1)) + str(str('启用了设备鸣叫功能') + str(str('\n') + str('设备鸣叫功能为标准SOS(三短三长三短)，可用于辨别方位'))))))
            write_data_to_file('log.txt', str(RTCdate(0)) + str(str(RTCdate(1)) + str(str(':') + str('Student Device Sound Beep Pressed!Message sended.'))), '\r\n')
            while True:
                rgb.fill((int(255), int(255), int(255)))
                rgb.write()
                time.sleep_ms(1)
                music.play('A5:1')
                rgb.fill( (0, 0, 0) )
                rgb.write()
                time.sleep_ms(1)
                time.sleep(0.2)
                rgb.fill((int(255), int(255), int(255)))
                rgb.write()
                time.sleep_ms(1)
                music.play('A5:1')
                rgb.fill( (0, 0, 0) )
                rgb.write()
                time.sleep_ms(1)
                time.sleep(0.2)
                rgb.fill((int(255), int(255), int(255)))
                rgb.write()
                time.sleep_ms(1)
                music.play('A5:1')
                rgb.fill( (0, 0, 0) )
                rgb.write()
                time.sleep_ms(1)
                time.sleep(0.2)
                rgb.fill((int(255), int(255), int(255)))
                rgb.write()
                time.sleep_ms(1)
                music.play('A5:4')
                rgb.fill( (0, 0, 0) )
                rgb.write()
                time.sleep_ms(1)
                time.sleep(0.2)
                rgb.fill((int(255), int(255), int(255)))
                rgb.write()
                time.sleep_ms(1)
                music.play('A5:4')
                rgb.fill( (0, 0, 0) )
                rgb.write()
                time.sleep_ms(1)
                time.sleep(0.2)
                rgb.fill((int(255), int(255), int(255)))
                rgb.write()
                time.sleep_ms(1)
                music.play('A5:4')
                rgb.fill( (0, 0, 0) )
                rgb.write()
                time.sleep_ms(1)
                time.sleep(0.2)
                rgb.fill((int(255), int(255), int(255)))
                rgb.write()
                time.sleep_ms(1)
                music.play('A5:1')
                rgb.fill( (0, 0, 0) )
                rgb.write()
                time.sleep_ms(1)
                time.sleep(0.2)
                rgb.fill((int(255), int(255), int(255)))
                rgb.write()
                time.sleep_ms(1)
                music.play('A5:1')
                rgb.fill( (0, 0, 0) )
                rgb.write()
                time.sleep_ms(1)
                time.sleep(0.2)
                rgb.fill((int(255), int(255), int(255)))
                rgb.write()
                time.sleep_ms(1)
                music.play('A5:1')
                rgb.fill( (0, 0, 0) )
                rgb.write()
                time.sleep_ms(1)
                time.sleep(1)
        else:
            while True:
                oled.fill(0)
                oled.DispChar(str('P:信息'), 3, 3, 1)
                oled.DispChar(str('Y:天气'), 3, 25, 1)
                oled.DispChar(str('T:积分'), 3, 46, 1)
                oled.DispChar(str('H:作业'), 67, 3, 1)
                oled.DispChar(str('O:设置'), 67, 25, 1)
                oled.DispChar(str('N:返回桌面'), 67, 46, 1)
                oled.show()
                if touchpad_p.is_pressed():
                    oled.RoundRect(0, 0, 64, 20, 2, 1)
                    oled.show()
                    time.sleep(0.3)
                    oled.fill(0)
                    oled.show()
                    while True:
                        oled.fill(0)
                        # message.app
                        oled.blit(image_picture.load('face/System/Play.pbm', 0), 58, 0)
                        oled.DispChar(str('按下T键录音 按下N键退出'), 0, 16, 1)
                        oled.DispChar(str(str('上条信息:') + str(LastMSG)), 0, 32, 1, True)
                        oled.show()
                        if touchpad_t.is_pressed():
                            oled.fill(0)
                            audio.recorder_init(i2c)
                            rgb.fill((int(255), int(0), int(0)))
                            rgb.write()
                            time.sleep_ms(1)
                            oled.DispChar(str('录音中...'), 0, 0, 1)
                            audio.record('chat.wav', 2)
                            oled.DispChar(str('录音结束'), 0, 0, 1)
                            rgb.fill((int(51), int(255), int(51)))
                            rgb.write()
                            time.sleep_ms(1)
                            xunfei_params = {"APPID":'讯飞APPID', "APISecret":'讯飞APISecret', "APIKey":'讯飞APIKey'}
                            _rsp = urequests.post("http://119.23.66.134:8085/xunfei_iat", files={"file":('chat.wav', "audio/wav")}, params=xunfei_params)
                            try:
                                xunfei_iat_result = _rsp.json()
                            except:
                                xunfei_iat_result = {"text":""}
                            oled.DispChar(str(str('识别结果:') + str((xunfei_iat_result["text"]))), 0, 16, 1, True)
                            oled.DispChar(str('T:发送     N:取消'), 0, 48, 1)
                            oled.show()
                            while True:
                                if touchpad_t.is_pressed():
                                    oled.fill(0)
                                    oled.blit(image_picture.load('face/System/Busy_1.pbm', 0), 57, 10)
                                    oled.DispChar(str('发送中...'), 42, 30, 1)
                                    oled.show()
                                    send_email('发送用邮箱','smtp密钥','接收者(老师)邮箱',2,str('[信息]学生艾马仕') + str('发送了信息'),str(RTCdate(0)) + str(str(RTCdate(1)) + str(str(':') + str((xunfei_iat_result["text"])))))
                                    write_data_to_file('log.txt', str(RTCdate(0)) + str(str(RTCdate(1)) + str(str(':Student Sended:') + str((xunfei_iat_result["text"])))), '\r\n')
                                    oled.fill(0)
                                    oled.blit(image_picture.load('face/System/Accept_1.pbm', 0), 57, 10)
                                    oled.DispChar(str('发送成功'), 42, 30, 1)
                                    LastMSG = xunfei_iat_result["text"]
                                    rgb.fill( (0, 0, 0) )
                                    rgb.write()
                                    time.sleep_ms(1)
                                    oled.show()
                                    break
                                if touchpad_n.is_pressed():
                                    time.sleep(0.2)
                                    rgb.fill( (0, 0, 0) )
                                    rgb.write()
                                    time.sleep_ms(1)
                                    oled.fill(0)
                                    oled.show()
                                    break
                        if touchpad_n.is_pressed():
                            rgb.fill( (0, 0, 0) )
                            rgb.write()
                            time.sleep_ms(1)
                            oled.fill(0)
                            oled.show()
                            time.sleep(0.3)
                            break
                # weather.app
                if touchpad_y.is_pressed():
                    oled.RoundRect(0, 23, 64, 20, 2, 1)
                    oled.show()
                    time.sleep(0.3)
                    oled.fill(0)
                    oled.show()
                    while True:
                        oled.DispChar(str('<返回(N)'), 0, 0, 1)
                        oled.DispChar(str(str('武汉 今天:') + str(str(w1["results"][0]["now"]["text"]) + str(str('  气温:') + str(w1["results"][0]["now"]["temperature"])))), 0, 16, 1)
                        oled.DispChar(str('明天  后天  大后天'), 25, 32, 1)
                        oled.DispChar(str('天气'), 0, 48, 1)
                        oled.DispChar(str(w2["results"][0]["daily"][1]["text_day"]), 25, 48, 1)
                        oled.DispChar(str(w2["results"][0]["daily"][2]["text_day"]), 52, 48, 1)
                        oled.DispChar(str(w2["results"][0]["daily"][0]["text_day"]), 82, 82, 1)
                        oled.DispChar(str(str(w2["results"][0]["daily"][0]["wind_direction"]) + str(w2["results"][0]["daily"][0]["wind_speed"])), 64, 0, 1)
                        oled.hline(0, 32, 128, 1)
                        oled.hline(0, 48, 128, 1)
                        oled.hline(0, 63, 128, 1)
                        oled.vline(0, 32, 32, 1)
                        oled.vline(24, 32, 32, 1)
                        oled.vline(50, 32, 32, 1)
                        oled.vline(81, 32, 32, 1)
                        oled.vline(127, 32, 32, 1)
                        oled.show()
                        if touchpad_n.is_pressed():
                            rgb.fill( (0, 0, 0) )
                            rgb.write()
                            time.sleep_ms(1)
                            oled.fill(0)
                            oled.show()
                            time.sleep(0.3)
                            break
                if touchpad_t.is_pressed():
                    oled.RoundRect(0, 46, 64, 18, 2, 1)
                    oled.show()
                    time.sleep(0.3)
                    oled.fill(0)
                    oled.show()
                    points = get_list_from_file('points.txt', '\r\n')[0]
                    while True:
                        oled.DispChar(str('<返回(N)'), 0, 0, 1)
                        oled.DispChar(str('积分:'), 28, 24, 1)
                        display_font(font.digiface_21, points, 56, 25, False, 2)
                        oled.show()
                        if 1 == 0:
                            oled.fill(0)
                            oled.blit(image_picture.load('face/System/Accept_1.pbm', 0), 0, 0)
                            oled.DispChar(str('积分+1'), 25, 0, 1)
                            oled.show()
                            points = points + 1
                            time.sleep(0.5)
                            oled.fill(0)
                            oled.show()
                        if int(points) >= 0 and int(points) < 100:
                            oled.DispChar(str('加油，争取突破两位数积分！'), 0, 48, 1)
                            oled.show()
                        if int(points) >= 100 and int(points) < 500:
                            oled.DispChar(str('哇！已经有许多积分了！'), 0, 48, 1)
                            oled.show()
                        if int(points) >= 500 and int(points) < 1000:
                            oled.DispChar(str('太多积分了！秀儿，你太秀了'), 0, 48, 1)
                            oled.show()
                        if touchpad_n.is_pressed():
                            init_text_file('points.txt')
                            write_data_to_file('points.txt', points, '\r\n')
                            rgb.fill( (0, 0, 0) )
                            rgb.write()
                            time.sleep_ms(1)
                            oled.fill(0)
                            oled.show()
                            time.sleep(0.3)
                            break
                # hw.app
                if touchpad_h.is_pressed():
                    oled.RoundRect(65, 0, 64, 20, 2, 1)
                    oled.show()
                    time.sleep(0.3)
                    hwpage = 0
                    oled.fill(0)
                    oled.show()
                    while True:
                        oled.fill(0)
                        oled.DispChar(str('<返回(N)下页:Y上页:P'), 0, 0, 1)
                        if hwpage == 0:
                            oled.DispChar(str('语文'), 1, 16, 1)
                            oled.DispChar(str('数学'), 43, 16, 1)
                            oled.DispChar(str('英语'), 85, 16, 1)
                            oled.DispChar(str('1.练字'), 1, 32, 1)
                            oled.DispChar(str('2.作文'), 1, 48, 1)
                            oled.DispChar(str('1.试卷'), 43, 32, 1)
                            oled.DispChar(str('2.课本'), 43, 48, 1)
                            oled.DispChar(str('1.抄写'), 85, 32, 1)
                            oled.DispChar(str('2.默写'), 85, 48, 1)
                            oled.RoundRect(0, 16, 42, 48, 2, 1)
                            oled.RoundRect(42, 16, 42, 48, 2, 1)
                            oled.RoundRect(84, 16, 42, 48, 2, 1)
                            oled.show()
                        if hwpage == 1:
                            oled.DispChar(str('地生'), 1, 16, 1)
                            oled.DispChar(str('道法'), 43, 16, 1)
                            oled.DispChar(str('历史'), 85, 16, 1)
                            oled.RoundRect(0, 16, 42, 48, 2, 1)
                            oled.RoundRect(42, 16, 42, 48, 2, 1)
                            oled.RoundRect(84, 16, 42, 48, 2, 1)
                            oled.show()
                        if touchpad_p.is_pressed():
                            hwpage = 0
                        if touchpad_y.is_pressed():
                            hwpage = 1
                        if touchpad_n.is_pressed():
                            rgb.fill( (0, 0, 0) )
                            rgb.write()
                            time.sleep_ms(1)
                            oled.fill(0)
                            oled.show()
                            time.sleep(0.3)
                            break
                if touchpad_o.is_pressed():
                    oled.RoundRect(65, 23, 64, 20, 2, 1)
                    oled.show()
                    time.sleep(0.3)
                    oled.fill(0)
                    oled.show()
                    while True:
                        oled.fill(0)
                        oled.DispChar(str('P:WLAN'), 3, 3, 1)
                        oled.DispChar(str('Y:BLE'), 3, 25, 1)
                        oled.DispChar(str('T:硬件'), 3, 46, 1)
                        oled.DispChar(str('H:系统更新'), 67, 3, 1)
                        oled.DispChar(str('O:关于'), 67, 25, 1)
                        oled.DispChar(str('N:返回'), 67, 46, 1)
                        oled.show()
                        if touchpad_p.is_pressed():
                            oled.RoundRect(0, 0, 64, 20, 2, 1)
                            oled.show()
                            time.sleep(0.3)
                            oled.fill(0)
                            oled.show()
                            while True:
                                oled.fill(0)
                                oled.DispChar(str('<返回(N)'), 0, 0, 1)
                                oled.DispChar(str('WLAN----------AMS'), 0, 16, 1)
                                oled.DispChar(str('L__已连接'), 0, 32, 1)
                                oled.DispChar(str(str('ip:') + str(my_wifi.sta.ifconfig()[0])), 0, 48, 1)
                                oled.show()
                                if touchpad_n.is_pressed():
                                    rgb.fill( (0, 0, 0) )
                                    rgb.write()
                                    time.sleep_ms(1)
                                    oled.fill(0)
                                    oled.show()
                                    time.sleep(0.3)
                                    break
                        if touchpad_y.is_pressed():
                            oled.RoundRect(0, 23, 64, 20, 2, 1)
                            oled.show()
                            time.sleep(0.3)
                            oled.fill(0)
                            oled.show()
                            while True:
                                oled.fill(0)
                                oled.DispChar(str('<返回(N)'), 0, 0, 1)
                                oled.DispChar(str('BLE-未连接'), 0, 16, 1)
                                oled.show()
                                if touchpad_n.is_pressed():
                                    rgb.fill( (0, 0, 0) )
                                    rgb.write()
                                    time.sleep_ms(1)
                                    oled.fill(0)
                                    oled.show()
                                    time.sleep(0.3)
                                    break
                        if touchpad_t.is_pressed():
                            oled.RoundRect(0, 46, 64, 20, 2, 1)
                            oled.show()
                            time.sleep(0.3)
                            oled.fill(0)
                            oled.show()
                            while True:
                                oled.fill(0)
                                oled.DispChar(str('<返回(N)'), 0, 0, 1)
                                oled.DispChar(str(str('三轴传感:') + str(str('X:') + str(str((round(accelerometer.get_x()))) + str(str('Y:') + str(str((round(accelerometer.get_y()))) + str(str('Z:') + str((round(accelerometer.get_z()))))))))), 0, 16, 1)
                                oled.DispChar(str(str('环境光:') + str(light.read())), 0, 32, 1)
                                oled.DispChar(str(str('指南针:') + str(magnetic.get_heading())), 0, 48, 1)
                                oled.show()
                                if touchpad_n.is_pressed():
                                    rgb.fill( (0, 0, 0) )
                                    rgb.write()
                                    time.sleep_ms(1)
                                    oled.fill(0)
                                    oled.show()
                                    time.sleep(0.3)
                                    break
                        if touchpad_h.is_pressed():
                            oled.RoundRect(64, 0, 64, 20, 2, 1)
                            oled.show()
                            time.sleep(0.3)
                            oled.fill(0)
                            oled.show()
                            while True:
                                oled.fill(0)
                                oled.DispChar(str('<返回(N)'), 0, 0, 1)
                                oled.blit(image_picture.load('face/System/Accept_1.pbm', 0), 52, 16)
                                oled.DispChar(str('您的系统为最新版本!'), 3, 34, 1, True)
                                oled.show()
                                if touchpad_n.is_pressed():
                                    rgb.fill( (0, 0, 0) )
                                    rgb.write()
                                    time.sleep_ms(1)
                                    oled.fill(0)
                                    oled.show()
                                    time.sleep(0.3)
                                    break
                        if touchpad_o.is_pressed():
                            oled.RoundRect(64, 23, 64, 20, 2, 1)
                            oled.show()
                            time.sleep(0.3)
                            oled.fill(0)
                            oled.show()
                            while True:
                                oled.fill(0)
                                oled.DispChar(str('<返回(N)'), 31, 0, 1)
                                oled.fill_rect(0, 0, 31, 31, 1)
                                myUI.qr_code(str('艾OS For Mpython 1.41') + str(str('\n') + str('版权所有，侵权必究')), 1, 1, scale=1)
                                oled.DispChar(str('艾OS Mpython 1.41'), 0, 32, 1)
                                oled.DispChar(str('版权所有，侵权必究'), 0, 48, 1)
                                oled.show()
                                if touchpad_n.is_pressed():
                                    rgb.fill( (0, 0, 0) )
                                    rgb.write()
                                    time.sleep_ms(1)
                                    oled.fill(0)
                                    oled.show()
                                    time.sleep(0.3)
                                    break
                        if touchpad_n.is_pressed():
                            oled.RoundRect(65, 46, 64, 18, 2, 1)
                            oled.show()
                            time.sleep(0.3)
                            rgb.fill( (0, 0, 0) )
                            rgb.write()
                            time.sleep_ms(1)
                            oled.fill(0)
                            oled.show()
                            break
    oled.show()
