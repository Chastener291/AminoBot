try:
    import aminofix as amino
except ModuleNotFoundError:
    print('Download amino.fix,\nhttps://pypi.org/project/amino.fix/\npip install amino.fix')
    raise ModuleNotFoundError('Download amino.fix, https://pypi.org/project/amino.fix/ pip install amino.fix')


client = amino.Client()
email = input('Email >>> ')
password = input('Password >>> ')
client.login(email=email, password=password)
comlink = input('Community link >>> ')
print(f'{client.get_from_code(code=comlink).comId} - paste it in CID in db.py')
chatlink = input('Chat link where bot will work >>> ')
print(f'{client.get_from_code(code=chatlink).objectId} - paste it in READ_CHATS in db.py')
reportlink = input('Chat link where bot will send reports >>> ')
print(f"'{client.get_from_code(code=reportlink).objectId}' - paste it in READ_CHATS in db.py\n")
print('if you want send report to the dm or private chat, use it:\n\n'
      'chats_info = sub_client.get_chat_threads(start=0, size=100)\n'
      'for name, chat_id in zip(chats_info.title, chats_info.chatId):\n'
      '----print(name, chat_id)\n')
print('For any questions: discord K1rLes#3663')
