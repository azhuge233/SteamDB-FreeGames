import datetime
from MyClass.json_op import *
from MyClass.PUSH import *
from MyClass.GETSOUP import *

'''CONFIG START'''
TOKEN = ""
CHAT_ID = ""
'''CONFIG END'''

URL = "https://steamdb.info/upcoming/free/"
PATH = "record.json"
DELAY = 7


def send_notification(msg_list): # send messages to Telegram Bot
	if len(msg_list) != 0:
		for each in msg_list:
			Push().tg_bot(msg=each, chat_id=CHAT_ID, token=TOKEN, htmlMode=True)
			time.sleep(1)


def record(path, data): # write data to json file
	if len(data) != 0:
		write_json(path=path, data=data)


def utc2cst(utc): # convert UTC to CST
	utc_format = "%d %B %Y – %H:%M:%S %Z"
	utc_date = datetime.datetime.strptime(utc, utc_format)
	cst_date = utc_date + datetime.timedelta(hours=8)
	return cst_date.strftime("%Y 年 %m 月 %d 日 %H:%M")


def main():
	previous = load_json(path=PATH)
	db_free_page_soup = selenium_get_url(URL, DELAY, nopic=True)

	result = list([])
	push_result = list([])
	
	# go through all the free games
	for each_tr in db_free_page_soup.select(".sub"):
		tds = each_tr.find_all("td")
		td_len = len(tds)
		
		'''get basic info'''
		if td_len == 5: # steamdb add a install button in table column
			free_type = tds[2].contents[0]
			start_time = str(utc2cst(tds[3].get("title")))
			end_time = str(utc2cst(tds[4].get("title")))
		else :
			free_type = tds[3].contents[0]
			start_time = str(utc2cst(tds[4].get("title")))
			end_time = str(utc2cst(tds[5].get("title")))
		
		game_name = str(tds[1].find("b").contents[0])
		sub_id = str(tds[1].contents[1].get('href').split('/')[2])
		# remove the url variables
		steam_url = str(tds[0].contents[1].get('href')).split("?")[0]
		'''get basic info end'''
		
		# +1 game
		if free_type != "Weekend":
			
			# record information
			d = dict({})
			d["Name"] = game_name
			d["ID"] = sub_id
			d["URL"] = steam_url
			d["Start_time"] = start_time
			d["End_time"] = end_time
			result.append(d)
			
			'''new free games notify'''
			# check if this game exists in previous records
			is_push = True
			for each in previous:
				if sub_id == each["ID"]:
					is_push = False
					break
				
			# if it does not exist, then notify
			if is_push:
				
				'''get game details'''
				# try to get game's name on Steam store page
				steam_soup = get_url_single(url=steam_url)
				name = steam_soup.select(".apphub_AppName")
				if len(name) > 0:
					game_name = steam_soup.select(".apphub_AppName")[0].contents[0]
				'''get game details end'''
				
				tmp = "<b>" + game_name + "</b>\n\n"
				tmp += "Sub ID: <i>" + sub_id + "</i>\n"
				# prettify url
				tmp += "链接: <a href=\"" + steam_url + "\" >" + game_name + "</a>" + "\n"
				tmp += "开始时间: " + start_time + "\n"
				tmp += "结束时间: " + end_time
				push_result.append(tmp)
			'''new free games notify end'''
	
	# do the notify job
	send_notification(push_result)
	
	# refresh the record
	if len(result) > 0:
		record(PATH, result)
	else:
		pass

if __name__ == "__main__":
	main()
