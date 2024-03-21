安装okx的库

创建一个.env的环境文件

OKX_API_KEY=api key

OKX_SECRET_KEY=密钥

OKX_PASSPHRASE=okx创建api的密码

TELEGRAM_BOT_TOKEN=tg 机器人api

TELEGRAM_CHAT_ID=tg id

运行 python3 ok.py

后台运行
 nohup /usr/bin/python3 /root/ok.py > /root/ok.log 2>&1 &
   我放在root下运行，放在其他文件下自行修改，设置了log分区、满了后自动覆盖
