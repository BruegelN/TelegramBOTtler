import sys

if sys.version_info[0] == 2:
    from urllib import urlopen
elif sys.version_info[0] ==3:
    from urllib.request import urlopen
else:
    raise ValueError("This Python version is currently not supported. Try with Python2.7 or Python3.x instead.\n\nYour Python version is "+str(sys.version_info[0]) )

import json


class TelegramBOTtler(object):
    '''
    A Python class which let's you connect to you Telegram bot via your token.
    You can send messages to other user as long as you have their `id`
    or receive messages and handle them with your custom callbacks.
    TODO: still need to impl. somekind of run() method for continous polling.
    '''
    def __init__(self, token):
        self.__update_id = 0
        self.__token = token
        self.__callbacks = {}


    def sendTelegramMessage(self, to_id=0, text=""):
        '''
        Send a message to user with `to_id` and  message `text`.
        Mehtod will return True or false depenig of the result form the server.
        '''
        if to_id == 0:
            return False
        url = "https://api.telegram.org/bot"+self.__token+"/sendMessage?chat_id="+str(to_id)+"&text="+str(text)
        response = urlopen(url)
        data = json.loads(response.read().decode("utf-8"))
        # TODO: remove this print only for debugging
        print(json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False))
        return data["ok"]


    def getUpdates(self):
        '''
        Will ask the Telegram Bot-API for the latest updates of your Bot.
        When ever the Bot receives a new message and for the sender of
        the message a `callback_function` exists it will be called.
        A `callback_function` can be registerd with `registerCallback`.
        Will return the whole json response of getUpdates
        TODO: maybe return true on succes as well as the json or false on failure
        '''
        url = "https://api.telegram.org/bot"+self.__token+"/getUpdates"
        response = urlopen(url)
        json_response = json.loads(response.read().decode("utf-8"))

        for result in json_response["result"]:
            try:
                message_text = result["message"]["text"]
                from_id = result["message"]["from"]["id"]
                if result["update_id"] > self.__update_id:
                    self.__update_id = result["update_id"]
                    self.__callbacks[from_id](message_text, from_id=from_id)
            except Exception as e:
                pass
        return json_response


    def registerCallback(self, from_id="", callback_function=None):
        '''
        Register a custom callback method.
        This method will be called every time the bot receives a new message
        from the user with `from_id`.
        It will get called like this:
        `callback_function(message_text, from_id=from_id)`
        So the call back get the received message text as first argument
        and the id of the current user as second parameter.
        '''
        self.__callbacks[from_id] = callback_function

        