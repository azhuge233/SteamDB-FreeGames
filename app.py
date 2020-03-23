import time, json
from MyClass import PUSH
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

URL = "https://steamdb.info/upcoming/free/"
PATH = "record.json"
TOKEN = ""
CHAT_ID = ""

def load_json():
	with open(PATH, 'r', encoding='utf-8') as f:
		data = json.load(f)
	return data

def write_json(data):
	with open(PATH, "w", encoding='utf-8') as f:
		json.dump(data, f, indent=4)

def push(msg):
	push = PUSH.Push()
	push.tg_bot(token=TOKEN, chat_id=CHAT_ID, msg=msg)

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
	previous = load_json()
	soup = BeautifulSoup(get_html(), "lxml")

	result = list([])
	push_result = list([])
	for eachtr in soup.select(".app"):
		tds = eachtr.find_all("td")
		
		free_type = tds[2].contents[0]
		game_name = str(tds[1].find("b").contents[0])
		sub_id = str(tds[1].contents[1].get('href').split('/')[2])
		steam_url = str(tds[0].contents[1].get('href'))
		start_time = str(tds[3].contents[0])
		end_time = str(tds[4].contents[0])
		
		if free_type != "Weekend":
			d = dict({})
			d["Name"] = game_name
			d["ID"] = sub_id
			d["URL"] = steam_url
			d["StartTime"] = start_time
			d["EndTime"] = end_time
			result.append(d)
			
			is_push = True
			for each in previous:
				if sub_id == each["ID"]:
					is_push = False
					break
			if is_push:
				tmp = "Name: " + game_name + "\n"
				tmp += "Sub ID: " + sub_id + "\n"
				tmp += "Url: " + steam_url + "\n"
				tmp += "Start time: " + start_time + "\n"
				tmp += "End time: " + end_time
				push_result.append(tmp)
	
	if len(push_result) != 0:
		for each in push_result:
			push("Steam Game +1 !\n" + each)
			time.sleep(0.5)
	if len(result) != 0:
		write_json(result)
			
if __name__ == "__main__":
	main()
