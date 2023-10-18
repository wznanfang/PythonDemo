import json
from datetime import datetime

import requests

username = '不逆'
formatted_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# 获取天气预报信息
def get_weather():
    # 这里使用了一个国家气象局的天气API，可以根据实际情况替换为自己的API接口
    url = 'http://t.weather.sojson.com/api/weather/city/101270101'
    response = requests.get(url)
    # print(response.text)
    weather = json.loads(response.text)
    # 解析服务器返回的数据，具体可参考weather.json文件
    cityInfo = weather['cityInfo']
    city = cityInfo['city']
    # print("城市:", city)
    time = weather['time']
    # print("时间：", time)
    data = weather['data']
    shidu = data['shidu']
    # print("湿度：", shidu)
    quality = data['quality']
    # print("空气质量:", quality)
    wendu = data['wendu']
    # print("温度:", wendu)
    pm25 = data['pm25']
    # print("PM2.5:", pm25)
    pm10 = data['pm10']
    # print("PM10:", pm10)
    ganmao = data['ganmao']
    # print("感冒指数:", ganmao)
    forecast = data['forecast'][0]
    week = forecast['week']
    # print("星期:", week)
    type = forecast['type']
    # print("天气:", type)
    high = forecast['high']
    # print("最高温度:", high)
    low = forecast['low']
    # print("最低温度:", low)
    sunrise = forecast['sunrise']
    # print("日出时间:", sunrise)
    sunset = forecast['sunset']
    # print("日落时间:", sunset)
    aqi = forecast['aqi']
    # print("空气指数:", aqi)
    fx = forecast['fx']
    # print("风向：", fx)
    fl = forecast['fl']
    # print("风速:", fl)
    type = forecast['type']
    # print("天气:", type)
    notice = forecast['notice']
    # print("温馨提示：", notice)

    # 将解析好的数据组装成想要的格式做为函数的返回值
    result = "今日天气预报\n" \
             + formatted_time + " " + week + " " + city + "\n" \
             + type + " " + fx + " " + fl + " " + low[-3:] + " ~ " + high[-3:] + "\n" \
             + "当前温度：" + str(wendu) + "℃\n" \
             + "污染指数：" + "PM2.5(" + str(pm25) + ") - PM10(" + str(pm10) + ") " + "\n" \
             + "空气指数：" + str(aqi) + "\n" \
             + "空气质量：" + str(quality) + "\n" \
             + "当前湿度：" + shidu + "\n" \
             + "温馨提示：" + notice

    print(result)
    return result


# 调用微信发送消息的接口，将天气预报信息发送到微信上
def auto_send():
    try:
        # 调用get_weather函数
        GW = get_weather()
        # 填入你朋友的微信昵称，注意这里不是备注，也不是微信帐号
        # friends = itchat.search_friends(username)
        # friend = friends[0]['UserName']
        # # # 发送微信消息
        # itchat.send(GW, friend)
    except Exception as e:
        print("消息发送异常：", e)


if __name__ == '__main__':
    # todo 登录微信 暂时登录有问题，扫码后执行程序报错
    # itchat.auto_login(hotReload=True)
    # 调用函数进行消息发送
    auto_send()
