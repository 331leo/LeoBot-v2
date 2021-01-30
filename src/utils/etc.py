import random
import string

colormap = {
    "aqua": 0x00f1ff,
    "hotpink": 0xFF69B4,
    "yellowgreen": 0xADFF2F,
    "red": 0xff0000,
    "purple": 0x800080,
    "skyblue": 0xadd8e6,
    "lightgreen": 0x90ee90,
    "lightpink": 0xffc0cb,
    "yellow": 0xfcf794
}

discord_perms = {
    #GUILD_PERMS
    "kick_members": "멤버 추방하기",
    "ban_members": "멤버 차단하기",
    "administrator": "관리자",
    "manage_guild": "서버 관리하기",
    "view_audit_log": "감사 로그 보기",
    "view_guild_insights": "서버 인사이트 확인하기",
    "change_nickname": "별명 변경하기",
    "manage_nicknames": "별명 관리하기",
    "manage_roles": "역할 관리하기",
    "manage_emojis": "이모티콘 관리",

    #GENERAL_PERMS
    "create_instant_invite": "초대 코드 만들기",
    "manage_channels": "채널 관리하기",
    "manage_roles": "권한 관리하기",
    "manage_webhooks": "웹후크 관리하기",

    #TEXT_PERMS
    "read_messages": "메시지 읽기",
    "send_messages": "메시지 보내기",
    "send_tts_messages": "TTS 메시지 보내기",
    "manage_messages": "메시지 관리하기",
    "embed_links": "링크 첨부",
    "attach_files": "파일 첨부",
    "read_message_history": "메시지 기록 보기",
    "mention_everyone": "everyone, here, 모든 역할 멘션하기",
    "external_emojis": "외부 이모티콘 사용하기",
    "add_reactions": "반응 추가하기",

    #VOICE_PERMS 
    "priority_speaker": "우선 발언권",
    "stream": "동영상",
    "connect": "연결",
    "speak": "말하기",
    "mute_members": "멤버들의 마이크 음소거하기",
    "deafen_members": "멤버의 헤드셋 음소거하기",
    "move_members": "멤버 이동",
    "use_voice_activation": "음성 감지 사용",
}

def random_string(length):
    pool = string.ascii_lowercase + string.digits
    return ''.join(random.choice(pool) for i in range(length))

