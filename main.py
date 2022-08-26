import requests, json
import os


class SendMsg():
    """docstring for SendMsg"""

    def __init__(self):
        self.appID = os.environ.get('APPID')
        self.appsecret = os.environ.get('APPSECRET')
        self.access_token = self.get_access_token()
        self.opend_ids = self.get_openid()

    def get_access_token(self):
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(
            self.appID, self.appsecret)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36'}
        response = requests.get(url, headers=headers).json()
        access_token = response.get('access_token')
        return access_token

    def get_openid(self):
        next_openid = ''
        url_openid = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token={}&next_openid={}'.format(
            self.access_token,
            next_openid)
        ans = requests.get(url_openid)
        print(ans.content)
        open_ids = json.loads(ans.content)['data']['openid']
        return open_ids

    def sendmsg(self, msg):
        """
        给所有粉丝发送文本消息
        """
        url = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={}".format(self.access_token)
        print(url)
        if self.opend_ids != '':
            for open_id in self.opend_ids:
                body = {
                    "touser": open_id,
                    "msgtype": "text",
                    "text":
                        {
                            "content": msg
                        }
                }
                data = bytes(json.dumps(body, ensure_ascii=False).encode('utf-8'))
                print(data)
                response = requests.post(url, data=data)
                # 这里可根据回执code进行判定是否发送成功(也可以根据code根据错误信息)
                result = response.json()
                print(result)
        else:
            print("当前没有用户关注该公众号！")

    def sendTemplate(self, msg):
        url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(self.access_token)
        print(url)
        if self.opend_ids != '':
            for open_id in self.opend_ids:
                body = {
                    "touser": open_id,
                    "template_id": os.environ.get('TID'),
                    "url": "http://weixin.qq.com/download",
                    "topcolor": "#999999",
                    "data":
                        {
                            "content": {
                                "value": msg,
                                "color": "#666666"
                            }
                        }
                }
                data = bytes(json.dumps(body, ensure_ascii=False).encode('utf-8'))
                print(data)
                response = requests.post(url, data=data)
                # 这里可根据回执code进行判定是否发送成功(也可以根据code根据错误信息)
                result = response.json()
                print(result)
        else:
            print("当前没有用户关注该公众号！")


def get_iciba_everyday():
    icbapi = 'http://open.iciba.com/dsapi/'
    eed = requests.get(icbapi)
    bee = eed.json()  # 返回的数据
    english = bee['content']
    zh_CN = bee['note']
    str = english + '\n' + zh_CN
    return str


def get_caihongpi():
    try:
        key = os.environ.get('SERVERKEY')
        api = 'http://api.tianapi.com/caihongpi/index?key=' + key
        resp = requests.post(api)
        data = resp.json()
        print(data)
        if (data['code'] == 200):
            res = data['newslist'][0]['content']
            return res
    except Exception:
        print("【ERROR】彩虹屁请求失败")
        print(Exception)


def getWeather():
    try:
        api = 'http://t.weather.itboy.net/api/weather/city/'  # API地址，必须配合城市代码使用
        city_code = os.environ.get('CITY_CODE')  # 进入https://where.heweather.com/index.html查询你的城市代码
        tqurl = api + city_code
        response = requests.get(tqurl)
        d = response.json()  # 将数据以json形式返回，这个d就是返回的json数据
        if (d['status'] == 200):  # 当返回状态码为200，输出天气状况
            parent = d["cityInfo"]["parent"]  # 省
            city = d["cityInfo"]["city"]  # 市
            update_time = d["time"]  # 更新时间
            date = d["data"]["forecast"][0]["ymd"]  # 日期
            week = d["data"]["forecast"][0]["week"]  # 星期
            weather_type = d["data"]["forecast"][0]["type"]  # 天气
            wendu_high = d["data"]["forecast"][0]["high"]  # 最高温度
            wendu_low = d["data"]["forecast"][0]["low"]  # 最低温度
            shidu = d["data"]["shidu"]  # 湿度
            pm25 = str(d["data"]["pm25"])  # PM2.5
            pm10 = str(d["data"]["pm10"])  # PM10
            quality = d["data"]["quality"]  # 天气质量
            fx = d["data"]["forecast"][0]["fx"]  # 风向
            fl = d["data"]["forecast"][0]["fl"]  # 风力
            ganmao = d["data"]["ganmao"]  # 感冒指数
            tips = d["data"]["forecast"][0]["notice"]  # 温馨提示
            # 天气提示内容
            tdwt = "【今日份天气】\n城市：" + parent + city + \
                   "\n日期：" + date + \
                   "\n星期: " + week + \
                   "\n天气: " + weather_type + \
                   "\n温度: " + wendu_high + " / " + wendu_low + \
                   "\n湿度: " + shidu + \
                   "\n空气质量: " + quality + \
                   "\n风力风向: " + fx + fl + \
                   "\n感冒指数: " + ganmao + \
                   "\n更新时间: " + update_time + \
                   "\n✁---------------------------------------\n" + \
                   get_caihongpi()
            print(tdwt)
            return tdwt
    except Exception:
        error = '【出现错误】\n　　今日天气推送错误，请检查服务或网络状态！'
        print(error)
        print(Exception)


if __name__ == "__main__":
    data = getWeather()
    sends = SendMsg()
    sends.sendTemplate(data)
