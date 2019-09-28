import telebot
from telebot import types

bot = telebot.TeleBot('877686854:AAGR_kcDf70arRSR0wzWi4K_8HDumhv9HpM')


# @bot.message_handler(content_types=["text"])
# def get_text_messages(message):
    # if message.text == "Привет":
    #     bot.send_message(message.from_user.id, 'Привет, чем могу помочь ?')
    # elif message.text == "/help":
    #     bot.send_message(message.from_user.id, "Напиши привет")
    # else:
    #     bot.send_message(message.from_user.id, 'Я тебя не понимаю. Напиши /help ')


name = ""
surname = ""
age = 0


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, 'Как тебя зовут')
        bot.register_next_step_handler(message, get_name)  # следующий шаг - функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')


def get_name(message):  # получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, "Сколько тебе лет ?")
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    global age
    while age == 0:  # Проверяем что возрас изменился
        try:
            age = int(message.text)  # Проеряем что возраст введен корректно
        except Exception:
            bot.send_message(message.from_user, "Цифрами пожалуйста")
        question = f"Тебе {age} лет , тебя зовут {name} {surname} ?"
        keyboard = types.InlineKeyboardMarkup()  # Наша клавиатура
        key_yes = types.InlineKeyboardButton(text="Да", callback_data='yes')  # Кнопка Да
        keyboard.add(key_yes)
        key_no = types.InlineKeyboardButton(text="Нет", callback_data='no')  # Кнопка Нет
        keyboard.add(key_no)
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'yes':
        bot.send_message(call.message.chat.id, 'Запомню')
    elif call.data == 'no':
        start('/reg')


bot.polling(none_stop=True, interval=0)
