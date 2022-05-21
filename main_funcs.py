import time
import aminofix as amino
import random as rnd
from db import *


client = amino.Client(socketDebugging=False)
client.login(email=EMAIL, password=PASSWORD)  # check db.py
sub_client = amino.SubClient(comId=CID, profile=client.profile)


duels_first_dict = dict()  # userId who invited : Duel Object
duels_second_dict = dict()  # userId who was invited : userId who invited
duels_started = dict()   # userIds who is currently dueling : Duel Object
report_ids = list()  # userIds who send !report without text


class Duel:
    def __init__(self, first, second, f_name, s_name, chat_id):  # ids
        self.first = first
        self.second = second
        self.chat_id = chat_id
        self.first_name = f_name
        self.second_name = s_name
        self.shots = 0
        self.start = False
        if rnd.randint(0, 1) == 0:
            self.who_start_name = f_name
            self.who_start_id = first
        else:
            self.who_start_name = s_name
            self.who_start_id = second

    def start_duel(self):
        duels_started[self.first], duels_started[self.second] = self, self
        self.start = True

    def shot(self, user_id):
        if not self.start:
            return 'nostart'
        if user_id == self.who_start_id:
            if self.shots % 2 == 0:
                self.shots += 1
                return rnd.choices(('win', 'miss'), weights=(25, 75))[0]
            return 'noturn'
        if self.shots % 2 == 1:
            self.shots += 1
            return rnd.choices(('win', 'miss'), weights=(25, 75))[0]
        return 'noturn'


def stop_duel(first, second):
    del duels_first_dict[first]
    del duels_second_dict[second]
    try:
        del duels_started[first]
        del duels_started[second]
    except Exception: pass


def console_log(msg_time, chat_name, author_name, msg_content):
    print(f'{msg_time.split("T")[1][:-1]}  |  {chat_name}  |  {author_name}:  {msg_content}')


def id_from_url(url):
    url = url[:-1] if url[-1] == '/' else url
    try:
        var = client.get_from_code(url)
        if var.objectId is not None: return var.objectId
        else: return var.json['extensions']['community']['ndcId']
    except Exception: return 'None'


def url_from_id(objectId: str, objectType: int, comId=None):
    # ObjectType. 0 - user, 12 - chat
    # if comId is None - check global, else - check in community. comId is str
    shortUrl = None
    if objectType is None or objectId is None: raise TypeError('objectId or objectType is None')
    if comId is not None:
        if objectType == 0:  # user
            shortUrl = client.get_from_id(objectId=objectId, objectType=objectType, comId=comId).json['extensions']['linkInfo']['shareURLShortCode']
    else:
        if objectType == 0:  # user
            shortUrl = client.get_from_id(objectId=objectId, objectType=objectType).json['extensions']['linkInfo']['shareURLShortCode']
    return shortUrl


def save_chat(chat_id: str):  # Save chat info in database.db
    chat = sub_client.get_chat_thread(chat_id)
    chat_id, chat_name, chat_icon, chat_bg, chat_desc = chat.chatId, chat.title, chat.icon, chat.backgroundImage, chat.content
    if save_chat_in_db(chat_id, chat_name, chat_icon, chat_bg, chat_desc): return True
    return False


def upload_chat(chat_id: str):
    materials = return_chat_info_from_db(chat_id)
    if materials is None: return False
    title, icon, bg, desc = materials[1:]
    sub_client.edit_chat(chatId=chat_id, title=title, icon=icon, content=desc)
    try: sub_client.edit_chat(chatId=chat_id, backgroundImage=bg)  # There is always an error when updating the background
    except Exception: pass
    return True


def error_message(kwargs):
    sub_client.send_message(**kwargs, message='The command failed, an error occurred. Contact the creator on github or person who hosts the bot for help.')


def func_user_info(user_id: str):  # for other info check info_user.json or objects.py
    info_user_com = sub_client.get_user_info(userId=user_id)
    info_user_amino = client.get_user_info(userId=user_id)
    try: user_name = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_user_com.nickname is None else info_user_com.nickname
    except Exception: user_name = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: user_global_url = '𝐍𝐨 𝐢𝐧𝐟𝐨' if url_from_id(user_id, 0) is None else url_from_id(user_id, 0)
    except Exception: user_global_url = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: user_created = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_user_amino.createdTime is None else ' '.join(info_user_amino.createdTime[:-1].split('T'))
    except Exception: user_created = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try : user_join_com = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_user_com.createdTime is None else ' '.join(info_user_com.createdTime[:-1].split('T'))
    except Exception: user_join_com = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: user_modified = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_user_com.modifiedTime is None else ' '.join(info_user_com.modifiedTime[:-1].split('T'))
    except Exception: user_modified = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: user_level = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_user_com.level is None else info_user_com.level
    except Exception: user_level = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: user_reputation = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_user_com.reputation is None else info_user_com.reputation
    except Exception: user_reputation = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: user_followers = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_user_com.followersCount is None else info_user_com.followersCount
    except Exception: user_followers = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: user_following = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_user_com.followingCount is None else info_user_com.followingCount
    except Exception: user_following = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: user_comments = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_user_com.commentsCount is None else info_user_com.commentsCount
    except Exception: user_comments = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: user_posts = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_user_com.postsCount is None else info_user_com.postsCount
    except Exception: user_posts = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: user_blogs = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_user_com.blogsCount is None else info_user_com.blogsCount
    except Exception: user_blogs = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: user_statiy = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_user_com.itemsCount is None else info_user_com.itemsCount
    except Exception: user_statiy = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: user_stories = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_user_com.storiesCount is None else info_user_com.storiesCount
    except Exception: user_stories = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: user_titles = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_user_com.json['extensions']['customTitles'] is None else len(info_user_com.json['extensions']['customTitles'])
    except Exception: user_titles = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: user_online = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_user_com.onlineStatus is None else info_user_com.onlineStatus
    except Exception: user_online = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    user_message = '\n'.join([
        f'𝐍𝐢𝐜𝐤𝐧𝐚𝐦𝐞: {user_name}',
        f'𝐆𝐥𝐨𝐛𝐚𝐥 𝐩𝐫𝐨𝐟𝐢𝐥𝐞: {user_global_url}',
        f'𝐀𝐜𝐜𝐨𝐮𝐧𝐭 𝐜𝐫𝐞𝐚𝐭𝐞𝐝: {user_created}',
        f'𝐉𝐨𝐢𝐧𝐞𝐝 𝐭𝐨 𝐜𝐨𝐦𝐦𝐮𝐧𝐢𝐭𝐲: {user_join_com}',
        f'𝐏𝐫𝐨𝐟𝐢𝐥𝐞 𝐜𝐡𝐚𝐧𝐠𝐞: {user_modified}',
        f'𝐋𝐞𝐯𝐞𝐥 𝐚𝐧𝐝 𝐫𝐞𝐩𝐮𝐭𝐚𝐭𝐢𝐨𝐧: {user_level}, {user_reputation}',
        f'𝐒𝐮𝐛𝐜𝐫𝐢𝐛𝐞𝐫𝐬: {user_followers}',
        f'𝐅𝐨𝐥𝐥𝐨𝐰𝐢𝐧𝐠: {user_following}',
        f'𝐂𝐨𝐦𝐦𝐞𝐧𝐭𝐬: {user_comments}',
        f'𝐏𝐨𝐬𝐭𝐬: {user_posts}',
        f'𝐀𝐫𝐭𝐢𝐜𝐥𝐞𝐬, 𝐛𝐥𝐨𝐠𝐬, 𝐬𝐭𝐨𝐫𝐢𝐞𝐬: {user_statiy}, {user_blogs}, {user_stories}',
        f'𝐓𝐢𝐭𝐥𝐞𝐬: {user_titles}',
        f'𝐎𝐧𝐥𝐢𝐧𝐞 𝐬𝐭𝐚𝐭𝐮𝐬: {"𝐎𝐧𝐥𝐢𝐧𝐞" if user_online == 1 else "𝐎𝐟𝐟𝐥𝐢𝐧𝐞"}'
        ])
    return user_message


def func_chat_info(chat_id: str):
    info_chat = sub_client.get_chat_thread(chatId=chat_id)
    try: chat_title = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_chat.title is None else info_chat.title
    except Exception: chat_title = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: chat_url = client.get_from_id(objectId=info_chat.chatId, objectType=12, comId=info_chat.comId).shortUrl
    except Exception: chat_url = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: chat_author_id = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_chat.creatorId is None else info_chat.creatorId
    except Exception: chat_author_id = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: chat_host_com_url = client.get_from_id(chat_author_id, 0, comId=info_chat.comId).shortUrl
    except Exception: chat_host_com_url = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: chat_host_global_url = client.get_from_id(chat_author_id, 0).shortUrl
    except Exception: chat_host_global_url = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: chat_language = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_chat.language is None else info_chat.language.upper()
    except Exception: chat_language = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: chat_created = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_chat.createdTime is None else ' '.join(info_chat.createdTime[:-1].split('T'))
    except Exception: chat_created = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: chat_users = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_chat.membersCount is None else info_chat.membersCount
    except Exception: chat_users = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: chat_coHosts = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_chat.coHosts is None else len(info_chat.coHosts)
    except Exception: chat_coHosts = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: chat_bannedUsers = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_chat.bannedUsers is None else len(info_chat.bannedUsers)
    except Exception: chat_bannedUsers = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: chat_lastActivity = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_chat.latestActivityTime is None else ' '.join(info_chat.latestActivityTime[:-1].split('T'))
    except Exception: chat_lastActivity = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: chat_tippedCoins = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_chat.json['tipInfo']['tippedCoins'] is None else int(info_chat.json['tipInfo']['tippedCoins'])
    except Exception: chat_tippedCoins = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: chat_tippers = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_chat.json['tipInfo']['tippersCount'] is None else info_chat.json['tipInfo']['tippersCount']
    except Exception: chat_tippers = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: chat_keywords = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_chat.json['keywords'] is None else info_chat.json['keywords']
    except Exception: chat_keywords = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    chat_message = '\n'.join([
        f'𝐂𝐡𝐚𝐭 𝐭𝐢𝐭𝐥𝐞: {chat_title}',
        f'𝐋𝐢𝐧𝐤: {chat_url}',
        f"𝐂𝐡𝐚𝐭'𝐬 𝐡𝐨𝐬𝐭: {chat_host_com_url}, {chat_host_global_url}",
        f'𝐂𝐡𝐚𝐭 𝐜𝐫𝐞𝐚𝐭𝐞𝐝: {chat_created}',
        f'𝐂𝐡𝐚𝐭 𝐥𝐚𝐧𝐠: {chat_language}',
        f'𝐌𝐞𝐦𝐛𝐞𝐫𝐬: {chat_users}',
        f'𝐂𝐨𝐇𝐨𝐬𝐭𝐬: {chat_coHosts}',
        f'𝐁𝐚𝐧𝐧𝐞𝐝: {chat_bannedUsers}',
        f'𝐓𝐢𝐩𝐩𝐞𝐫𝐬: {chat_tippers}',
        f'𝐓𝐢𝐩𝐩𝐞𝐝 𝐜𝐨𝐢𝐧𝐬: {chat_tippedCoins}',
        f'𝐊𝐞𝐲𝐰𝐨𝐫𝐝𝐬: {chat_keywords}',
        f'𝐋𝐚𝐬𝐭 𝐚𝐜𝐭𝐢𝐯𝐢𝐭𝐲: {chat_lastActivity}'
        ])
    return chat_message


def func_com_info(com_id: str):
    if int(com_id) not in list(client.sub_clients(start=0, size=100).comId):
        client.join_community(comId=com_id)
    info_com = client.get_community_info(com_id)
    sub_client_for_com = amino.SubClient(comId=com_id, profile=client.profile)
    try: com_link = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_com.link is None else info_com.link
    except Exception: com_link = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: com_name = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_com.name is None else info_com.name
    except Exception: com_name = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: com_createdTimed = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_com.createdTime is None else ' '.join(info_com.createdTime[:-1].split('T'))
    except Exception: com_createdTimed = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: com_comId = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_com.comId is None else info_com.comId
    except Exception: com_comId = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: com_searchable = False if info_com.searchable is None else info_com.searchable
    except Exception: com_searchable = False
    try: com_welcomeMessageEnabled = False if info_com.welcomeMessageEnabled is None else info_com.welcomeMessageEnabled
    except Exception: com_welcomeMessageEnabled = False
    try: com_invitePermission = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_com.json['configuration']['general']['invitePermission'] is None else info_com.json['configuration']['general']['invitePermission']
    except Exception: com_invitePermission = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: com_membersCount = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_com.usersCount is None else info_com.usersCount
    except Exception: com_membersCount = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: com_onlineCount = sub_client_for_com.get_online_users().userProfileCount
    except Exception: com_onlineCount = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: com_adminsCount = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_com.json['communityHeadList'] is None else len(info_com.json['communityHeadList'])
    except Exception: com_adminsCount = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: com_primaryLanguage = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_com.primaryLanguage is None else info_com.primaryLanguage.upper()
    except Exception: com_primaryLanguage = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: com_agent_name = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_com.agent.nickname is None else info_com.agent.nickname
    except Exception: com_agent_name = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: com_agent_id = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_com.agent.userId is None else info_com.agent.userId
    except Exception: com_agent_id = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: com_agent_global_url = '𝐍𝐨 𝐢𝐧𝐟𝐨' if url_from_id(com_agent_id, 0) is None else url_from_id(com_agent_id, 0)
    except Exception: com_agent_global_url = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    # try: com_rankingTable = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_com.rankingTable.title is None else ', '.join(info_com.rankingTable.title)
    # except Exception: com_rankingTable = '𝐍𝐨 𝐢𝐧𝐟𝐨'
    try: com_keywords = '𝐍𝐨 𝐢𝐧𝐟𝐨' if info_com.keywords is None else ', '.join(info_com.keywords.split(','))
    except Exception: com_keywords = '𝐍𝐨 𝐢𝐧𝐟𝐨'

    if com_invitePermission == 1:
        com_invitePermission = '𝐄𝐯𝐞𝐫𝐲𝐨𝐧𝐞 𝐜𝐚𝐧 𝐣𝐨𝐢𝐧'
    elif com_invitePermission == 2:
        com_invitePermission = '𝐁𝐲 𝐚𝐩𝐩𝐥𝐢𝐜𝐚𝐭𝐢𝐨𝐧'
    elif com_invitePermission == 3:
        com_invitePermission = '𝐁𝐲 𝐢𝐧𝐯𝐢𝐭𝐚𝐭𝐢𝐨𝐧'

    com_message = '\n'.join([
        f'𝐋𝐢𝐧𝐤: {com_link}',
        f'𝐂𝐨𝐦𝐦𝐮𝐧𝐢𝐭𝐲 𝐭𝐢𝐭𝐥𝐞: {com_name}',
        f'𝐂𝐫𝐞𝐚𝐭𝐞𝐝: {com_createdTimed}',
        f'𝐂𝐨𝐦𝐈𝐝: {com_comId}',
        f'𝐒𝐞𝐚𝐫𝐜𝐡𝐚𝐛𝐥𝐞: {"𝐘𝐞𝐬" if com_searchable else "𝐍𝐨"}',
        f'𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐦𝐞𝐬𝐬𝐚𝐠𝐞: {"𝐄𝐧𝐚𝐛𝐥𝐞" if com_welcomeMessageEnabled else "𝐃𝐢𝐬𝐚𝐛𝐥𝐞"}',
        f'𝐈𝐧𝐯𝐢𝐭𝐞 𝐩𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧: {com_invitePermission}',
        f'𝐓𝐨𝐭𝐚𝐥 𝐦𝐞𝐦𝐛𝐞𝐫𝐬: {com_membersCount}',
        f'𝐎𝐧𝐥𝐢𝐧𝐞 𝐦𝐞𝐦𝐛𝐞𝐫𝐬: {com_onlineCount}',
        f'𝐀𝐝𝐦𝐢𝐧𝐬: {com_adminsCount}',
        f'𝐋𝐚𝐧𝐠𝐮𝐚𝐠𝐞: {com_primaryLanguage}',
        f"𝐀𝐠𝐞𝐧𝐭'𝐬 𝐧𝐚𝐦𝐞: {com_agent_name}",
        f"𝐀𝐠𝐞𝐧𝐭'𝐬 𝐠𝐥𝐨𝐛𝐚𝐥 𝐩𝐫𝐨𝐟𝐢𝐥𝐞: {com_agent_global_url}",
        # f'𝐑𝐚𝐧𝐤𝐢𝐧𝐠 𝐭𝐚𝐛𝐥𝐞: {com_rankingTable}',
        f'𝐊𝐞𝐲𝐰𝐨𝐫𝐝𝐬: {com_keywords}'
    ])
    return com_message


def mention(message: str, chat_info):
    chat_id = chat_info.chatId
    if not message: message = 'Notify!\n'
    else: message = ' '.join(message) + '\n'
    chat_members = chat_info.membersCount - (chat_info.membersCount % 100 - 1)
    mention_ids = []
    for i in range(0, chat_members):
        mention_ids.extend(sub_client.get_chat_users(chatId=chat_id, start=i, size=100).userId)
    message_mention = [message] + [f'<${i}$>' for i in range(chat_info.membersCount)]
    return message_mention, mention_ids


def coin():  # useless func xd
    return rnd.choices(['heads', 'tails', 'edge'], weights=[49.75, 49.75, 0.50])[0]
    # from collections import Counter
    # print(Counter(rnd.choices(['heads', 'tails', 'edge'], weights=[49.75, 49.75, 0.50])[0] for _ in range(1000000)))
    # ~ Counter({'решка': 497835, 'орёл': 497274, 'ребро': 4891})


def roll(content: str):
    # if content[1] == 'test':
    #     return f"🎲 1, 2, 3, 4, 5, 6 (1, 6)"
    content = list(map(int, content[1:]))
    if len(content) == 0:
        return f"🎲 {rnd.randint(1, 100)} (1, 100)"
    if len(content) == 1:
        return f"🎲 {rnd.randint(1, content[0])} (1, {content[0]})"
    if len(content) == 2:
        return f"🎲 {rnd.randint(content[0], content[1])} ({content[0]}, {content[1]})"
    if len(content) == 3:
        rolls = [str(rnd.randint(content[0], content[1])) for _ in range(content[2])]
        return f"🎲 {', '.join(rolls)} ({content[0]}, {content[1]})"
    raise ValueError


def report(content, user_id, com_id, chat_id, msg_time):
    try: user_link = client.get_from_id(user_id, 0, comId=com_id).shortUrl
    except Exception: user_link = '-'
    try: chat_link = client.get_from_id(chat_id, 12, comId=com_id).shortUrl
    except Exception: chat_link = '-'
    message = f'Report from {user_link}\nChat: {chat_link}\nUTC Time: {" ".join(msg_time[:-1].split("T"))}\nMessage: {" ".join(content)}'
    return message



