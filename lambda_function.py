import json
import urllib.request
import re
import os
import qrcode
from PIL import Image
import cv2
 
from datetime import datetime, timezone
 
def lambda_handler(event, context):
    url = "https://api.line.me/v2/bot/message/reply"
    method = "POST"
    headers = {
        'Authorization': 'Bearer ' + os.environ['CHANNEL_ACCESS_TOKEN'],
        'Content-Type': 'application/json'
    }
    message_dist = json.loads(event["body"])
    print("message_dist", message_dist)

    #UserIDを取得
    user_id = message_dist["events"][0]["source"]["userId"]
    
    # 友達登録時
    if message_dist["events"][0]["type"] == "follow":
        json_open = open('json/Age.json', 'r')

    elif message_dist["events"][0]["type"] == "postback":
        postback = message_dist["events"][0]["postback"]["data"] 
        postback_action = postback.split("&")[0].split("=")[1]
        # DB保存用
        # postback_value = postback.split("&")[1].split("=")[1]
        if postback_action == "romance":
            json_open = open('json/Major.json', 'r')
        if postback_action == "major":
            json_open = open('json/Club.json', 'r')
        if postback_action == "club":
            json_open = open('json/Work.json', 'r')
        if postback_action == "work":
            json_open = open('json/Height.json', 'r')
        if postback_action == "height":
            json_open = open('json/Style.json', 'r')
        if postback_action == "style":
            json_open = open('json/Age.json', 'r')
        if postback_action == "age":
            json_open = open('json/Opinion.json', 'r')
        if postback_action == "opinion":
            json_open = open('json/Emotion.json', 'r')
        if postback_action == "emotion":
            # QRコードを生成しクエリパラメータとしてuser_idを与える、一旦正田氏のqrをそのまま利用する。
            # qr = qrcode.make('https://comingout.tokyo/1806'+ '/?user_id='+ user_id)
            json_open = open('json/Aicode.json', 'r')
    
    else:
        json_open = open('json/error.json', 'r')
    
    # #ユーザーの画像送信をキャッチ
    # if message_dist["events"][0]["type"] == "message":
    #     if message_dist["events"][0]["message"]["type"] == "image":
            
    
    #ユーザーのID送信をキャッチ
    if message_dist["events"][0]["type"] == "message":
        if message_dist["events"][0]["message"]["text"] == r"^[0-9]*$":
            json_open = open('json/matching_result.json')

    json_load = json.load(json_open)
    print("||||", json_load)
    params = {
        "replyToken": message_dist["events"][0]["replyToken"],
        "messages": [json_load]
    }
    request = urllib.request.Request(url, json.dumps(params).encode("utf-8"), method=method, headers=headers)
    with urllib.request.urlopen(request) as res:
        body = res.read()
        print("入力", body)
            
    return 0