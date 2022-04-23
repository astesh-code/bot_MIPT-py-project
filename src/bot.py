import telebot
import csv
from os import environ
from time import time
import stage as st
import re
import logging
import config as conf

TOKEN = environ.get("API_KEY")


bot = telebot.TeleBot(TOKEN)
new_user = 1
mis_counter = 0
logging.basicConfig(
    filename=conf.log_path,
    level=logging.INFO,
    format="%(asctime)s:  in %(funcName)s:  %(message)s")
logging.info('session starts')


@bot.message_handler(commands=['start'])
def get_start(message):
    global tg_id
    tg_id = message.from_user.id
    logging.info(f'user {tg_id} uses start command')
    bot.send_message(tg_id, conf.phrases['hello1'])
    bot.send_message(tg_id, conf.phrases['hello2'], reply_markup=start_key())
    bot.register_next_step_handler(message, get_input)


def get_input(message):
    if message.text == conf.btn_input or message.text == conf.btn_edit:
        bot.send_message(tg_id, conf.phrases['input_number'])
        bot.register_next_step_handler(message, get_number)
    elif message.text == '/start' or message.text == conf.btn_reload:
        logging.info(f'user {tg_id} clears data')
        get_start(message)
    else:
        bot.send_message(tg_id, conf.phrases['press_btn'])
        bot.register_next_step_handler(message, get_input)


def get_number(message):
    global number
    number = message.text
    if re.match(r'[A-Z]{3}\-\d{5}\/\d{2}', number):
        bot.send_message(tg_id, conf.phrases['input_email'])
        bot.register_next_step_handler(message, get_email)
    elif message.text == '/start' or message.text == conf.btn_reload:
        logging.info(f'user {tg_id} clears data')
        get_start(message)
    elif message.text in [conf.btn_input, conf.btn_edit, conf.btn_check]:
        bot.send_message(tg_id, conf.phrases['input_number'])
        bot.register_next_step_handler(message, get_number)
    else:
        bot.send_message(tg_id, conf.phrases['check_number'])
        bot.register_next_step_handler(message, get_number)


def get_email(message):
    global email
    email = message.text
    if re.match(r'[a-zA-Z0-9\-\._]+@[a-z0-9]+(\.[a-z0-9]+){1,}', email):

        bot.send_message(
            tg_id,
            conf.phrases['data_updated'],
            reply_markup=usual_key()
        )

        with open(conf.base_path) as r_file:
            opened_file = csv.DictReader(
                r_file,
                delimiter=";",
                lineterminator="\\n"
            )
            lis = [tg_id, number, email, 0]
            for user in opened_file:
                if int(user['tg_id']) == tg_id and time() < float(user['ban']):
                    lis = [tg_id, number, email, user['ban']]
        with open(conf.base_path, mode="a") as w_file:
            file_writer = csv.writer(
                w_file, delimiter=";", lineterminator="\n")
            file_writer.writerow(lis)
        logging.info(f'user {tg_id} updates data')
        bot.register_next_step_handler(message, get_main)
    elif message.text == '/start' or message.text == conf.btn_reload:
        logging.info(f'user {tg_id} clears data')
        get_start(message)
    elif message.text == conf.btn_input or message.text == conf.btn_edit:
        bot.send_message(tg_id, conf.phrases['input_number'])
        bot.register_next_step_handler(message, get_number)
    elif message.text == conf.btn_check:
        bot.send_message(tg_id, conf.phrases['email_to_start'])
        bot.register_next_step_handler(message, get_email)
    else:
        bot.send_message(tg_id, conf.phrases['check_email'])
        bot.register_next_step_handler(message, get_email)


def get_main(message):
    global tg_id, email, number, new_user
    tg_id = message.from_user.id
    if message.text == conf.btn_check:
        with open(conf.base_path) as r_file:
            opened_file = csv.DictReader(
                r_file, delimiter=";", lineterminator="\\n")
            for user in opened_file:
                if int(user['tg_id']) == tg_id:
                    new_user = 0
                    email = user['email']
                    number = user['number']
                    ban = user['ban']
        if new_user:
            bot.register_next_step_handler(message, get_start)
        elif float(ban) > time():
            banos = int(float(ban)-float(time()))
            bot.send_message(
                tg_id, conf.phrases['ban_time']+f'{banos//60} м {banos%60} с')
            logging.info(f'user {tg_id} gets message with ban time')
            bot.register_next_step_handler(message, get_main)
        else:
            ending(message)
    elif message.text == conf.btn_edit or message.text == conf.btn_input:
        bot.send_message(tg_id, conf.phrases['input_number'])
        bot.register_next_step_handler(message, get_number)
    elif message.text == conf.btn_reload or message.text == '/start':
        logging.info(f'user {tg_id} clears data')
        bot.send_message(tg_id, conf.phrases['erasing'])
        get_start(message)
    else:
        bot.register_next_step_handler(message, get_main)


def ending(message):
    global number, email
    bot.send_message(tg_id, conf.phrases['waiting'])
    data = st.stage(number, email)
    if data:
        number = data.get('number')
        name = data.get('name')
        stage = data.get('stage').lower()
        answer_first = f'Проверил статус завяления {number}, на имя {name}'
        answer_second = f'Статус - {stage}'
        bot.send_message(tg_id, answer_first)
        bot.send_message(tg_id, answer_second)
        bot.send_message(
            tg_id, conf.phrases['success'], reply_markup=usual_key())
        logging.info(f'user {tg_id} gets status: success')
        bot.register_next_step_handler(message, get_main)
    else:
        global mis_counter
        mis_counter += 1
        if mis_counter < 5:
            bot.send_message(
                tg_id, conf.phrases['fail'], reply_markup=usual_key())
            logging.info(f'user {tg_id} gets status: fail')
            bot.register_next_step_handler(message, get_main)
        else:
            bot.send_message(tg_id, conf.phrases['get_ban'])
            logging.info(f'user {tg_id} gets ban')
            with open(conf.base_path, mode="a") as w_file:
                file_writer = csv.writer(
                    w_file, delimiter=";", lineterminator="\n")
                file_writer.writerow(
                    [tg_id, number, email, time()+conf.ban_per])
            bot.register_next_step_handler(message, get_main)


@bot.message_handler()
def sort_empty(message):
    global tg_id
    tg_id = message.from_user.id
    bot.send_message(tg_id, conf.phrases['input_number'])
    bot.register_next_step_handler(message, get_number)


def start_key():
    markup = telebot.types.ReplyKeyboardMarkup(
        one_time_keyboard=True,
        resize_keyboard=True
    )
    btn = telebot.types.KeyboardButton(conf.btn_input)
    markup.add(btn)
    return markup


def usual_key():
    markup = telebot.types.ReplyKeyboardMarkup(
        one_time_keyboard=True,
        resize_keyboard=True
    )
    btn_check = telebot.types.KeyboardButton(conf.btn_check)
    btn_edit = telebot.types.KeyboardButton(conf.btn_edit)
    btn_reload = telebot.types.KeyboardButton(conf.btn_reload)
    markup.add(btn_check, btn_edit, btn_reload)
    return markup


bot.polling(none_stop=True, interval=0)
