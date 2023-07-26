import telebot
import sqlite3
from datetime import datetime
import RoBertA

TOKEN = '6414676263:AAFwGNELqRMtUvXBTIg3vmqTqZJiNyDa4Ng'
bot = telebot.TeleBot(TOKEN)
chat_states = {}
db_file = "database/messages.db"

def create_connection():
    return sqlite3.connect(db_file)

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item = telebot.types.KeyboardButton('Создать новое обращение')
    markup.add(item)
    bot.send_message(message.chat.id, "Привет! Чем я могу вам помочь?", reply_markup=markup)

@bot.message_handler(func=lambda message: chat_states.get(message.chat.id) == 'waiting_for_text')
def process_issue_text(message):
    chat_id = message.chat.id
    issue_text = message.text
    label = classify_word(issue_text)
    status = 'Waiting'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    chat_states[chat_id] = None
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (chat_id, timestamp, text, label, status) VALUES (?, ?, ?, ?, ?)",
                       (chat_id, timestamp, issue_text, label, status))
        conn.commit()
    bot.send_message(chat_id, f"Обращение принято:\n{issue_text}")

@bot.message_handler(func=lambda message: message.text == 'Создать новое обращение')
def create_issue(message):
    chat_id = message.chat.id
    chat_states[chat_id] = 'waiting_for_text'
    bot.send_message(message.chat.id, 'Пожалуйста, опишите вашу проблему')
    
def classify_word(text):
    result = RoBertA.classify(text)
    return result

if __name__ == "__main__":
    bot.polling(none_stop=True)
