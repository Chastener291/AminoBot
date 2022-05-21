from main_funcs import *


@client.event("on_text_message")
def on_text_message(data):
    try:
        if data.json['chatMessage']['threadId'] not in READCHATS: return  # READCHATS - check db.py
        # Data processing
        chat_info = sub_client.get_chat_thread(data.json['chatMessage']['threadId'])
        chat_host_id = chat_info.json['author']['uid']
        chat_host_name = chat_info.json['author']['nickname']
        chat_name = chat_info.json['title']
        chat_id = data.json['chatMessage']['threadId']
        author_name = data.json['chatMessage']['author']['nickname']
        author_id = data.json['chatMessage']['author']['uid']
        msg_id = data.json['chatMessage']['messageId']
        msg_time = data.json['chatMessage']['createdTime']
        msg_content = data.json['chatMessage']['content']
        com_id = str(chat_info.json['ndcId'])
        # A little magic
        console_log(msg_time, chat_name, author_name, msg_content)
        kwargs = {"chatId": chat_id, "replyTo": msg_id}
        content = str(msg_content).split()
        # pprint.pprint(data.json)

        if author_id in report_ids:  # "!report" before
            try:
                message = report(content, author_id, com_id, chat_id, msg_time)
                report_ids.remove(author_id)
                sub_client.send_message(**kwargs, message='𝐘𝐨𝐮𝐫 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐡𝐚𝐬 𝐛𝐞𝐞𝐧 𝐬𝐞𝐧𝐭!')
                return sub_client.send_message(chatId=REPORT_CHAT, message=message)  # REPORT_CHAT - check db.py
            except Exception as e: print(e)

        if content[0][0] != '!':
            return
        if len(content[0]) == 1:  # content == "! sddfh", "! save" etc
            return

        if content[0][1:].lower() == 'report':
            try:
                if len(content) == 1:
                    report_ids.append(author_id)
                    return sub_client.send_message(**kwargs, message=
                                                   f'𝐘𝐨𝐮 𝐮𝐬𝐞𝐝 𝐚 𝐜𝐨𝐦𝐦𝐚𝐧𝐝 !𝐫𝐞𝐩𝐨𝐫𝐭.\n'
                                                   f'𝐘𝐨𝐮𝐫 𝐧𝐞𝐱𝐭 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐰𝐢𝐥𝐥 𝐛𝐞 𝐬𝐞𝐧𝐭 𝐭𝐨 𝐭𝐡𝐞 𝐩𝐞𝐫𝐬𝐨𝐧 𝐰𝐡𝐨 𝐡𝐨𝐬𝐭𝐬 𝐭𝐡𝐢𝐬 𝐯𝐞𝐫𝐬𝐢𝐨𝐧 𝐨𝐟 𝐭𝐡𝐞 𝐛𝐨𝐭, '
                                                   f'𝐝𝐞𝐬𝐜𝐫𝐢𝐛𝐞 𝐲𝐨𝐮𝐫 𝐩𝐫𝐨𝐛𝐥𝐞𝐦/𝐪𝐮𝐞𝐬𝐭𝐢𝐨𝐧.')
                message = report(content[1:], author_id, com_id, chat_id, msg_time)
                sub_client.send_message(**kwargs, message='𝐘𝐨𝐮𝐫 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐡𝐚𝐬 𝐛𝐞𝐞𝐧 𝐬𝐞𝐧𝐭!')
                sub_client.send_message(chatId=REPORT_CHAT, message=message)
                return
            except Exception as e: print(e)

        if content[0][1:].lower() == 'help':
            try:
                if len(content) == 1:
                    return sub_client.send_message(**kwargs, message=
                                                   '[b]𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐜𝐚𝐭𝐞𝐠𝐨𝐫𝐢𝐞𝐬:\n\n'
                                                   '[i]𝐢𝐧𝐟𝐨\n'
                                                   '[i]𝐜𝐡𝐚𝐭\n'
                                                   '[i]𝐟𝐮𝐧\n\n'
                                                   '[i]𝐒𝐞𝐧𝐝 !𝐡𝐞𝐥𝐩 {𝐜𝐚𝐭𝐞𝐠𝐨𝐫𝐲} 𝐟𝐨𝐫 𝐜𝐨𝐦𝐦𝐚𝐧𝐝 𝐥𝐢𝐬𝐭.\n'
                                                   '[i]𝐓𝐡𝐞 𝐯𝐚𝐥𝐮𝐞𝐬 𝐢𝐧 (𝐛𝐫𝐚𝐜𝐤𝐞𝐭𝐬) 𝐚𝐫𝐞 𝐫𝐞𝐪𝐮𝐢𝐫𝐞𝐝.\n'
                                                   '[i]𝐓𝐡𝐞 𝐯𝐚𝐥𝐮𝐞𝐬 𝐢𝐧 [𝐛𝐫𝐚𝐜𝐤𝐞𝐭𝐬] 𝐚𝐫𝐞 𝐨𝐩𝐭𝐢𝐨𝐧𝐚𝐥.')
                if content[1].lower() == 'info':
                    return sub_client.send_message(**kwargs, message=
                                                   '[bc]𝐈𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧\n\n'
                                                   '[ci]!𝐡𝐞𝐥𝐩 [𝐜𝐚𝐭𝐞𝐠𝐨𝐫𝐲]\n'
                                                   '[c]𝐂𝐚𝐭𝐞𝐠𝐨𝐫𝐢𝐞𝐬 - 𝐢𝐧𝐟𝐨, 𝐜𝐡𝐚𝐭, 𝐟𝐮𝐧.\n\n'
                                                   '[ci]!𝐠𝐞𝐭 (𝐚𝐦𝐢𝐧𝐨-𝐮𝐫𝐥)\n'
                                                   '[c]𝐓𝐡𝐞 𝐨𝐛𝐣𝐞𝐜𝐭 𝐢𝐝\n\n'
                                                   '[ci]!𝐫𝐞𝐩𝐨𝐫𝐭 [𝐦𝐞𝐬𝐬𝐚𝐠𝐞]\n'
                                                   '[c]𝐒𝐞𝐧𝐝 𝐲𝐨𝐮𝐫 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐭𝐨 𝐭𝐡𝐞 𝐜𝐫𝐞𝐚𝐭𝐨𝐫.\n\n'
                                                   '[ci]!𝐮𝐬𝐞𝐫 [𝐮𝐬𝐞𝐫-𝐥𝐢𝐧𝐤]\n'
                                                   '[c]𝐈𝐧𝐟𝐨 𝐚𝐛𝐨𝐮𝐭 𝐮𝐬𝐞𝐫.\n\n'
                                                   '[ci]!𝐜𝐡𝐚𝐭 [𝐜𝐡𝐚𝐭-𝐥𝐢𝐧𝐤]\n'
                                                   '[c]𝐈𝐧𝐟𝐨 𝐚𝐛𝐨𝐮𝐭 𝐜𝐡𝐚𝐭.\n\n'
                                                   '[ci]!𝐜𝐨𝐦 [𝐜𝐨𝐦𝐦𝐮𝐧𝐢𝐭𝐲-𝐥𝐢𝐧𝐤]\n'
                                                   '[c]𝐈𝐧𝐟𝐨 𝐚𝐛𝐨𝐮𝐭 𝐜𝐨𝐦𝐦𝐮𝐧𝐢𝐭𝐲. (𝐋𝐢𝐧𝐤 - 𝐨𝐧𝐥𝐲𝐨 𝐚𝐛𝐨𝐮𝐭 𝐨𝐩𝐞𝐧 𝐜𝐦)')
                if content[1].lower() == 'chat':
                    return sub_client.send_message(**kwargs, message=
                                                   '[bc]𝐂𝐡𝐚𝐭 𝐦𝐚𝐧𝐚𝐠𝐞𝐦𝐞𝐧𝐭\n\n'
                                                   '[ci]!𝐬𝐚𝐯𝐞\n'
                                                   '[c]𝐒𝐚𝐯𝐢𝐧𝐠 𝐭𝐡𝐞 𝐭𝐢𝐭𝐥𝐞, 𝐝𝐞𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧, 𝐢𝐜𝐨𝐧 𝐚𝐧𝐝 𝐛𝐚𝐜𝐤𝐠𝐫𝐨𝐮𝐧𝐝 𝐨𝐟 𝐭𝐡𝐞 𝐜𝐮𝐫𝐫𝐞𝐧𝐭 𝐜𝐡𝐚𝐭 𝐭𝐨 𝐭𝐡𝐞 𝐝𝐚𝐭𝐚𝐛𝐚𝐬𝐞. '
                                                   '(𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐨𝐧𝐥𝐲 𝐟𝐨𝐫 𝐇𝐨𝐬𝐭 𝐚𝐧𝐝 𝐜𝐨𝐇𝐨𝐬𝐭𝐬)\n\n'
                                                   '[ci]!𝐮𝐩𝐥𝐨𝐚𝐝\n'
                                                   '[c]𝐒𝐞𝐭 𝐭𝐡𝐞 𝐭𝐢𝐭𝐥𝐞, 𝐝𝐞𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧, 𝐢𝐜𝐨𝐧 𝐚𝐧𝐝 𝐛𝐚𝐜𝐤𝐠𝐫𝐨𝐮𝐧𝐝 𝐟𝐫𝐨𝐦 𝐭𝐡𝐞 𝐥𝐚𝐬𝐭 𝐬𝐚𝐯𝐞 𝐨𝐟 𝐭𝐡𝐞 𝐜𝐮𝐫𝐫𝐞𝐧𝐭 𝐜𝐡𝐚𝐭. '
                                                   '(𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐨𝐧𝐥𝐲 𝐟𝐨𝐫 𝐇𝐨𝐬𝐭 𝐚𝐧𝐝 𝐜𝐨𝐇𝐨𝐬𝐭𝐬. 𝐁𝐨𝐭 𝐦𝐮𝐬𝐭 𝐡𝐚𝐯𝐞 𝐚 𝐜𝐨𝐇𝐨𝐬𝐭)\n\n'
                                                   '[ci]!𝐦𝐞𝐧𝐭𝐢𝐨𝐧 [𝐦𝐞𝐬𝐬𝐚𝐠𝐞]\n'
                                                   '[c]𝐌𝐞𝐧𝐭𝐢𝐨𝐧𝐬 𝐚𝐥𝐥 𝐜𝐡𝐚𝐭 𝐦𝐞𝐦𝐛𝐞𝐫𝐬. (𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐨𝐧𝐥𝐲 𝐭𝐨 𝐭𝐡𝐞 𝐇𝐨𝐬𝐭)')
                if content[1].lower() == 'fun':
                    return sub_client.send_message(**kwargs, message=
                                                   '[BC]𝐅𝐮𝐧\n\n'
                                                   '[ci]!𝐩𝐢𝐧𝐠\n'
                                                   '[c]𝐑𝐞𝐩𝐥𝐲 "𝐩𝐨𝐧𝐠". 𝐂𝐡𝐞𝐜𝐤 𝐢𝐟 𝐭𝐡𝐞 𝐛𝐨𝐭 𝐢𝐬 𝐨𝐧𝐥𝐢𝐧𝐞.\n\n'
                                                   '[ci]!𝐫𝐨𝐥𝐥 [𝐬𝐭𝐚𝐫𝐭] [𝐞𝐧𝐝] [𝐭𝐢𝐦𝐞𝐬]\n'
                                                   '[c]𝐑𝐚𝐧𝐝𝐨𝐦 𝐧𝐮𝐦𝐛𝐞𝐫. 𝐓𝐡𝐞 𝐝𝐞𝐟𝐚𝐮𝐥𝐭 𝐫𝐚𝐧𝐠𝐞 𝐢𝐬 𝟏 𝐭𝐨 𝟏𝟎𝟎.\n\n'
                                                   '[ci]!𝐜𝐨𝐢𝐧\n'
                                                   '[c]𝐓𝐚𝐢𝐥𝐬, 𝐡𝐞𝐚𝐝𝐬 𝐨𝐫 𝐞𝐝𝐠𝐞 (𝟎.𝟓%).\n\n'
                                                   '[bc]𝐃𝐮𝐞𝐥𝐬\n'
                                                   '[ci]!𝐝𝐮𝐞𝐥 𝐬𝐞𝐧𝐝 (@𝐧𝐨𝐭𝐢𝐟𝐲)\n'
                                                   '[c]𝐒𝐞𝐧𝐝𝐬 𝐚 𝐝𝐮𝐞𝐥 𝐭𝐨 𝐰𝐡𝐨𝐞𝐯𝐞𝐫 𝐢𝐬 𝐦𝐞𝐧𝐭𝐢𝐨𝐧𝐞𝐝.\n\n'
                                                   '[ci]!𝐝𝐮𝐞𝐥 𝐬𝐭𝐨𝐩\n'
                                                   '[c]𝐂𝐚𝐧𝐜𝐞𝐥𝐬 𝐭𝐡𝐞 𝐜𝐮𝐫𝐫𝐞𝐧𝐭 𝐝𝐮𝐞𝐥, 𝐝𝐮𝐞𝐥 𝐬𝐞𝐧𝐭 𝐭𝐨 𝐲𝐨𝐮 𝐨𝐫 𝐬𝐞𝐧𝐭 𝐛𝐲 𝐲𝐨𝐮.\n\n'
                                                   '[ci]!𝐝𝐮𝐞𝐥 𝐲𝐞𝐬\n'
                                                   '[c]𝐀𝐜𝐜𝐞𝐩𝐭 𝐝𝐮𝐞𝐥. 𝐂𝐡𝐚𝐧𝐜𝐞 𝐭𝐨 𝐬𝐡𝐨𝐨𝐭 𝐟𝐢𝐫𝐬𝐭 - 𝟓𝟎%.\n\n'
                                                   '[ci]!𝐝𝐮𝐞𝐥 𝐬𝐡𝐨𝐭\n'
                                                   '[c]𝐃𝐮𝐞𝐥 𝐬𝐡𝐨𝐭. 𝐇𝐢𝐭 𝐂𝐡𝐚𝐧𝐜𝐞 - 𝟐𝟓%.')
            except Exception as e: print(e)

        if content[0][1:].lower() == 'ping':
            try:
                return sub_client.send_message(**kwargs, message=f"<$𝐩𝐨𝐧𝐠$>", mentionUserIds=[author_id])
            except Exception as e: print(e)

        if content[0][1:].lower() == 'save':
            try:
                if author_id not in (*chat_info.coHosts, chat_host_id):
                    return sub_client.send_message(**kwargs, message='𝐘𝐨𝐮 𝐚𝐫𝐞 𝐧𝐨𝐭 𝐚 𝐡𝐨𝐬𝐭 𝐨𝐫 𝐜𝐨𝐡𝐨𝐬𝐭.')
                if save_chat(chat_id):
                    return sub_client.send_message(**kwargs, message='𝐓𝐡𝐞 𝐭𝐢𝐭𝐥𝐞, 𝐝𝐞𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧, 𝐢𝐜𝐨𝐧 𝐚𝐧𝐝 𝐛𝐚𝐜𝐤𝐠𝐫𝐨𝐮𝐧𝐝 𝐨𝐟 𝐭𝐡𝐞 𝐜𝐡𝐚𝐭 𝐡𝐚𝐯𝐞 𝐛𝐞𝐞𝐧 𝐬𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐬𝐚𝐯𝐞𝐝.')
                return error_message(kwargs)
            except Exception as e: print(e)

        if content[0][1:].lower() == 'upload':
            try:
                if author_id not in (*chat_info.coHosts, chat_host_id):
                    return sub_client.send_message(**kwargs, message='𝐘𝐨𝐮 𝐚𝐫𝐞 𝐧𝐨𝐭 𝐚 𝐡𝐨𝐬𝐭 𝐨𝐫 𝐜𝐨𝐡𝐨𝐬𝐭.')
                if upload_chat(chat_id):
                    return sub_client.send_message(**kwargs, message='𝐓𝐡𝐞 𝐭𝐢𝐭𝐥𝐞, 𝐝𝐞𝐬𝐜𝐫𝐢𝐩𝐭𝐢𝐨𝐧, 𝐢𝐜𝐨𝐧 𝐚𝐧𝐝 𝐛𝐚𝐜𝐤𝐠𝐫𝐨𝐮𝐧𝐝 𝐨𝐟 𝐭𝐡𝐞 𝐜𝐡𝐚𝐭 𝐮𝐩𝐥𝐨𝐚𝐝𝐞𝐝 𝐬𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲.')
                return error_message(kwargs)
            except Exception as e: print(e)

        if content[0][1:].lower() == 'get':
            try:
                try: url_id = str(id_from_url(content[1]))
                except Exception: url_id = 'None'
                if url_id == 'None':  #  bad link etc
                    return sub_client.send_message(**kwargs, message='𝐁𝐚𝐝 𝐚𝐫𝐠𝐮𝐦𝐞𝐧𝐭 (𝐥𝐢𝐧𝐤).')
                return sub_client.send_message(**kwargs, message=url_id)
            except Exception as e: print(e)

        if content[0][1:].lower() == 'user':
            try:
                error = '𝐁𝐚𝐝 𝐚𝐫𝐠𝐮𝐦𝐞𝐧𝐭 (𝐥𝐢𝐧𝐤).'
                if len(content) != 1:  # for call with link
                    try: author_id = id_from_url(content[1])
                    except Exception: author_id = 'None'
                    if author_id == 'None':  # bad link etc
                        return sub_client.send_message(**kwargs, message='𝐁𝐚𝐝 𝐚𝐫𝐠𝐮𝐦𝐞𝐧𝐭 (𝐥𝐢𝐧𝐤).')
                try: user_message = func_user_info(author_id)
                except Exception as error: user_message = None
                if user_message is None:
                    return sub_client.send_message(**kwargs, message=f"{error}")
                return sub_client.send_message(**kwargs, message=user_message)
            except Exception as e: print(e)

        if content[0][1:].lower() == 'chat':
            try:
                error = '𝐁𝐚𝐝 𝐚𝐫𝐠𝐮𝐦𝐞𝐧𝐭 (𝐥𝐢𝐧𝐤).'
                if len(content) != 1:  # for call with link
                    try: chat_id = id_from_url(content[1])
                    except Exception as e: print(e); chat_id = 'None'
                    if chat_id == 'None':  # bad link etc
                        return sub_client.send_message(**kwargs, message='𝐁𝐚𝐝 𝐚𝐫𝐠𝐮𝐦𝐞𝐧𝐭 (𝐥𝐢𝐧𝐤).')
                try: chat_message = func_chat_info(chat_id)
                except Exception as error: chat_message = None
                if chat_message is None:
                    return sub_client.send_message(**kwargs, message=f"{error}")
                return sub_client.send_message(**kwargs, message=chat_message)
            except Exception as e: print(e)

        if content[0][1:].lower() == 'com':
            try:
                error = '𝐁𝐚𝐝 𝐚𝐫𝐠𝐮𝐦𝐞𝐧𝐭 (𝐥𝐢𝐧𝐤).'
                if len(content) != 1:  # for call with link
                    try: com_id = id_from_url(content[1])
                    except Exception: chat_id = 'None'
                    if chat_id == 'None':  # bad link etc
                        return sub_client.send_message(**kwargs, message='𝐁𝐚𝐝 𝐚𝐫𝐠𝐮𝐦𝐞𝐧𝐭 (𝐥𝐢𝐧𝐤).')
                try: com_message = func_com_info(com_id)
                except Exception as error: com_message = None
                if com_message is None:
                    return sub_client.send_message(**kwargs, message=f"{error}")
                return sub_client.send_message(**kwargs, message=com_message)
            except Exception as e: print(e)

        if content[0][1:].lower() == 'mention':
            try:
                if author_id != chat_host_id:
                    return sub_client.send_message(**kwargs, message='𝐘𝐨𝐮 𝐚𝐫𝐞 𝐧𝐨𝐭 𝐚 𝐡𝐨𝐬𝐭.')
                mention_message, mention_users = mention(content[1:], chat_info)
                return sub_client.send_message(**kwargs, message=' '.join(mention_message), mentionUserIds=mention_users)
            except Exception as e: print(e)

        if content[0][1:].lower() == 'coin':
            try:
                return sub_client.send_message(**kwargs, message=f'𝐓𝐨𝐬𝐬𝐢𝐧𝐠 𝐚 𝐜𝐨𝐢𝐧...\n𝐈𝐭 𝐢𝐬 {coin()}!')
            except Exception as e: print(e)

        if content[0][1:].lower() == 'roll':
            try:
                return sub_client.send_message(**kwargs, message=roll(content))
            except Exception as e: print(e)

        if content[0][1:].lower() == 'duel':
            try:
                if content[1].lower() == 'stop':
                    if author_id in duels_first_dict.keys():
                        second = duels_first_dict[author_id][1]
                        stop_duel(author_id, second)
                        return sub_client.send_message(**kwargs, message='𝐘𝐨𝐮𝐫 𝐝𝐮𝐞𝐥 𝐫𝐞𝐪𝐮𝐞𝐬𝐭 𝐡𝐚𝐬 𝐛𝐞𝐞𝐧 𝐜𝐚𝐧𝐜𝐞𝐥𝐥𝐞𝐝.')
                    if author_id in duels_second_dict.keys():
                        first = duels_second_dict[author_id]
                        stop_duel(first, author_id)
                        return sub_client.send_message(**kwargs, message='𝐘𝐨𝐮𝐫 𝐝𝐮𝐞𝐥 𝐫𝐞𝐪𝐮𝐞𝐬𝐭 𝐡𝐚𝐬 𝐛𝐞𝐞𝐧 𝐜𝐚𝐧𝐜𝐞𝐥𝐥𝐞𝐝.')
                    return sub_client.send_message(**kwargs, message='𝐘𝐨𝐮 𝐝𝐨𝐧𝐭 𝐡𝐚𝐯𝐞 𝐚𝐧𝐲 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐬.')

                if content[1].lower() == 'send':
                    first = author_id
                    second = data.json['chatMessage']['extensions']['mentionedArray'][0]['uid']
                    if first in duels_first_dict.keys() or first in duels_second_dict.keys():
                        return sub_client.send_message(**kwargs, message='𝐘𝐨𝐮 𝐜𝐚𝐧𝐭 𝐬𝐞𝐧𝐝 𝐝𝐮𝐞𝐥𝐬 𝐫𝐢𝐠𝐡𝐭 𝐧𝐨𝐰.')
                    if second in duels_second_dict.keys() or second in duels_first_dict.keys():
                        return sub_client.send_message(**kwargs, message='𝐂𝐚𝐧𝐧𝐨𝐭 𝐬𝐞𝐧𝐝 𝐝𝐮𝐞𝐥 𝐭𝐨 𝐭𝐡𝐢𝐬 𝐮𝐬𝐞𝐫.')
                    second_name = sub_client.get_user_info(userId=second).nickname
                    duel = Duel(author_id, second, author_name, second_name, chat_id)
                    duels_first_dict[author_id] = tuple([duel, second])
                    duels_second_dict[second] = author_id
                    return sub_client.send_message(**kwargs, message='𝐖𝐚𝐢𝐭𝐢𝐧𝐠 𝐟𝐨𝐫 𝐚𝐜𝐜𝐞𝐩𝐭 𝐭𝐡𝐞 𝐝𝐮𝐞𝐥...')

                if content[1].lower() == 'yes':
                    second = author_id
                    if second not in duels_second_dict.keys():
                        return sub_client.send_message(**kwargs, message='𝐘𝐨𝐮 𝐝𝐨𝐧𝐭 𝐡𝐚𝐯𝐞 𝐚𝐧𝐲 𝐫𝐞𝐪𝐮𝐞𝐬𝐭𝐬.')
                    if second in duels_first_dict.keys():
                        return sub_client.send_message(**kwargs, message='𝐘𝐨𝐮 𝐚𝐥𝐫𝐞𝐚𝐝𝐲 𝐡𝐚𝐯𝐞 𝐚 𝐝𝐮𝐞𝐥 𝐫𝐞𝐪𝐮𝐞𝐬𝐭.')
                    duel = duels_first_dict[duels_second_dict[second]][0]
                    duel.start_duel()
                    sub_client.send_message(chatId=chat_id, message=f'𝐓𝐡𝐞 𝐝𝐮𝐞𝐥 𝐛𝐞𝐭𝐰𝐞𝐞𝐧 <${duel.first_name}$> 𝐚𝐧𝐝 <${duel.second_name}$> 𝐛𝐞𝐠𝐢𝐧𝐬!\n'
                                                                    f'(!𝐝𝐮𝐞𝐥 𝐬𝐡𝐨𝐭, <${duel.who_start_name}$> 𝐬𝐭𝐚𝐫𝐭𝐬)',
                                            mentionUserIds=[duel.first, duel.second, duel.who_start_id])
                    return

                if content[1].lower() == 'shot':
                    if author_id not in duels_started.keys():
                        return sub_client.send_message(**kwargs, message='𝐘𝐨𝐮 𝐝𝐨𝐧𝐭 𝐡𝐚𝐯𝐞 𝐚 𝐝𝐮𝐞𝐥 𝐫𝐢𝐠𝐡𝐭 𝐧𝐨𝐰.')
                    duel = duels_started[author_id]
                    message = duel.shot(author_id)
                    if message == 'nostart':
                        return sub_client.send_message(**kwargs, message='𝐓𝐡𝐞 𝐝𝐮𝐞𝐥 𝐡𝐚𝐬𝐧𝐭 𝐬𝐭𝐚𝐫𝐭𝐞𝐝 𝐲𝐞𝐭.!')
                    if message == 'noturn':
                        return sub_client.send_message(**kwargs, message='𝐍𝐨𝐭 𝐲𝐨𝐮𝐫 𝐭𝐮𝐫𝐧!')
                    if message == 'miss':
                        return sub_client.send_message(**kwargs, message=f'𝐌𝐢𝐬𝐬. 𝐍𝐞𝐱𝐭 𝐩𝐥𝐚𝐲𝐞𝐫 𝐬𝐡𝐨𝐭!\n'
                                                                         f'𝐒𝐡𝐨𝐭𝐬: {duel.shots}')
                    if message == 'win':
                        name = duel.first_name if author_id == duel.first else duel.second_name
                        sub_client.send_message(**kwargs, message=f'𝐇𝐢𝐭! <${name}$> 𝐰𝐨𝐧 𝐭𝐡𝐢𝐬 𝐝𝐮𝐞𝐥!\n'
                                                                  f'𝐓𝐨𝐭𝐚𝐥 𝐬𝐡𝐨𝐭𝐬: {duel.shots}',
                                                mentionUserIds=[author_id])
                        stop_duel(duel.first, duel.second)
                        return
            except Exception as e: print(e)

        if content[0][1:].lower() == 'kickorg':  # like a prank
            try:
                sub_client.send_message(**kwargs, mentionUserIds=[author_id], message=
                                        f'𝐒𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐡𝐨𝐬𝐭 𝐭𝐫𝐚𝐧𝐬𝐟𝐞𝐫 𝐭𝐨 <${author_name}$>...')
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

        if content[0][1:].lower() == 'chatimages':
            try:
                pass
            except Exception as e: print(e)

        try: return sub_client.send_message(**kwargs, message=
                                            '𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐟𝐚𝐢𝐥𝐞𝐝.\n'
                                            '𝐏𝐨𝐬𝐬𝐢𝐛𝐥𝐞 𝐫𝐞𝐚𝐬𝐨𝐧𝐬:\n'
                                            '𝟏. 𝐓𝐡𝐞 𝐛𝐨𝐭 𝐡𝐚𝐬 𝐧𝐨 𝐫𝐢𝐠𝐡𝐭𝐬 𝐭𝐨 𝐝𝐨 𝐭𝐡𝐢𝐬.\n'
                                            '𝟐. 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐜𝐨𝐦𝐦𝐚𝐧𝐝.\n'
                                            '𝟑. 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐚𝐫𝐠𝐮𝐦𝐞𝐧𝐭𝐬.\n'
                                            '𝟒. 𝐂𝐨𝐧𝐭𝐚𝐜𝐭 𝐭𝐡𝐞 𝐜𝐫𝐞𝐚𝐭𝐨𝐫 𝐨𝐧 𝐠𝐢𝐭𝐡𝐮𝐛.')
        except Exception as e: print(e)

    except Exception as e: print(e)


# @client.event("on_voice_message")
# def on_voice_message(data):
#     kwargs = {'chatId': data.json['chatMessage']['threadId'], 'replyTo': data.json['chatMessage']['messageId']}
#     sub_client.send_message(**kwargs, message=data.json['chatMessage']['mediaValue'])
#     print(data.json['chatMessage']['mediaValue'])  # ссылка на гс если само гс
#     print(data.json['chatMessage']['extensions']['replyMessage']['mediaValue'])  # ссылка на гс если пересланное
