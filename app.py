from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('6YO4sIvoxjcNIozLuKU7IBtnyofmyAfvY8+xiQqE0RWoCkakIXRkJt2PT4WF7zrgq7JDM7rnogrj3y90TGX+cvlnAVROQ2SPEx8Qx+qI0ASUYaY9rJyYkM38en7/XiSDYx8sBRX5NplreR9Q8i7ypAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('00a21f206bd05842de9fd9efb50a9af6')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
