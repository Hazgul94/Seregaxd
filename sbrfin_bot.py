import telebot
from config import TOKEN, keys
from extensions import ApiException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start',])
def help(message: telebot.types.Message):
    text = 'Добро пожаловать в бот - конвертер валют \n \
Увидеть доступные валюты /values \
\n Справка /help'
    bot.reply_to(message, text)

@bot.message_handler(commands=['help', ])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в формате: \n <Имя валюты> \
<В какую валюту перенести> \
<Количествол валюты необходимой для перевода> \n \
Пример "Рубль Евро 100" \n \
В результате Вы получите стоимость 100 Рублей в Евро \n \
Увидеть доступные валюты /values \
\n Справка /help \n \
Прошу заметить что бот чуствителен к верхнему и нижнему регистру, \n \
Что означает что А и а не равны!'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'На данный момент доступны валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ApiException('Слишком много параметров')
        
        quote,base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ApiException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена за {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()
