'''
트위치 봇 제작 준비 중
'''



import code
import sys
import irc.bot
import requests
import json
import time
import os

class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel, delay_time):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel
        self.delay_time = delay_time

        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        server = 'irc.chat.twitch.tv'
        port = 6667

        print ('Connecting to ' + server + ' on port ' + str(port) + '...')

        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)
        

    def on_welcome(self, c, e):
        print ('Joining ' + self.channel)

        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        if e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]
            print ('Received command: ' + cmd)
            self.do_command(e, cmd)
        return

    def do_command(self, e, cmd):
        global member, start_member, start_command, command, command_time

        def backup_msg(command, command_time):
            f = open("./command", 'w')
            f.write(json.dumps(command))
            f.close()

            f = open("./command_time", 'w')
            f.write(json.dumps(command_time))
            f.close()                 

        c = self.connection
        channel = self.channel[1:]
        check_mod = e.tags[7]
        check_broad = e.source.split('!')[0]

        #명령어 백업 및 복원
        if cmd == "백업":
            if check_mod['value'] == '1' or check_broad == channel:
                backup_msg(command, command_time)
                message = "[Bot] 명령어 백업 완료"
                c.privmsg(self.channel, message)

        elif cmd == "복원":
            if check_mod['value'] == '1' or check_broad == channel:
                with open("./command") as f:
                        command = json.load(f)
                with open("./command_time") as f:
                        command_time = json.load(f)
                f.close()
                message = "[Bot] 명령어 복원 완료"
                c.privmsg(self.channel, message)

        # 자주 사용하는 기능 예외 처리
        elif cmd == "멤버추가":
            if check_mod['value'] == '1' or check_broad == channel:
                member = e.arguments[0][5:]
                message = "[Bot] 멤버 추가 완료"
                backup_msg(command, command_time)
                c.privmsg(self.channel, message)

        elif cmd == "멤버" and time.time() - start_member > self.delay_time:
            if member == "1":
                message = "[Bot] 혼자 방송 중"
            else:
                message = "[Bot] 멤버 : " + member
            start_member = time.time()
            c.privmsg(self.channel, message)

        elif cmd == "멤버삭제":
            if check_mod['value'] == '1' or check_broad == channel:
                member = "1"
                message = "[Bot] 멤버 삭제 완료"
                backup_msg(command, command_time)
                c.privmsg(self.channel, message)

        elif cmd == "명령어":
            str = e.arguments[0].split(' ')

            # 0 = 명령어
            # 1 = 명령 구분
            # 2 = 명령어 이름
            # 3 = 명령어 내용

            if len(str) == 1 and time.time() - start_command > self.delay_time:
                tmp = "[Bot] 현재 등록된 명령어 : "
                for key in command.keys():
                    tmp += key + ', '
                tmp += '멤버'
                message = tmp
                start_command = time.time()
                c.privmsg(self.channel, message)

            elif len(str) == 3:
                if str[1] == "삭제":
                    if check_mod['value'] == '1' or check_broad == channel:
                        if str[2] == '멤버':
                            message = "[Bot] '" + str[2] + "' 명령어는 해당 명령어로 삭제될 수 없습니다."
                        elif str[2] in command:
                            del command[str[2]]
                            del command_time[str[2]]
                            message = "[Bot] 명령어 '" + str[2] + "' 삭제 완료"
                            backup_msg(command, command_time)
                            c.privmsg(self.channel, message)                              
                        else:
                            message = "[Bot] '" + str[2] + "'에 해당하는 명령어가 없습니다."
                            c.privmsg(self.channel, message)

            elif len(str) >= 4:
                if str[1] == "추가":
                    if check_mod['value'] == '1' or check_broad == channel:
                        if str[2] == "멤버":
                            message = "[Bot] '" + str[2] + "' 명령어는 해당 명령어로 추기할 수 없습니다."
                            c.privmsg(self.channel, message)
                        else:    
                            if str[2] in command:
                                del command[str[2]]
                            for i in range(4,len(str)):
                                str[3] = str[3] + " " + str[i]
                            command[str[2]] = str[3]
                            message = "[Bot] 명령어 '" + str[2] + "' 추가 완료"
                            command_time[str[2]] = time.time()
                            backup_msg(command, command_time)
                            c.privmsg(self.channel, message)

        elif cmd in command and time.time() - command_time[cmd] > self.delay_time:
            if cmd != '멤버':
                message = "[Bot] "+cmd+" : "+command[cmd]
                command_time[cmd] = time.time()
                c.privmsg(self.channel, message)

def main():
    username  = "AMANSA BOT"
    client_id = code.twitchid
    token     = code.twitchcode
    channel = "Han_MangUl"
    delay_time = 20

    bot = TwitchBot(username, client_id, token, channel, delay_time)
    bot.start()

if __name__ == "__main__":
    main()