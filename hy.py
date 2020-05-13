import jwt
import websocket
import json
import time
import _thread as thread


def get_sign(app_id, secret):
    payload = {
        "iat": int(time.time()),
        "exp": int(time.time()) + 600,
        "appId": app_id
    }
    sig = jwt.encode(payload, secret, algorithm='HS256').decode()
    print(sig)
    return sig


def on_message(ws, message):
    info = json.loads(message)
    print(info)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        ws.send(
            '{"command":"subscribeNotice","data":["getMessageNotice","getVipEnterBannerNotice","getSendItemNotice","getOnTVAwardNotice", "getOpenNobleNotice", "getOpenGuardianNotice", "getUserMutedNotice"],"reqId":"123456789"}')
        while True:
            # 心跳
            ws.send("ping")
            time.sleep(10)

    thread.start_new_thread(run, ())


if __name__ == "__main__":
    room_id = 521000
    app_id = '780a6c2455a8916b'
    secret = '19d5039edb723d41fc5b2b7ef27b5c3c'
    sign = get_sign(app_id, secret)
    print(sign)
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(
        "ws://ws-apiext.huya.com/index.html?do=comm&roomId=" + str(room_id) + "&appId=" + app_id + "&iat=" + str(
            int(time.time())) + "&sToken=" + sign,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
