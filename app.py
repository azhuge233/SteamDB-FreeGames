import datetime
import sys
from twocaptcha import TwoCaptcha
from fake_useragent import UserAgent
from MyClass.json_op import *
from MyClass.PUSH import *
from MyClass.GETSOUP import *
from MyClass.LOG import *

'''CONFIG START'''
TOKEN = ""  # Bot token
CHAT_ID = ""  # Admin ID
API_KEY = ""  # 2captcha api key
'''CONFIG END'''

'''Static Variables'''
URL = "https://steamdb.info/upcoming/free/"
PATH = "record.json"
FIRST_DELAY = 10
SECOND_DELAY = 5
SUBMIT_SCRIPT = "window.submitToken = function(token) { " \
                "document.querySelector('[name=g-recaptcha-response]').innerText = token;" \
                "document.querySelector('[name=h-captcha-response]').innerText = token;" \
                "document.querySelector('.challenge-form').submit();" \
                "}"
'''Static Variables END'''

'''Global Variables'''
# logger
logger.name = "SteamDB-FreeGames"
# browser
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('User-Agent=' + str(UserAgent().random))
# have to remove no picture option due to captcha loading issue
# if picture loading were disabled, captcha may fails loading randomly
browser = webdriver.Chrome(options=chrome_options)
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
	utc_format = "%d %B %Y – %H:%M:%S %Z"
	utc_date = datetime.datetime.strptime(utc, utc_format)
	cst_date = utc_date + datetime.timedelta(hours=8)
	return cst_date.strftime("%Y 年 %m 月 %d 日 %H:%M")


def solv_captcha(sitekey):  # solve captcha
	solver = TwoCaptcha(API_KEY)
	try:
		result = solver.hcaptcha(
			sitekey=sitekey,
			url=URL,
		)
	except Exception as e:
		logger.error("Solve captcha failed!")
		sys.exit(e)
	else:
		return result['code']


def get_sitekey(html):  # get captcha sitekey
	iframe = html.select('iframe')
	source = iframe[0].get('src')
	sitekey = str(source).split("sitekey=")[1]
	return sitekey


def load_page():
	browser.get(URL)
	time.sleep(FIRST_DELAY)  # wait a few seconds to load the captcha
	html = BeautifulSoup(browser.page_source, 'lxml')
	return html


def start_process(previous, db_free_page_soup):
	result = list([])
	push_result = list([])
	
	# go through all the free games
	for each_tr in db_free_page_soup.select(".app"):
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
	html = load_page()
	logger.warning("Done")
	
	if html.find('iframe') is None:
		logger.info("Captcha not found")
		# web driver ends
		browser.quit()
		
		# start analysing page source
		logger.warning("Start processing data...")
		start_process(previous=previous, db_free_page_soup=html)
	else:
		logger.warning("Getting sitekey...")
		sitekey = get_sitekey(html)
		logger.warning("Sitekey: " + sitekey)
		
		logger.warning("Solving captcha...")
		result_code = solv_captcha(sitekey=sitekey)
		logger.warning("Done")
	
		# inject javascript submit function
		logger.warning("Submitting captcha code...")
		browser.execute_script(SUBMIT_SCRIPT)
		browser.execute_script("submitToken('" + result_code + "')")
		time.sleep(SECOND_DELAY)  # give some time to let browser load the page
		logger.warning("Done")
	
		# convert page html to lxml
		logger.warning("Getting page source...")
		db_free_page_soup = BeautifulSoup(browser.page_source, 'lxml')
		logger.warning("Done")
		
		# web driver ends
		browser.quit()
	
		# start analysing page source
		logger.warning("Start processing data...")
		start_process(previous=previous, db_free_page_soup=db_free_page_soup)
	
	logger.warning("Task Done!")
	logger.info("\n\n")


if __name__ == "__main__":
	main()
