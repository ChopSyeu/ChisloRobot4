import telebot
import random

TOKEN = '6222882207:AAHyrF82_EWgAn75-hLJPSod6LrXz9lxyQA'

bot = telebot.TeleBot(TOKEN)

# Количество попыток для каждой игры
MAX_TRIES = 5

# Словарь для хранения текущих игр и количества попыток
games = {}

# База данных стихотворений
poems = [
    "Я не знаю, зачем мне это нужно\nГоворить о тебе в стихах,\nНо иногда я просыпаюсь по ночам,\nИ мне кажется, что я живу снова.",
    "Для меня нет утра, без тебя в нём нет света,\nС тобою взгляды наши - словно беседы.\nКак много чудес создало природа,\nНо такого, как ты, неродили.",
    "Ваше благородие, сударь,\nНас очень тронуло,\nНо мы не привыкли к таким словам,\nМы скромные люди, простые рыцари.",
    "Хотелось бы вам кое-что сказать,\nПорой устают даже ноги героя,\nНо сердце и душа всегда остаются на месте,\nКогда встречаются с настоящей любовью.",
]

# База данных цитат
quotes = [
    "Я не боюсь умереть, я просто не хочу этого делать.\n— Монти Пайтон",
    "Сложнее всего начать действовать, все остальное зависит только от упорства.\n— Амелия Эрхарт",
    "Война — это способ ошибок и заблуждений, которые не умирают после своих авторов.\n— Джон Кеннеди",
    "Что такое жизнь? Она является трагедией, однако я ее считаю комедией.\n— Чарли Чаплин",
]

@bot.message_handler(commands=['start'])
def handle_start(message):
    sti = open('Cartoon/sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    
    # Генерируем случайное число и сохраняем его в словаре игр под ключом chat_id
    games[message.chat.id] = {'number': random.randint(1, 100), 'tries_left': MAX_TRIES}
    
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = telebot.types.KeyboardButton('Новая игра')
    itembtn2 = telebot.types.KeyboardButton('Стих')
    itembtn3 = telebot.types.KeyboardButton('Цитата')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, "Привет! Я загадал число от 1 до 100. Попробуй угадать его!", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_guess(message):
    if message.text == 'Новая игра':
        games[message.chat.id] = {'number': random.randint(1, 100), 'tries_left': MAX_TRIES}
        bot.send_message(message.chat.id, "Новая игра началась! Я загадал число от 1 до 100. Попробуй угадать его!")
        return
    elif message.text == 'Стих':
        poem = random.choice(poems)
        bot.send_message(message.chat.id, poem)
        return
    elif message.text == 'Цитата':
        quote = random.choice(quotes)
        bot.send_message(message.chat.id, quote)
        return
    
    try:
        guess = int(message.text)
        game_data = games.get(message.chat.id)

        if not game_data:
            bot.send_message(message.chat.id, "Чтобы начать новую игру, нажмите 'Новая игра'.")
            return

        secret_number = game_data['number']
        tries_left = game_data['tries_left']

        if guess == secret_number:
            bot.send_message(message.chat.id, "Поздравляю, ты угадал число!")
            games[message.chat.id] = None
        elif guess > secret_number:
            tries_left -= 1
            games[message.chat.id]['tries_left'] = tries_left
            if tries_left == 0:
                bot.send_message(message.chat.id, f"Ты проиграл! Загаданное число было {secret_number}. Нажми 'Новая игра', чтобы начать заново.")
                games[message.chat.id] = None
            else:
                bot.send_message(message.chat.id, f"Твоё число слишком большое, попробуй еще раз! Осталось попыток: {tries_left}")
        elif guess < secret_number:
            tries_left -= 1
            games[message.chat.id]['tries_left'] = tries_left
            if tries_left == 0:
                bot.send_message(message.chat.id, f"Ты проиграл! Загаданное число было {secret_number}. Нажми 'Новая игра', чтобы начать заново.")
                games[message.chat.id] = None
            else:
                bot.send_message(message.chat.id, f"Твоё число слишком маленькое, попробуй еще раз! Осталось попыток: {tries_left}")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите целое число.")
    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка: {}".format(str(e)))

bot.polling(none_stop=True)