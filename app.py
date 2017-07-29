from telegrambottler import TelegramBOTtler
import json
import sys
import time as t


def custom_callback(Message):
    text = Message.getMessageText()
    print ("I got the following message: " + text)
    Message.answer("Echo: "+text)


def main():
    me = 0
    bot_token = ""

    with open('config.json') as json_config:
        data = json.load(json_config)
        me = data["id"]
        bot_token = data["token"]

    myBot = TelegramBOTtler(token=bot_token)
    # first register a callback before getting updates
    myBot.registerCallback(me, custom_callback)
    myBot.run()
    t.sleep(30)
    myBot.stop()

if __name__ == "__main__":
    main()

