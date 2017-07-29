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
    updates_json = myBot.getUpdates()
    #print str(myBot.sendTelegramMessage(id=me, text="number"))
    print_my_json(updates_json)
    
    # try second to make shure the callback get only called once for every message 
    updates_json = myBot.getUpdates()
    #print str(myBot.sendTelegramMessage(id=me, text="number"))
    print_my_json(updates_json)

if __name__ == "__main__":
    main()

