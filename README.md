# TelegramBOTtler

A Python wrapper for the REST-API of Telegram(https://telegram.org/).
TelegramBOTtler provides easy access to your Telegram bot.

TelegramBOTtler let's you register callback methods for Telegram users based on their id.
And everytime the user send's a message to the Bot the callback get's called.
Inside your callback you have access to the message text and are also able to answer the user both through a BOTtlerMessage-object which is passed as an argument to your callback.

To make use of you bot please add the your token in ```config.json``` 
like:
```json
{
    "token": "Insert your token here",
    "id": 123
}
```
The field ```id``` can be used to store the user id of you personal Telegram account e.g. sending messages to yourself. This field is currently only used for testing.


 