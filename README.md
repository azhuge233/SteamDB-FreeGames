# SteamDB-FreeGames
Gathering Steam free games information from [SteamDB](https://steamdb.info/upcoming/free/) then send notification using Telegram bot.

## Requirements

- python3
  - selenium
  - bs4(lxml)
  - pyTelegramBotAPI
- GUI enviroment
- Google Chrome
  - with chromedriver installed

## Usage

Fill your bot TOKEN and your account ID to CONFIG field in the app.py file, then run

```shell
python3 app.py
```

To schedule the script, use cron.d in Linux(macOS) or Task Scheduler in Windows.

**Notice**: when the script used as a scheduled task, change the "PATH" variable to your absolute path.

Tested on Windows Server 2016 (python3.8) and macOS Catalina 10.15.4 (python3.7.7), both have the latest Chrome and chromedriver installed.