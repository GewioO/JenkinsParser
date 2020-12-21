# Jenkins parser bot

Telegram bot for checking build stage in Jenkins if you do not have access to Jenkins api.

## Bot commands

* /start 
* /help - commands guide
* /set_link - writes a link, which you can later check.
* /check_link - checking the saved address.
* /set_path - you can write down the path to the builder, in this case, for further verification, you will not need to rewrite the entire link. You only need to send the build number. 
* /check_path - check saved path before build.
* /set_number - write down the number, it will come together with the path. Further, to check the assembly, you only need to update the number using /setNumber, and then send /checkBuildStateNumber. 
* /check_number - check saved number before build.
* /check_build_state_link - command to check the build from the link. Before shipment, you need to use /setLink.
* /check_build_state_number - checking the status by build number. Before first use, you must to use /set_path. Next, add your build number /set_number (all data is saved, then, for the same assembly, you can simply use /check_build_state_number.)
* /real_time_check_link or /real_time_check_number - use if you want the bot to check your build periodically and send you an alert once at a specified time. Default time = 300 seconds (5 minutes).
* /set_message_time - set time for /real_time_check_link or /real_time_check_number (in minutes). If you send: readiness , a status message will only be sent to you on completion or on error.
* /delete_me_from_base - delete information about you. Every time when you do this, the cats cry.
* /last_builds - you can check last 10 build. Before that, once, enter the command /set_path. Next, you will have buttons with the choice of the build number. After clicking, the build number will be copied, as with the /set_number command. Next, you will be prompted to check the assembly with the selected number.

!!! 
    Build have 3 state: SUCCESS, FAILURE and in process (if the build is assembling),
    There is also a specific bug when the build has not started. Then you will see: "Something wrong, please check your build."
!!!

## Libs

* [Telebot](https://github.com/eternnoir/pyTelegramBotAPI)
    * Use: pip3 install pytelegrambotapi

* [psycopg2](https://github.com/psycopg/psycopg2)
    * Use: pip3 install psycopg2

* [BeautifulSoup](https://github.com/wention/BeautifulSoup4)
    * Use: pip3 install BeautifulSoup4

* [requests](https://requests.readthedocs.io/en/master/)
    * Use: pip3 install requests

## Data base

* [postgeSQL](https://www.postgresql.org/download/)

## Ignore files

* You need create config.py, which looks like:

    from enum import Enum

    token = "Your token"

    class States(Enum):
        START            = 0
        SET_LINK         = 1
        SET_PATH         = 2
        SET_BUILD_NUMBER = 3
        SET_MESSAGE_TIME = 4

* You need use file where will you store the texts for the commands.
    * I use map. Key -> command name or something related to the command (textMessageProcessing_2);
    * Help have big text. For help I use dict.