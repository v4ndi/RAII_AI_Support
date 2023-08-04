import sqlite3
import telebot 

# api_token = ""

def update_status_by_chat_id(db_file, chat_id, text, id):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM messages WHERE id=?", (id,))
        row = cursor.fetchone()

        if row is not None:
            cursor.execute("UPDATE messages SET status = \'Done\' WHERE id=?", (id,))
            conn.commit()
            print(f"Status updated to 1 for chat_id {chat_id}")
        else:
            print(f"Row not found for chat_id {chat_id}")

    except sqlite3.Error as e:
        print(f"Error: {e}")

    finally:
        send_message_to_telegram_bot(chat_id, text)
        if conn:
            conn.close()


def send_message_to_telegram_bot( chat_id, message):
    try:
        message = 'Answer: \n' + message
        bot = telebot.TeleBot(api_token)

        bot.send_message(chat_id, message)
        
        print(f"Message sent to chat_id {chat_id}: {message}")

    except telebot.apihelper.ApiException as e:
        print(f"Error: {e}")






