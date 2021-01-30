#Bot Settings
VERSION = "0.0.0"
EXTENSION_LIST = ["extensions.admin", "extensions.events", "extensions.etc","extensions.moderation","extensions.util"]
COMMAND_PREFIXS = ["=", "ㅇㅇ아"]
BOT_STATUS = ["=도움말을 입력해보세요!", "{server_count}서버 | {user_count}유저 ", "LeoBot-v2: {version}"]

#Bot Settings
BOT_TOKEN = "YOUR BOT TOKEN"
BOT_INTENT_MEMBERS = True
BOT_INTENT_PRESENCES = True

#DB Settings
MONGO_DB_HOST = "example.com" #example.com
MONGO_DB_USERNAME = "root"  #root
MONGO_DB_PASSWORD = "MyPassWord123!"  #MyPassWord123!
MONGO_DB_PORT = 27017  #27017

#External Services Credential
KOREAN_BOTS_TOKEN = "YOUR KOREANBOTS.DEV TOKEN"

#Master Server Setting
YES_EMOJI_STRING = "<a:yes:your_emoji_code>"
NO_EMOJI_STRING = "<a:x_:your_emoji_code>"

YES_EMOJI_INT = int(YES_EMOJI_STRING[-19:-1])
NO_EMOJI_INT = int(NO_EMOJI_STRING[-19:-1])

#Discord Support Server Settings
ERROR_LOG_CHANNEL = 12345677848484848
SERVER_LOG_CHANNEL = 98765434342424243