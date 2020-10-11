# SteamDB-FreeGames

Gathering Steam free games information from [SteamDB](https://steamdb.info/upcoming/free/) then send notification using Telegram bot.

### Note that this script is no longer usable, since SteamDB updated the anti-spider method, I may update this once it's achievable.

Here's the whole sotry: At the very beginning they just has a 5 secs countdown  before you can reach the page, then couple weeks ago they added hcaptcha to prevent spiders, I used 2captcha to bypass it, but when I just updated the 2captcha version, they changed the method, now they are using a different method with no captcha implements that I apparently can't reach the free games page with selenium.

## Requirements

- python3
  - selenium
  - bs4(lxml)
  - pyTelegramBotAPI
  - 2captcha-python
- GUI enviroment
- Google Chrome
  - with chromedriver installed

## Usage

Fill your bot TOKEN, your account ID and 2captcha API key to CONFIG field in the app.py file, then run

```shell
python3 app.py
```

To schedule the script, use cron.d in Linux(macOS) or Task Scheduler in Windows.

**Notice**: when the script used as a scheduled task, change the "PATH" variable to your absolute path.

Tested on Windows Server 2016 (python3.8) and macOS Catalina 10.15.4 (python3.7.7), both have the latest Chrome and chromedriver installed.