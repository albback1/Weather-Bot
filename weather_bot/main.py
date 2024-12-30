import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types


token = "TOKEN"
bot = telebot.TeleBot(token)

'''
ФУНКЦИИ ПАРСИНГА САЙТОВ

'''

def get_weather(html):
    soup = BeautifulSoup(requests.get(html).text, 'lxml')
    temperature = soup.find('span', class_="_h3 align-top me-1 d-inline-block")
    weather = soup.find('div', class_="col-16 text-500")
    feel = soup.find('div',class_="col-16 mt-0 text-500")
    return f"{temperature.text}, {weather.text}. {feel.text}."

def get_uvi(html, id):
    soup = BeautifulSoup(requests.get(html).text, 'lxml')
    uvi_index = soup.find('div', class_="number")
    int_uvi_index = int(uvi_index.text)
    if int_uvi_index < 3:
        advice = 'Вампиры могут прогуляться.'
        bot.send_sticker(id, "CAACAgEAAxkBAAEK99FnYHCVVxlJn7RuuC2GLjSe5KePVQAC4wkAAr-MkAQnneSdFDZscjYE")
    elif  3 <= int_uvi_index < 7:
        advice = 'Не забудь нанести SPF 30.'
        bot.send_sticker(id, "CAACAgEAAxkBAAEK99xnYHEC3aoPxAABxIq1AeFAWhBWYYYAAt8JAAK_jJAEnkyZEiD409w2BA")
    elif 7 <= int_uvi_index < 11:
        advice = 'SPF 50++! Но лучше посиди дома.'
        bot.send_sticker(id, "CAACAgEAAxkBAAEK99pnYHDgahXhnuNDZKcWTVw5B55CYQAC4gkAAr-MkAQP3M2Ux5s-pzYE")
    elif int_uvi_index >= 11:
        advice = 'Лучше никуда не выходить!'
        bot.send_sticker(id, "CAACAgEAAxkBAAEK99dnYHDHG4icSxHPdAedbjkZBkODWQAC2QkAAr-MkARuJjhruX10oTYE")
    return f"УФ индекс в Краснодаре: {int_uvi_index}. {advice}"

'''
НАЧАЛО ВЗАИМОДЕЙСТВИЯ С БОТОМ. КНОПКИ МЕНЮ.
'''

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Погода")
    btn2 = types.KeyboardButton("УФ-лучи в Краснодаре")
    btn3 = types.KeyboardButton("Разработчик")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Я бесполезный бот, показываю температуру в нескольких городах (это только пока). Выбери, что ты хочешь в меню".format(message.from_user), reply_markup=markup)

'''
ОБРАБОТЧИКИ

'''

@bot.message_handler(func=lambda message: message.text == "Разработчик")
def get_info(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("GitHub", url='https://github.com/albback1')
    markup.add(button1)
    bot.send_message(message.chat.id, "Сайта пока нет, есть только скромный акк на GitHub".format(message.from_user), reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "УФ-лучи в Краснодаре")
def time(message):
        url = "https://www.pogodairadar.com/uf-indeks/krasnodar/5751391"
        bot.send_message(message.chat.id, text=get_uvi(url, message.chat.id))

@bot.message_handler(func=lambda message: message.text == "Погода")
def weather(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Тюмень")
    btn2 = types.KeyboardButton("Краснодар")
    btn3 = types.KeyboardButton("Казань")
    btn4 = types.KeyboardButton("Москва")
    back = types.KeyboardButton("Назад")
    markup.add(btn1, btn2, btn3, btn4, back)
    bot.send_message(message.chat.id, text="Выбери город из меню:".format(message.from_user), reply_markup=markup)
   
@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "Тюмень":
        url = "https://www.meteovesti.ru/pogoda_10/28367"
        bot.send_message(message.chat.id, text="Загружаем данные о погоде в Тюмени...")
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEK93dnYGGK8IH46QnI-7sVm-SazbGSswACkQIAAixg9RzM4FiRBlr3UDYE")
        bot.send_message(message.chat.id, text=get_weather(url)) 
        
    elif message.text == "Краснодар":
        url = "https://www.meteovesti.ru/pogoda/34929"
        bot.send_message(message.chat.id, text="Загружаем данные о погоде в Краснодаре...")
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEK93dnYGGK8IH46QnI-7sVm-SazbGSswACkQIAAixg9RzM4FiRBlr3UDYE")
        bot.send_message(message.chat.id, text=get_weather(url))  

    elif message.text == "Казань":
        url = "https://www.meteovesti.ru/pogoda/27595"
        bot.send_message(message.chat.id, text="Загружаем данные о погоде в Казани...")
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEK93dnYGGK8IH46QnI-7sVm-SazbGSswACkQIAAixg9RzM4FiRBlr3UDYE")
        bot.send_message(message.chat.id, text=get_weather(url))  

    elif message.text == "Москва":
        url = "https://www.meteovesti.ru/pogoda/27612"
        bot.send_message(message.chat.id, text="Загружаем данные о погоде в Москве...")
        bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEK93dnYGGK8IH46QnI-7sVm-SazbGSswACkQIAAixg9RzM4FiRBlr3UDYE")
        bot.send_message(message.chat.id, text=get_weather(url))  
    elif message.text == "Назад":
        start(message)
    else:
        bot.send_message(message.chat.id, text="Такого города в базе нет")
        weather(message)
        


bot.polling(none_stop=True)