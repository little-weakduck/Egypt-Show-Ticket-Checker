import requests
import schedule
import time
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 想要蹲票的时间 按照YYYY-MM-DD的形式写
dates = ["2025-01-01", "2025-02-01"]

# Bark发送通知的设备号，通过Bark来实时提醒手机 下载链接在下面
# https://apps.apple.com/app/id1403753865
device_codes = ["", ""]

# mpsessid也不知道是什么，反正是用来鉴权的 可以用whistle开启https代理抓下下面的url地址 在headers里面
mpsessid = ""

# 需要的票的数量，小于这个数量的票，认为他没票
ticket_num = 2

url = "https://shmres-zwc.shanghaimuseum.net/vendor/reserve/getReservePeriodListByDate.xhtml"
ticket_headers = {
    "Host": "shmres-zwc.shanghaimuseum.net",
    "Connection": "keep-alive",
    "mpsessid": mpsessid,
    "content-type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 18_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.56(0x1800382d) NetType/WIFI Language/zh_CN",
    "Referer": "https://servicewechat.com/wxa0a7f2b3bf67edcc/143/page-frame.html"
}

def check_tickets():
    logging.info("开始检查票务情况...")
    arr = []
    for date in dates:
        data = {
            "stadiumId": "69002",
            "reservedate": date,
            "type": "union",
            "isDedicated": "undefiend",
            "stadiumHomeCode": "stadiumPudongValue",
            "tempExhibitionCode": "69002_1",
        }

        try:
            response = requests.post(url, headers=ticket_headers, data=data)
            response.raise_for_status()
            response_data = response.json()

            if response_data.get("errcode") == "0000" and response_data.get("success"):
                reserve_period_list = response_data.get("data", {}).get("reservePeriodList", [])
                for period in reserve_period_list:
                    if period.get("avaiable") == "Y" and period.get("availableNum") >= ticket_num:
                        arr.append({
                            "date": date,
                            "starttime": period.get("starttime"),
                            "endtime": period.get("endtime"),
                            "availableNum": period.get("availableNum")
                        })
        except requests.RequestException as e:
            logging.error(f"请求失败: {e}")
            continue

    if arr:
        send_ticket_notifications(arr)
    else:
        current_minute = time.localtime().tm_min
        if current_minute in [0, 30]:
            notify_no_tickets()
        else:
            logging.info('没有票了')

def send_ticket_notifications(tickets):
    alert_url = "https://api.day.app/"
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    for ticket in tickets:
        alert_data = {
            "title": "埃及展览有票了",
            "body": f"日期: {ticket['date']}, 时间: {ticket['starttime']} - {ticket['endtime']}, 剩余票数量: {ticket['availableNum']}",
            "level": "critical",
            "volume": 10,
            "group": "EgyptShowTicket" + ticket['date']
        }
        for device_code in device_codes:
            try:
                response = requests.post(alert_url + device_code, headers=headers, json=alert_data)
                response.raise_for_status()
                logging.info(f"通知发送成功: {alert_data}")
            except requests.RequestException as e:
                logging.error(f"通知发送失败: {e}")

def notify_no_tickets():
    alert_url = "https://api.day.app/"
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    alert_data = {
        "title": "埃及展览",
        "body": "目前没有票",
        "level": "passive",
        "volume": 10,
        "group": "EgyptShowTicket"
    }
    for device_code in device_codes:
        try:
            response = requests.post(alert_url + device_code, headers=headers, json=alert_data)
            response.raise_for_status()
            logging.info("静音通知发送成功")
        except requests.RequestException as e:
            logging.error(f"静音通知发送失败: {e}")
            

# 利用schedule库做没分钟一次的轮询，当然你也可以自己修改
schedule.every(1).minutes.do(check_tickets)

while True:
    schedule.run_pending()
    time.sleep(1)