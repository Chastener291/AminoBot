from main_funcs import *


@client.event("on_text_message")
def on_text_message(data):
    try:
        if data.json['chatMessage']['content'][0] != '!': return
        # uncommnet next string (9) to check only readchats (check db.py)
        # if data.json['chatMessage']['threadId'] not in READCHATS: return  # READCHATS - check db.py
        # Data processing
        sub_client = amino.SubClient(comId=str(data.json['ndcId']), profile=client.profile)
        chat_id = data.json['chatMessage']['threadId']
        chat_info = sub_client.get_chat_thread(chat_id)
        chat_host_id = chat_info.json['author']['uid']
        chat_host_name = chat_info.json['author']['nickname']
        # chat_name = chat_info.json['title']
        author_name = data.json['chatMessage']['author']['nickname']
        author_id = data.json['chatMessage']['author']['uid']
        msg_id = data.json['chatMessage']['messageId']
        msg_time = data.json['chatMessage']['createdTime']
        msg_content = data.json['chatMessage']['content']
        com_id = str(data.json['ndcId'])
        # A little magic
        # console_log(msg_time, chat_name, author_name, msg_content)
        kwargs = {"chatId": chat_id, "replyTo": msg_id}  # "comId": com_id
        content = str(msg_content).split()
        # pprint.pprint(data.json)

        if len(content[0]) == 1:  # content == "! sddfh", "! save" etc
            return

        content = [content[0][1:]] + content[1:]  # from ['!duel', 'yes'] to ['duel', 'yes']

        if content[0].lower() == 'report':
            try:
                message = report(content[1:], author_id, com_id, chat_id, msg_time)
                sub_client.send_message(chatId=REPORT_CHAT, message=message)
                sub_client.send_message(**kwargs, message='Your message has been sent to the person who hosts this version of the bot!')
                return
            except Exception as e: print(e)

        if content[0].lower() == 'help':
            try:
                if len(content) == 1:
                    return sub_client.send_message(**kwargs, message=
                                                   '[b]Command categories:\n\n'
                                                   '[ci]info\n'
                                                   '[ci]chat\n'
                                                   '[ci]fun\n\n'
                                                   'Send !help {category} for command list.\n'
                                                   'The values in (brackets) are required.\n'
                                                   'The values in [brackets] are optional.\n'
                                                   'GitHub Link - github.com/K1rL3s/aminobot')
                if content[1].lower() == 'info':
                    sub_client.send_message(**kwargs, message=
                                            '[bc]Information\n\n'
                                            '[ci]!help [category]\n'
                                            '[c]Categories - info, chat, fun.\n\n'
                                            '[ci]!get (amino-url)\n'
                                            '[c]The object id\n\n'
                                            '[ci]!report [message]\n'
                                            '[c]Send your message to the creator.\n\n'
                                            '[ci]!user [user-link]\n'
                                            '[c]info about user.\n\n'
                                            '[ci]!chat [chat-link]\n'
                                            '[c]info about chat.\n\n'
                                            '[ci]!com [community-link]\n'
                                            '[c]Info about community. (Link - only about open coms)')
                    return
                if content[1].lower() == 'chat':
                    sub_client.send_message(**kwargs, message=
                                            '[bc]Chat management\n\n'
                                            '[ci]!save\n'
                                            '[c]Saving the title, description, icon and background of the current chat to the database. '
                                            '(Available only for Host ans coHosts)\n\n'
                                            '[ci]!upload\n'
                                            '[c]Set the title, description, icon and background from the last save of the current chat. '
                                            '(Available only for Host ans coHosts. Bot must have a coHost or Host)\n\n'
                                            '[ci]!mention [message]\n'
                                            '[c]Mentions all chat members. (Available only to the Host)')
                    return
                if content[1].lower() == 'fun':
                    sub_client.send_message(**kwargs, message=
                                            '[BC]Fun\n\n'
                                            '[ci]!ping\n'
                                            '[c]Reply "pong". Check if the bot is online.\n\n'
                                            '[ci]!roll [start] [end] [times]\n'
                                            '[c]Random number. The default range is 1 to 100.\n\n'
                                            '[ci]!coin\n'
                                            '[c]Tails, heads or edge (0.5%).\n\n'
                                            '[bc]Duels\n'
                                            '[ci]!duel send (@notify)\n'
                                            '[c]Sends a duel to whoever is mentioned.\n\n'
                                            '[ci]!duel stop\n'
                                            '[c]Cancels the current duel, duel sent to you or sent by you.\n\n'
                                            '[ci]!duel yes\n'
                                            '[c]Accept duel. Chance to shoot first - 50%.\n\n'
                                            '[ci]!duel shot\n'
                                            '[c]Duel shot. Hit chance - 25%.')
                    return
            except Exception as e: print(e)

        if content[0].lower() == 'ping':
            try:
                return sub_client.send_message(**kwargs, message=f"<$pong$>", mentionUserIds=[author_id])
            except Exception as e: print(e)

        if content[0].lower() == 'save':
            try:
                if author_id not in (*chat_info.coHosts, chat_host_id):
                    return sub_client.send_message(**kwargs, message='You are not a Host or coHost.')
                if save_chat(chat_id, sub_client):
                    return sub_client.send_message(**kwargs, message='The title, description, icon and background of the chat have been successfully saved.')
                return error_message(kwargs, sub_client)
            except Exception as e: print(e)

        if content[0].lower() == 'upload':
            try:
                if author_id not in (*chat_info.coHosts, chat_host_id):
                    return sub_client.send_message(**kwargs, message='You are not a Host or coHost.')
                if upload_chat(chat_id, sub_client):
                    return sub_client.send_message(**kwargs, message='The title, description, icon and background of the chat uploaded successfully.')
                return error_message(kwargs, sub_client)
            except Exception as e: print(e)

        if content[0].lower() == 'get':
            try:
                try: url_id = str(id_from_url(content[1]))
                except Exception: url_id = 'None'
                if url_id == 'None':  #  bad link etc
                    return sub_client.send_message(**kwargs, message='Bad argument (link).')
                return sub_client.send_message(**kwargs, message=url_id)
            except Exception as e: print(e)

        if content[0].lower() == 'user':
            try:
                error = 'Bad argument (link).'
                if len(content) != 1:  # for call with link
                    try: author_id = id_from_url(content[1])
                    except Exception: author_id = 'None'
                    if author_id == 'None':  # bad link etc
                        return sub_client.send_message(**kwargs, message='Bad argument (link).')
                try: user_message = func_user_info(author_id, sub_client)
                except Exception as error: user_message = None
                if user_message is None:
                    return sub_client.send_message(**kwargs, message=f"{error}")
                return sub_client.send_message(**kwargs, message=user_message)
            except Exception as e: print(e)

        if content[0].lower() == 'chat':
            try:
                error = 'Bad argument (link).'
                if len(content) != 1:  # for call with link
                    try: chat_id = id_from_url(content[1])
                    except Exception as e: print(e); chat_id = 'None'
                    if chat_id == 'None':  # bad link etc
                        return sub_client.send_message(**kwargs, message='Bad argument (link).')
                try: chat_message = func_chat_info(chat_id, sub_client)
                except Exception as error: chat_message = None
                if chat_message is None:
                    return sub_client.send_message(**kwargs, message=f"{error}")
                return sub_client.send_message(**kwargs, message=chat_message)
            except Exception as e: print(e)

        if content[0].lower() == 'com':
            try:
                error = 'Bad argument (link).'
                if len(content) != 1:  # for call with link
                    try: com_id = id_from_url(content[1])
                    except Exception: chat_id = 'None'
                    if chat_id == 'None':  # bad link etc
                        return sub_client.send_message(**kwargs, message='Bad argument (link).')
                try: com_message = func_com_info(com_id)
                except Exception as error: com_message = None
                if com_message is None:
                    return sub_client.send_message(**kwargs, message=f"{error}")
                return sub_client.send_message(**kwargs, message=com_message)
            except Exception as e: print(e)

        if content[0].lower() == 'mention':
            try:
                if author_id != chat_host_id:
                    return sub_client.send_message(**kwargs, message='You are not a Host.')
                mention_message, mention_users = mention(content[1:], chat_info, sub_client)
                return sub_client.send_message(**kwargs, message=' '.join(mention_message), mentionUserIds=mention_users)
            except Exception as e: print(e)

        if content[0].lower() == 'coin':
            try:
                return sub_client.send_message(**kwargs, message=f'Tossing a coin...\nIt is {coin()}!')
            except Exception as e: print(e)

        if content[0].lower() == 'roll':
            try:
                return sub_client.send_message(**kwargs, message=roll(content))
            except Exception as e: print(e)

        if content[0].lower() == 'duel':
            try:
                if content[1].lower() == 'stop':
                    if author_id in duels_first_dict.keys():
                        second = duels_first_dict[author_id][1]
                        stop_duel(author_id, second)
                        return sub_client.send_message(**kwargs, message='Your duel request has been cancelled.')
                    if author_id in duels_second_dict.keys():
                        first = duels_second_dict[author_id]
                        stop_duel(first, author_id)
                        return sub_client.send_message(**kwargs, message='Your duel request has been cancelled.')
                    return sub_client.send_message(**kwargs, message='You dont have any requests.')

                if content[1].lower() == 'send':
                    first = author_id
                    second = data.json['chatMessage']['extensions']['mentionedArray'][0]['uid']
                    if first in duels_first_dict.keys() or first in duels_second_dict.keys():
                        return sub_client.send_message(**kwargs, message='You cant send duels right now.')
                    if second in duels_second_dict.keys() or second in duels_first_dict.keys():
                        return sub_client.send_message(**kwargs, message='Cannot send duel to this user.')
                    second_name = sub_client.get_user_info(userId=second).nickname
                    duel = Duel(author_id, second, author_name, second_name, chat_id)
                    duels_first_dict[author_id] = tuple([duel, second])
                    duels_second_dict[second] = author_id
                    return sub_client.send_message(**kwargs, message=f'Waiting for accept the duel by {second_name}...')

                if content[1].lower() == 'yes':
                    second = author_id
                    if second not in duels_second_dict.keys():
                        return sub_client.send_message(**kwargs, message='You dont have any request𝐬.')
                    if second in duels_first_dict.keys():
                        return sub_client.send_message(**kwargs, message='You already have a duel request.')
                    duel = duels_first_dict[duels_second_dict[second]][0]
                    duel.start_duel()
                    sub_client.send_message(chatId=chat_id, mentionUserIds=[duel.first, duel.second, duel.who_start_id], message=
                                            f'The duel between <${duel.first_name}$> abd <${duel.second_name}$> begins!\n'
                                            f'(!duel shot, <${duel.who_start_name}$> starts)')
                    return

                if content[1].lower() == 'shot':
                    if author_id not in duels_started.keys():
                        return sub_client.send_message(**kwargs, message='You dont have a duel right now.')
                    duel = duels_started[author_id]
                    message = duel.shot(author_id)
                    if message == 'nostart':
                        return sub_client.send_message(**kwargs, message='The duel hasnt started yet!')
                    if message == 'noturn':
                        return sub_client.send_message(**kwargs, message='Not your turn!')
                    if message == 'miss':
                        return sub_client.send_message(**kwargs, message=f'Miss. Next player shot!\n'
                                                                         f'Shots: {duel.shots}')
                    if message == 'win':
                        name = duel.first_name if author_id == duel.first else duel.second_name
                        sub_client.send_message(**kwargs, mentionUserIds=[author_id], message=
                                                f'Hit! <${name}$> won this duel!\n'
                                                f'Total shots: {duel.shots}')
                        stop_duel(duel.first, duel.second)
                        return
            except Exception as e: print(e)

        if content[0].lower() == 'kickorg':  # like a prank
            try:
                sub_client.send_message(**kwargs, mentionUserIds=[author_id], message=
                                        f'Starting host transfer ro <${author_name}$>...')
                time.sleep(3)  # ???
                sub_client.send_message(chatId=chat_id, messageType=107, message=
                                        f'Участник {author_name} стал огранизатором этого чата.')
                # The author doesnt know this system message in english language. Use translation to correct it
                time.sleep(3)  # ???
                sub_client.send_message(chatId=chat_id, messageType=107, message=
                                        f'{chat_host_name} покинул(а) разговор.')
                # The author doesnt know this system message in english language. Use translation to correct it
                return
            except Exception as e: print(e)

        if content[0].lower() == 'chatimages':
            try:
                chat_icon = chat_info.icon
                chat_bg = chat_info.backgroundImage
                sub_client.send_message(**kwargs, message=
                                        f'Icon: {"There is no icon" if chat_icon is None else chat_icon}\n'
                                        f'Background: {"There is no bg" if chat_bg is None else chat_bg}')
                return
            except Exception as e: print(e)

        if content[0].lower() == 'follow':
            try:
                sub_client.follow(userId=author_id)
                return sub_client.send_message(**kwargs, message='Successful subscription!')
            except Exception as e: print(e)

        try:
            sub_client.send_message(**kwargs, message=
                                    'Command failed.\n'
                                    'Possible reasons:\n'
                                    '1. The bot has no rights to do this.\n'
                                    '2. Invalid command.\n'
                                    '3. Invalid arguments.\n'
                                    '4. Contact the creator on github.')
            return
        except Exception as e: print(e)

    except Exception as e: print(e)
