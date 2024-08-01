import os
import json
import paramiko
import requests


# 从环境变量中获取 Telegram Bot Token 和 Chat ID
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# 从环境变量中读取 ACCOUNTS_JSON
accounts_json = os.getenv('ACCOUNTS')
accounts = json.loads(accounts_json)

# 尝试通过SSH连接的函数
def ssh_connect(host, username, password):
    transport = None
    try:
        transport = paramiko.Transport((host, 22))
        transport.connect(username=username, password=password)
        ssh_status = "SSH连接成功"
        print(f"SSH连接成功。")
        message = f'Serv00 SSH自动登录:账号 {username} SSH连接成功！'
        send_telegram_message(message)
    except Exception as e:
        ssh_status = f"SSH连接失败，错误信息: {e}"
        print(f"SSH连接失败: {e}")
        message = f'Serv00 SSH自动登录:账号 {username} SSH连接失败，错误信息: {e}'
        send_telegram_message(message)
    finally:
        if transport is not None:
            transport.close()


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }
    headers = {
        'Content-Type': 'application/json'
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            print(f"发送消息到Telegram失败: {response.text}")
    except Exception as e:
        print(f"发送消息到Telegram时出错: {e}")




# 循环执行任务
for account in accounts:
    ssh_connect(account['host'], account['username'], account['password'])
