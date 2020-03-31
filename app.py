import time
from MyClass.json_op import *
from MyClass.PUSH import *
from MyClass.GETSOUP import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

URL = "https://steamdb.info/upcoming/free/"
PATH = "record.json"
ONE_HOUR_PATH = "one_hour_record.json"
TOKEN = ""
CHAT_ID = ""


def send_notification(msg_list):
	if len(msg_list) != 0:
		for each in msg_list:
			Push().tg_bot(msg=each, chat_id=CHAT_ID, token=TOKEN, htmlMode=True)
			time.sleep(1)


def record(path, data):
	if len(data) != 0:
		write_json(path=path, data=data)


def get_html():
	chrome_options = Options()
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-dev-shm-usage')
	browser = webdriver.Chrome(options=chrome_options)
	browser.get(URL)
	time.sleep(7)
	html = browser.page_source
	browser.close()
	return html


def main():
	previous = load_json(path=PATH)
	previous_on_hour = load_json(path=ONE_HOUR_PATH)
	dbsoup = BeautifulSoup(get_html(), "lxml")

	result = list([])
	starting_result = list([])
	
	push_result = list([])
	starting_push_result = list([])
	# go through all the free games
	for eachtr in dbsoup.select(".app"):
		tds = eachtr.find_all("td")
		
		free_type = tds[2].contents[0]
		game_name = str(tds[1].find("b").contents[0])
		sub_id = str(tds[1].contents[1].get('href').split('/')[2])
		# remove the url variables
		steam_url = str(tds[0].contents[1].get('href')).split("?")[0]
		start_time = str(tds[3].contents[0])
		end_time = str(tds[4].contents[0])
		
		# +1 game
		if free_type != "Weekend":
			# record information
			d = dict({})
			d["Name"] = game_name
			d["ID"] = sub_id
			d["URL"] = steam_url
			d["StartTime"] = start_time
			d["EndTime"] = end_time
			result.append(d)
			
			# if the game is starting in one hour, send starting notification
			start_time_split = start_time.split()
			# in minutes or in seconds
			if start_time_split[0] == "in" and (((int(start_time_split[1]) <= 10) and ("minute" in start_time_split[2])) or ("second" in start_time_split[2])) :
				starting_result.append(sub_id) # record starting games' subID
				
				is_push = True
				for each in previous_on_hour:
					if sub_id == each:
						is_push = False
				
				if is_push:
					steam_soup = get_url_single(url=steam_url)
					name = steam_soup.select(".apphub_AppName")
					if len(name) > 0:
						game_name = steam_soup.select(".apphub_AppName")[0].contents[0]
					tmp = "<b>" + game_name + " is starting " + start_time + "</b>\n\n"
					tmp += "Sub ID: <i>" + sub_id + "</i>"
					starting_push_result.append(tmp) # notification list
			
			# check if this game exists in previous records
			is_push = True
			for each in previous:
				if sub_id == each["ID"]:
					is_push = False
					break
			# if it does not exist, then notify
			if is_push:
				# try to get game's name on Steam store page
				steam_soup = get_url_single(url=steam_url)
				name = steam_soup.select(".apphub_AppName")
				if len(name) > 0:
					game_name = steam_soup.select(".apphub_AppName")[0].contents[0]
				# if the age page shows up, use SteamDB name
				tmp = "<b>" + game_name + "</b>\n\n"
				tmp += "Sub ID: <i>" + sub_id + "</i>\n"
				# prettify url
				tmp += "Url: <a href=\"" + steam_url + "\" >" + game_name + "</a>" + "\n"
				tmp += "Start time: " + start_time + "\n"
				tmp += "End time: " + end_time
				push_result.append(tmp)
	
	# do the notify job
	send_notification(starting_push_result)
	send_notification(push_result)
	
	# refresh the record
	record(PATH, result)
	record(ONE_HOUR_PATH, starting_result)
			
if __name__ == "__main__":
	main()
