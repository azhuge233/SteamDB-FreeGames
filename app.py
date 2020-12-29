import datetime
import sys
from MyClass.GETSOUP import *
from MyClass.json_op import *
from MyClass.PUSH import *
from MyClass.LOG import *

'''CONFIG START'''
TOKEN = ""  # Bot token
CHAT_ID = ""  # Admin ID
'''CONFIG END'''

'''Static Variables'''
URL = "https://steamdb.info/upcoming/free/"
PATH = "record.json"
FIRST_DELAY = 10
'''Static Variables END'''

'''Global Variables'''
# logger
logger.name = "SteamDB-FreeGames"
'''Global Variables END'''


def send_notification(msg_list):  # send messages to Telegram Bot
	if len(msg_list) != 0:
		try:
			for each in msg_list:
				Push().tg_bot(msg=each, chat_id=CHAT_ID, token=TOKEN, htmlMode=True)
				time.sleep(1)
		except Exception as e:
			logger.error("Send message error!")
			sys.exit(e)


def record(path, data):  # write data to json file
	if len(data) != 0:
		write_json(path=path, data=data)


def utc2cst(utc):  # convert UTC to CST
	utc_format = "%Y-%m-%dT%H:%M:%S+00:00"
	utc_date = datetime.datetime.strptime(utc, utc_format)
	cst_date = utc_date + datetime.timedelta(hours=8)
	return cst_date.strftime("%Y 年 %m 月 %d 日 %H:%M")


def start_process(previous, db_free_page_soup):
	result = list([])
	push_result = list([])
	
	# go through all the free games
	for each_tr in db_free_page_soup.select(".app"):
		if ("hidden" in each_tr.attrs.keys()):
			continue
		
		tds = each_tr.find_all("td")
		td_len = len(tds)
		
		'''get basic info'''
		if td_len == 5:  # steamdb add a install button in table column
			free_type = tds[2].contents[0]
			start_time = str(utc2cst(tds[3].get("title")))
			end_time = str(utc2cst(tds[4].get("title")))
		else:
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
			logger.info("Found free game: " + game_name)
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
				
				logger.info("Add " + game_name + " to push list")
				
				tmp = "<b>" + game_name + "</b>\n\n"
				tmp += "Sub ID: <i>" + sub_id + "</i>\n"
				# prettify url
				tmp += "链接: <a href=\"" + steam_url + "\" >" + game_name + "</a>" + "\n"
				tmp += "开始时间: " + start_time + "\n"
				tmp += "结束时间: " + end_time
				push_result.append(tmp)
			'''new free games notify end'''
	
	# do the notify job
	if len(push_result) == 0:
		logger.info("No new free games, no messages were sent!")
	else:
		logger.info("Sending notifications...")
		logger.info("This may fail due to network issue.")
		send_notification(push_result)
	
	# refresh the record
	if len(result) > 0:
		logger.info("Writing records...")
		record(PATH, result)
	else:
		logger.info("No records were written!")


def main():
	logger.warning("------------------- Start job -------------------")
	
	logger.warning("Loading previous records...")
	previous = load_json(path=PATH)
	logger.warning("Done")
	
	logger.warning("Loading the page...")
	html = selenium_get_url(url=URL, delay=FIRST_DELAY, uc=True)
	logger.warning("Done")
		
	# start analysing page source
	logger.warning("Start processing data...")
	start_process(previous=previous, db_free_page_soup=html)
	logger.warning("Task Done!")
	logger.info("\n\n")


if __name__ == "__main__":
	main()
