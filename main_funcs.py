import time
import aminofix as amino
import random as rnd
from db import *


client = amino.Client()
client.login(email=EMAIL, password=PASSWORD)  # check db.py


duels_first_dict = dict()  # userId who invited : Duel Object
duels_second_dict = dict()  # userId who was invited : userId who invited
duels_started = dict()   # userIds who is currently dueling : Duel Object


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


# def console_log(msg_time, chat_name, author_name, msg_content):
#     print(f'{msg_time.split("T")[1][:-1]}  |  {chat_name}  |  {author_name}:  {msg_content}')


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


def save_chat(chat_id, sub_client):  # Save chat info in database.db
    chat = sub_client.get_chat_thread(chat_id)
    chat_id, chat_name, chat_icon, chat_bg, chat_desc = chat.chatId, chat.title, chat.icon, chat.backgroundImage, chat.content
    if save_chat_in_db(chat_id, chat_name, chat_icon, chat_bg, chat_desc): return True
    return False


def upload_chat(chat_id, sub_client):
    materials = return_chat_info_from_db(chat_id)
    if materials is None: return False
    title, icon, bg, desc = materials[1:]
    sub_client.edit_chat(chatId=chat_id, title=title, icon=icon, content=desc)
    try: sub_client.edit_chat(chatId=chat_id, backgroundImage=bg)  # There is always an error when updating the background
    except Exception: pass
    return True


def error_message(kwargs, sub_client):
    sub_client.send_message(**kwargs, message='The command failed, an error occurred. Contact the creator on github or person who hosts the bot for help.')


def func_user_info(user_id, sub_client):  # for other info check info_user.json or objects.py
    info_user_com = sub_client.get_user_info(userId=user_id)
    info_user_amino = client.get_user_info(userId=user_id)
    try: user_name = 'No info' if info_user_com.nickname is None else info_user_com.nickname
    except Exception: user_name = 'No info'
    try: user_global_url = 'No info' if url_from_id(user_id, 0) is None else url_from_id(user_id, 0)
    except Exception: user_global_url = 'No info'
    try: user_created = 'No info' if info_user_amino.createdTime is None else ' '.join(info_user_amino.createdTime[:-1].split('T'))
    except Exception: user_created = 'No info'
    try: user_join_com = 'No info' if info_user_com.createdTime is None else ' '.join(info_user_com.createdTime[:-1].split('T'))
    except Exception: user_join_com = 'No info'
    try: user_modified = 'No info' if info_user_com.modifiedTime is None else ' '.join(info_user_com.modifiedTime[:-1].split('T'))
    except Exception: user_modified = 'No info'
    try: user_level = 'No info' if info_user_com.level is None else info_user_com.level
    except Exception: user_level = 'No info'
    try: user_reputation = 'No info' if info_user_com.reputation is None else info_user_com.reputation
    except Exception: user_reputation = 'No info'
    try: user_followers = 'No info' if info_user_com.followersCount is None else info_user_com.followersCount
    except Exception: user_followers = 'No info'
    try: user_following = 'No info' if info_user_com.followingCount is None else info_user_com.followingCount
    except Exception: user_following = 'No info'
    try: user_comments = 'No info' if info_user_com.commentsCount is None else info_user_com.commentsCount
    except Exception: user_comments = 'No info'
    try: user_posts = 'No info' if info_user_com.postsCount is None else info_user_com.postsCount
    except Exception: user_posts = 'No info'
    try: user_blogs = 'No info' if info_user_com.blogsCount is None else info_user_com.blogsCount
    except Exception: user_blogs = 'No info'
    try: user_statiy = 'No info' if info_user_com.itemsCount is None else info_user_com.itemsCount
    except Exception: user_statiy = 'No info'
    try: user_stories = 'No info' if info_user_com.storiesCount is None else info_user_com.storiesCount
    except Exception: user_stories = 'No info'
    try: user_titles = 'No info' if info_user_com.json['extensions']['customTitles'] is None else len(info_user_com.json['extensions']['customTitles'])
    except Exception: user_titles = 'No info'
    try: user_online = 'No info' if info_user_com.onlineStatus is None else info_user_com.onlineStatus
    except Exception: user_online = 'No info'
    user_message = '\n'.join([
        f'Nickname: {user_name}',
        f'Global profile: {user_global_url}',
        f'Account created: {user_created}',
        f'Joined to community: {user_join_com}',
        f'Profile change: {user_modified}',
        f'Level and reputation: {user_level}, {user_reputation}',
        f'Followers: {user_followers}',
        f'Following: {user_following}',
        f'Comments: {user_comments}',
        f'Posts: {user_posts}',
        f'Articles, blogs, stories: {user_statiy}, {user_blogs}, {user_stories}',
        f'Titles: {user_titles}',
        f'Online status: {"Online" if user_online == 1 else "Offline"}'
        ])
    return user_message


def func_chat_info(chat_id, sub_client):
    info_chat = sub_client.get_chat_thread(chatId=chat_id)
    try: chat_title = 'No info' if info_chat.title is None else info_chat.title
    except Exception: chat_title = 'No info'
    try: chat_url = client.get_from_id(objectId=info_chat.chatId, objectType=12, comId=info_chat.comId).shortUrl
    except Exception: chat_url = 'No info'
    try: chat_author_id = 'No info' if info_chat.creatorId is None else info_chat.creatorId
    except Exception: chat_author_id = 'No info'
    try: chat_host_com_url = client.get_from_id(chat_author_id, 0, comId=info_chat.comId).shortUrl
    except Exception: chat_host_com_url = 'No info'
    try: chat_host_global_url = client.get_from_id(chat_author_id, 0).shortUrl
    except Exception: chat_host_global_url = 'No info'
    try: chat_language = 'No info' if info_chat.language is None else info_chat.language.upper()
    except Exception: chat_language = 'No info'
    try: chat_created = 'No info' if info_chat.createdTime is None else ' '.join(info_chat.createdTime[:-1].split('T'))
    except Exception: chat_created = 'No info'
    try: chat_users = 'No info' if info_chat.membersCount is None else info_chat.membersCount
    except Exception: chat_users = 'No info'
    try: chat_coHosts = 'No info' if info_chat.coHosts is None else len(info_chat.coHosts)
    except Exception: chat_coHosts = 'No info'
    try: chat_bannedUsers = 'No info' if info_chat.bannedUsers is None else len(info_chat.bannedUsers)
    except Exception: chat_bannedUsers = 'No info'
    try: chat_lastActivity = 'No info' if info_chat.latestActivityTime is None else ' '.join(info_chat.latestActivityTime[:-1].split('T'))
    except Exception: chat_lastActivity = 'No info'
    try: chat_tippedCoins = 'No info' if info_chat.json['tipInfo']['tippedCoins'] is None else int(info_chat.json['tipInfo']['tippedCoins'])
    except Exception: chat_tippedCoins = 'No info'
    try: chat_tippers = 'No info' if info_chat.json['tipInfo']['tippersCount'] is None else info_chat.json['tipInfo']['tippersCount']
    except Exception: chat_tippers = 'No info'
    try: chat_keywords = 'No info' if info_chat.json['keywords'] is None else info_chat.json['keywords']
    except Exception: chat_keywords = 'No info'
    chat_message = '\n'.join([
        f'Chat title: {chat_title}',
        f'Link: {chat_url}',
        f"Chat's host: {chat_host_com_url}, {chat_host_global_url}",
        f'Chat created: {chat_created}',
        f'Chat lang: {chat_language}',
        f'Members: {chat_users}',
        f'CoHosts: {chat_coHosts}',
        f'Banned: {chat_bannedUsers}',
        f'Tippers: {chat_tippers}',
        f'Tipped coins: {chat_tippedCoins}',
        f'Keywords: {chat_keywords}',
        f'Last activity: {chat_lastActivity}'
        ])
    return chat_message


def func_com_info(com_id):
    if int(com_id) not in list(client.sub_clients(start=0, size=100).comId):
        client.join_community(comId=com_id)
    info_com = client.get_community_info(com_id)
    sub_client_for_com = amino.SubClient(comId=com_id, profile=client.profile)
    try: com_link = 'No info' if info_com.link is None else info_com.link
    except Exception: com_link = 'No info'
    try: com_name = 'No info' if info_com.name is None else info_com.name
    except Exception: com_name = 'No info'
    try: com_createdTimed = 'No info' if info_com.createdTime is None else ' '.join(info_com.createdTime[:-1].split('T'))
    except Exception: com_createdTimed = 'No info'
    try: com_comId = 'No info' if info_com.comId is None else info_com.comId
    except Exception: com_comId = 'No info'
    try: com_searchable = False if info_com.searchable is None else info_com.searchable
    except Exception: com_searchable = False
    try: com_welcomeMessageEnabled = False if info_com.welcomeMessageEnabled is None else info_com.welcomeMessageEnabled
    except Exception: com_welcomeMessageEnabled = False
    try: com_invitePermission = 'No info' if info_com.json['configuration']['general']['invitePermission'] is None else info_com.json['configuration']['general']['invitePermission']
    except Exception: com_invitePermission = 'No info'
    try: com_membersCount = 'No info' if info_com.usersCount is None else info_com.usersCount
    except Exception: com_membersCount = 'No info'
    try: com_onlineCount = sub_client_for_com.get_online_users().userProfileCount
    except Exception: com_onlineCount = 'No info'
    try: com_adminsCount = 'No info' if info_com.json['communityHeadList'] is None else len(info_com.json['communityHeadList'])
    except Exception: com_adminsCount = 'No info'
    try: com_primaryLanguage = 'No info' if info_com.primaryLanguage is None else info_com.primaryLanguage.upper()
    except Exception: com_primaryLanguage = 'No info'
    try: com_agent_name = 'No info' if info_com.agent.nickname is None else info_com.agent.nickname
    except Exception: com_agent_name = 'No info'
    try: com_agent_id = 'No info' if info_com.agent.userId is None else info_com.agent.userId
    except Exception: com_agent_id = 'No info'
    try: com_agent_global_url = 'No info' if url_from_id(com_agent_id, 0) is None else url_from_id(com_agent_id, 0)
    except Exception: com_agent_global_url = 'No info'
    # try: com_rankingTable = 'No info' if info_com.rankingTable.title is None else ', '.join(info_com.rankingTable.title)
    # except Exception: com_rankingTable = 'No info'
    try: com_keywords = 'No info' if info_com.keywords is None else ', '.join(info_com.keywords.split(','))
    except Exception: com_keywords = 'No info'

    if com_invitePermission == 1:
        com_invitePermission = 'Everyone can join'
    elif com_invitePermission == 2:
        com_invitePermission = 'By application'
    elif com_invitePermission == 3:
        com_invitePermission = 'By invitation'

    com_message = '\n'.join([
        f'Link: {com_link}',
        f'Community title: {com_name}',
        f'Created: {com_createdTimed}',
        f'ComId: {com_comId}',
        f'Searchable: {"Yes" if com_searchable else "No"}',
        f'Welcome message: {"Enable" if com_welcomeMessageEnabled else "Disable"}',
        f'Invite permission: {com_invitePermission}',
        f'Total members: {com_membersCount}',
        f'Online members: {com_onlineCount}',
        f'Admins: {com_adminsCount}',
        f'Language: {com_primaryLanguage}',
        f"Agent's name: {com_agent_name}",
        f"Agent's global profile: {com_agent_global_url}",
        # f'Ranking table: {com_rankingTable}',
        f'Keywords: {com_keywords}'
    ])
    return com_message


def mention(message, chat_info, sub_client):
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
    # ~ Counter({'heads': 497835, 'tails': 497274, 'edge': 4891})


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
