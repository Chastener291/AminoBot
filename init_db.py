import sqlite3


"""
START IT IF YOU DO NOT HAVE A 'database.db' FILE IN DIRECTORY
OR DO NOT HAVE A 'TABLE chats'
OR DO NOT HAVE A 'TABLE commands'
"""

with sqlite3.connect('database.db') as db:
    sql = db.cursor()
    sql.execute("""
        CREATE TABLE chats (
        chat_id TEXT,
        chat_name TEXT,
        chat_icon TEXT,
        chat_bg TEXT,
        chat_desc TEXT)""")
    db.commit()

    sql.execute("""
        CREATE TABLE commands (
        chat_id TEXT,
        command TEXT)""")
    db.commit()
