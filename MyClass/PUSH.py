import telebot
from urllib import request


class Push:
    METHOD = dict({})
    METHOD['serverchan'] = "http://sc.ftqq.com/"
    METHOD['bark'] = "https://api.day.app/"
    
    def server_chan(self, key, text="", desp=""):
        
        text = text.replace(' ', '%20')
        desp = desp.replace(' ', '%20')

        url = self.METHOD['serverchan'] + key + ".send?text=" + text + "&desp=" + desp

        req = request.Request(url)
        response = request.urlopen(req)
        response = response.read().decode('utf-8')
        if "\"errmsg\":\"success\"" in response:
            return True
        else:
            return False

    def bark(self, key, address="", title="", content="",  copy_content="", url="", copy_flag=False, url_flag=False, https=False):
        if address != "":
            if https is True:
                push_url = "https://" + address + "/"
            else:
                push_url = "http://" + address + "/"
        else:
            push_url = self.METHOD['bark']
            
        title = title.replace(' ', '%20')
        content = content.replace(' ', '%20')

        if copy_flag:
            push_url = push_url + key + "/" + title + "/" + content + "?copy=" + copy_content
        elif url_flag:
            push_url = push_url + key + "/" + title + "/" + content + "?url=" + url
        else:
            push_url = push_url + key + "/" + title + "/" + content

        req = request.Request(push_url)
        response = request.urlopen(req)
        response = response.read().decode('utf-8')
        if "\"code\":200" in response:
            return True
        else:
            return False
        
    @staticmethod
    def tg_bot(token, chat_id, msg="Test message", htmlMode=False):
        tb = telebot.TeleBot(token)
        if htmlMode:
            tb.send_message(chat_id, msg, parse_mode="HTML")
        else:
            tb.send_message(chat_id, msg)
