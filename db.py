import sqlite3


EMAIL = 'youremail'  # paste your email
PASSWORD = 'yourpass'  # paste your password
CID = 'communityId'  # paste community id
READCHATS = ('chatId', 'chatId')  # paste the chat ids where the bot will work
REPORT_CHAT = 'chatId'  # paste the chat id where the bot will send reports


def save_chat_in_db(chat_id, chat_name, chat_icon, chat_bg, chat_desc):
    db = sqlite3.connect('database.db', check_same_thread=False)
    sql = db.cursor()
    chat_ids = tuple([i[0] for i in sql.execute("SELECT chat_id FROM chats")])
    if chat_id in chat_ids:
        sql.execute(f"UPDATE chats SET chat_id = '{chat_id}', chat_name = '{chat_name}', chat_icon = '{chat_icon}',"
                    f"chat_bg = '{chat_bg}', chat_desc = '{chat_desc}' WHERE chat_id = '{chat_id}'")
    else:
        sql.execute(f"INSERT INTO chats VALUES ('{chat_id}', '{chat_name}', '{chat_icon}', '{chat_bg}', '{chat_desc}')")
    db.commit()
    db.close()
    return True


def return_chat_info_from_db(chat_id):
    db = sqlite3.connect('database.db', check_same_thread=False)
    sql = db.cursor()
    s = sql.execute(f"SELECT * FROM chats WHERE chat_id = '{chat_id}'")
    chat_info = s.fetchone()
    db.close()
    return chat_info

