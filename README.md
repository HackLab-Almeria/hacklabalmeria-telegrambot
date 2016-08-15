# HackLabAlmería RSS and Feeds parser bot

This is a very simple Telegram bot for automagically feeding HackLab Almería
Telegram channel and group with some of the community activity.

## Requirements:

It should work on a **Python 2.7** interpreter, along with the following dependencies:

* **beautifulsoup4**
* **requests**
* **python-dateutil**
* **lxml==3.6.1**

You can install them manually with `pip` or by using `pip install -r requirements.txt`.

## Usage:

Run `python parser.py` to get it working. It should be called regularly, using a CRON or some service.
If your input streams use UNICODE characters probably you'll need to set the
LANG variable as in `LANG=es_ES.utf8 python parser.py`.

You can set the `PARSE_ONLY_NEW` to `True` to parse only new items since the last time this script was executed, or to `False` to parse and send all items, including possible duplicates. 

You may change the target *Channel* by modifying the `BOT_CHANNEL` variable using your public channel id - in example: `@ChannyMcChannelFace`.
Remember to invite the bot to your channel as an __administrator__.

You can also change the target *Group*, but you have to get the **secret group id**. To do that, you can invite the `my_id` bot to the desired group and then ask him `/my_id`. The result will be the group id.
You should invite the bot as a group's member.

## How does it work?

The `SOURCES` variable contains the list of `Source` objects that will provide the data. Each `Source` has an `Adapter` which will turn the raw response of the `Source` into a valid `Message`.
 
All messages will be merged into a single list which will be sorted ascending by date so older messages are sent first and everything is received in the correct order.

Messages will be sent to both the *Channel* and the *Group* and only will be considered the last sent item - aka `last_item` when they were sent successfuly to both chats.

## One more thing:

Telegram supports [some HTML tags](https://core.telegram.org/bots/api#html-style), but not all of them and you can't nest tags - i.e. `<b><a>...</a></b>`. Be careful with your tags or the messages won't be sent at all.