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

'''Global Variables'''
URL = "https://steamdb.info/upcoming/free/"
PATH = "record.json"
FIRST_DELAY = 10 # SECOND_DELAY removed since SteamDB disabled hCaptcha
BROWSER_TYPE = ["chromium", "firefox", "webkit"]
NOTIFICATION_FORMAT = "<b>{0}</b>\n\nSub ID: <i>{1}</i>\n链接: <a href=\"{2}\" > {3}</a>\n开始时间: {4}\n结束时间: {5}\n"
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
	return cst_date.strftime("%Y {y} %m {m} %d {d} %H:%M").format(y='年', m='月', d='日')


def start_process(previous, db_free_page_soup):
	result = list([])
	push_result = list([])
	
	# go through all the free games
	for each_tr in db_free_page_soup.select(".app"):
		# skip trap column
		if "hidden" in each_tr.attrs.keys():
			continue
		
		tds = each_tr.find_all("td")
		td_len = len(tds)
		
		'''get basic info'''
		if td_len == 5:  # steamdb add a install button in table column
			free_type = tds[2].contents[0]
			start_time = str(tds[3].get("data-time"))
			end_time = str(tds[4].get("data-time"))
		else:
			free_type = tds[3].contents[0]
			start_time = str(tds[4].get("data-time"))
			end_time = str(tds[5].get("data-time"))
			
		# str(None) == "None", added this in C# version
		# start_time = "None" if start_time == None else utc2cst(start_time)
		# end_time = "None" if end_time == None else utc2cst(end_time)
		
		game_name = str(tds[1].find("b").contents[0])
		sub_id = str(tds[1].contents[1].get('href').split('/')[2])
		# remove the url variables
		steam_url = str(tds[0].contents[1].get('href')).split("?")[0]
		'''get basic info end'''
		
		# +1 game
		if free_type != "Weekend":
			logger.info("Found free game: " + game_name)
			# record information
			result.append({
				"Name": game_name,
				"ID": sub_id,
				"URL": steam_url,
				"Start_time": start_time,
				"End_time": end_time,
			})
			
			'''new free games notify'''
			# if it does not exist, then notify
			if not any(d.get('ID') == sub_id for d in previous):
				
				'''get game details'''
				# try to get game's name on Steam store page
				steam_soup = get_url_single(url=steam_url)
				name = steam_soup.select(".apphub_AppName")
				if len(name) > 0:
					game_name = steam_soup.select(".apphub_AppName")[0].contents[0]
				'''get game details end'''
				
				logger.info("Add " + game_name + " to push list")

				push_result.append(NOTIFICATION_FORMAT.format(game_name, sub_id, steam_url, game_name, start_time, end_time))
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
	html = playright_get_url(url=URL, type=BROWSER_TYPE[2], delay=FIRST_DELAY, headless=True)
	logger.warning("Done")
		
	# start analysing page source
	logger.warning("Start processing data...")
	start_process(previous=previous, db_free_page_soup=html)
	logger.warning("Task Done!")
	logger.info("\n\n")


if __name__ == "__main__":
	main()
