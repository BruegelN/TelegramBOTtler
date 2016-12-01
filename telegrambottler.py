import sys

if sys.version_info[0] == 2:
    from urllib import urlopen
elif sys.version_info[0] ==3:
    from urllib.request import urlopen
else:
    raise ValueError("This Python version is currently not supported. Try with Python2.7 or Python3.x instead.\n\nYour Python version is "+str(sys.version_info[0]) )

import json


class TelegramBOTtler(object):
    def __init__(self, token=None):
        if token is None:
            raise ValueError('Please provide a token')
        self.__token = token
        self.__callbacks = {}


    def sendTelegramMessage(self, id=0, text=""):
        if id == 0:
            return False
        url = "https://api.telegram.org/bot"+self.__token+"/sendMessage?chat_id="+str(id)+"&text="+str(text)
        response = urlopen(url)
        data = json.loads(response.read().decode("utf-8"))
        print(json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False))
        return data["ok"]


    def getUpdates(self):
        url = "https://api.telegram.org/bot"+self.__token+"/getUpdates"
        # TODO: iterate over all results and check if callback for the user id exists
        from_id = json_response["result"][0]["message"]["from"]["id"]
        message_text = json_response["result"][0]["message"]["text"]
        print "Callback for "+str(from_id)+" with text "+message_text
        self.__callbacks[from_id](message_text)

        response = urlopen(url)
        json_response = json.loads(response.read().decode("utf-8")) 
        return json_response


    def registerCallback(self, id="", callback_function=None):
        self.__callbacks[id] = callback_function

        