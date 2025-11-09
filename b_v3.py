import telebot
import os
import re

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Введите домен веб-сайта:")

@bot.message_handler(func=lambda message: True)
def search_domain(message):
    domain = message.text.strip()
    results = []
    
    for filename in os.listdir('db'):
        if filename.endswith('.txt'):
            with open(os.path.join('db', filename), 'r') as file:
                for line in file:
                    if re.search(r'\b' + re.escape(domain) + r'\b', line):
                        results.append(line.strip())

    if results:
        result_file = f"{domain}.txt"
        with open(result_file, 'w') as f:
            f.write('\n'.join(results))
        
        with open(result_file, 'rb') as f:
            bot.send_document(message.chat.id, f, caption=f'Найдено {len(results)} результатов.')
            os.system(f'rm {domain}.txt')

    else:
        bot.send_message(message.chat.id, "Совпадений не найдено.")
        os.system(f'rm {domain}.txt')

bot.polling()
