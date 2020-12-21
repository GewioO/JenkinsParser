# -*- coding: utf-8 -*-
import config, telebot, texts, re
from linkChecking import checkBuildState, realTimeCheck, checkLastBuildsList
from postgresql import db_setLink, db_getLink, db_setPath, db_getPath, db_setNumber ,db_getNumber, db_setTime, db_getTime, db_deleteUser
from telebot import types
from re import match

bot   = telebot.TeleBot(config.token)
state = config.States.START 

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, texts.textsStorage['start'])

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, texts.textsStorage['help'])

@bot.message_handler(commands=['set_link'])
def setLink(message):
    global state
    bot.send_message(message.chat.id, texts.textsStorage['set_link'])
    state = config.States.SET_LINK

@bot.message_handler(commands=['set_path'])
def setPath(message):
    global state
    bot.send_message(message.chat.id, texts.textsStorage['set_path'])
    state = config.States.SET_PATH

@bot.message_handler(commands=['set_number'])
def setNumber(message):
    global state
    bot.send_message(message.chat.id, texts.textsStorage['set_number'])
    state = config.States.SET_BUILD_NUMBER

@bot.message_handler(commands=['set_message_time'])
def setTime(message):
    global state
    bot.send_message(message.chat.id, texts.textsStorage['set_message_time'])
    state = config.States.SET_MESSAGE_TIME

@bot.message_handler(commands=['check_link'])
def sendLink(message):
    bot.send_message(message.chat.id, texts.textsStorage['check_link'] + str(db_getLink(message.chat.id)))

@bot.message_handler(commands=['check_path'])
def sendPath(message):
    bot.send_message(message.chat.id, texts.textsStorage['check_path'] + str(db_getPath(message.chat.id)))

@bot.message_handler(commands=['check_number'])
def sendNumber(message):
    bot.send_message(message.chat.id, texts.textsStorage['check_number_1'] + str(db_getNumber(message.chat.id)))
    bot.send_message(message.chat.id, texts.textsStorage['check_number_2'] + str(db_getPath(message.chat.id)) + str(db_getNumber(message.chat.id)))

@bot.message_handler(commands=['check_message_time'])
def sendTime(message):
    bot.send_message(message.chat.id, texts.textsStorage['check_message_time'] + str(db_getTime(message.chat.id)))

@bot.message_handler(commands=['real_time_check_link'])
def realTimeLink(message):
    state = 0
    if state == 0:
        bot.send_message(message.chat.id, "Waiting for result")
    state, time = realTimeCheck(str(db_getLink(message.chat.id)),str(db_getTime(message.chat.id)))
    if str(db_getTime(message.chat.id)) == "readiness":
        if state == "in process.":
            realTimeNumber(message)
        else:
            sendMessageVariant(message, state, time, str(db_getLink(message.chat.id)))
    else:
        if state == "in process.":
            realTimeNumber(message)
        else:
            sendMessageVariant(message, state, time, str(db_getLink(message.chat.id)))

@bot.message_handler(commands=['real_time_check_number'])
def realTimeNumber(message):
    state, time = realTimeCheck(str(db_getPath(message.chat.id)) + str(db_getNumber(message.chat.id)),str(db_getTime(message.chat.id)))
    if str(db_getTime(message.chat.id)) == "readiness":
        if state == "in process.":
            realTimeNumber(message)
        else:
            sendMessageVariant(message, state, time, str(db_getPath(message.chat.id))+str(db_getNumber(message.chat.id)))
    else:
        if state == "in process.":
            realTimeNumber(message)
        else:
            sendMessageVariant(message, state, time, str(db_getPath(message.chat.id))+str(db_getNumber(message.chat.id)))
    

@bot.message_handler(commands=['check_build_state_link'])
def checkBuildLink(message):
    state, time = checkBuildState(str(db_getLink(message.chat.id)))
    sendMessageVariant(message, state, time, str(db_getLink(message.chat.id)))

@bot.message_handler(commands=['check_build_state_number'])
def checkBuildNumber(message):
    state, time = checkBuildState(str(db_getPath(message.chat.id))+str(db_getNumber(message.chat.id)))
    sendMessageVariant(message, state, time, str(db_getPath(message.chat.id))+str(db_getNumber(message.chat.id)))

@bot.message_handler(commands=['delete_me_from_base'])
def delete(message):
    db_deleteUser(message.chat.id)
    bot.send_message(message.chat.id, texts.textsStorage['delete_me_from_base'])

@bot.message_handler(commands=['last_builds'])
def lastBuilds(message):
    buildNames, buildsNumber = checkLastBuildsList(db_getPath(message.chat.id))
    if buildsNumber == "":
        bot.send_message(message.chat.id, buildNames)
    else:
        i = 0
        buttons = []
        while i < len(buildsNumber):
            buttons.append(types.InlineKeyboardButton(text=str(buildsNumber[i]), callback_data=str(buildsNumber[i])))
            i += 1

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(*buttons)
        bot.send_message(message.chat.id, buildNames, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def inline(c):
    if c.data == 'check':
        state, time = checkBuildState(str(db_getPath(c.message.chat.id))+str(db_getNumber(c.message.chat.id)))
        sendMessageVariant(c.message, state, time, str(db_getPath(c.message.chat.id))+str(db_getNumber(c.message.chat.id)))
    else:
        db_setNumber(c.message.chat.id, str(c.data))
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="Check your build", callback_data=str('check')))
        bot.send_message(c.message.chat.id, texts.textsStorage['textMessageProcessing_2'] + db_getPath(c.message.chat.id) + db_getNumber(c.message.chat.id), reply_markup=keyboard) 

@bot.message_handler(content_types=['text'])
def textMessageProcessing(message):
    global state
    if state == config.States.SET_LINK:
        db_setLink(message.chat.id, str(message.text))
        bot.send_message(message.chat.id, texts.textsStorage['textMessageProcessing_1'] + str(db_getLink(message.chat.id)))
        
    elif state == config.States.SET_PATH:
        db_setPath(message.chat.id, str(message.text))
        bot.send_message(message.chat.id, texts.textsStorage['textMessageProcessing_2'] + str(db_getPath(message.chat.id)))

    elif state == config.States.SET_BUILD_NUMBER:
        db_setNumber(message.chat.id, str(message.text)+"/")
        bot.send_message(message.chat.id, texts.textsStorage['textMessageProcessing_3'] + str(db_getNumber(message.chat.id)))

    elif state == config.States.SET_MESSAGE_TIME:
        db_setTime(message.chat.id, str(message.text))
        bot.send_message(message.chat.id, texts.textsStorage['textMessageProcessing_4'] + str(db_getTime(message.chat.id)))

    state = config.States.START

def sendMessageVariant(message, state, time, link):
    keyboard = types.InlineKeyboardMarkup()
    verifyLink = checkURL(link)
    if not(state) and verifyLink != None:
        url_button = types.InlineKeyboardButton(text="Go to your build", url=link)
        keyboard.add(url_button)
        bot.send_message(message.chat.id, texts.textsStorage['error'], reply_markup=keyboard )
    elif time == "" and verifyLink != None:
        url_button = types.InlineKeyboardButton(text="Go to your build", url=link)
        keyboard.add(url_button)
        bot.send_message(message.chat.id, texts.textsStorage['build_state'] + state, reply_markup=keyboard)
    elif  verifyLink != None:    
        url_button = types.InlineKeyboardButton(text="Go to your build", url=link)
        keyboard.add(url_button)
        bot.send_message(message.chat.id, texts.textsStorage['build_state'] + state + " In: " + time, reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Not correct URL")


def checkURL(link):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|' 
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return re.match(regex, link)

if __name__ == '__main__':
    bot.infinity_polling(True)