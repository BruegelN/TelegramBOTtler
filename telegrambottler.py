import sys
import json

if sys.version_info[0] == 2:
    from urllib import urlopen
elif sys.version_info[0] ==3:
    from urllib.request import urlopen
else:
    raise ValueError("This Python version is currently not supported. Try with Python2.7 or Python3.x instead.\n\nYour Python version is "+str(sys.version_info[0]) )



class BOTtlerMessage(object):
    '''
    An object of this class will be passed as an argument to your callback.
    '''
    def __init__(self, bot, user_id, message_text):
        self.__bot = bot
        self.__user_id = user_id
        self.__message_text = message_text
    
    def getMessageText(self):
        '''
        Can be used in your callback to retrieve certain 
        information form the written message.
        Return value is of type string.
        '''
        return self.__message_text

    def answer(self, response_text):
        '''
        This method let's you easily responde to messages in your callback.
        '''
        return self.__bot.sendTelegramMessage(to_id=self.__user_id, text=response_text)



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
                    message = BOTtlerMessage(self, user_id=from_id, message_text=message_text)
                    self.__callbacks[from_id](message)
            except Exception as e:
                pass
        return json_response


    def registerCallback(self, from_id="", callback_function=None):
        '''
        Register a custom callback method.
        This method will be called every time the bot receives a new message
        from the user with `from_id`.
        It will get called like this:
        `callback_function(message)`
        The callback gets an object of type `BOTtlerMessage` passed.
        In your callback you can then use the message object to parse the message text
        and to some action based on that e.g. send back an answer.
        '''
        self.__callbacks[from_id] = callback_function


    def deleteCallback(self, from_id):
        '''
        Removes the `callback_function` for the user with `from_id`.
        Afterwards `callback_function` will get not called anymore
        when the bot receives a message for user with `from_id`.
        '''
        self.__callbacks.pop(from_id)


