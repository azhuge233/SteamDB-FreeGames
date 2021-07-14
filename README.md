# SteamDB-FreeGames

Gathering Steam free games information from [SteamDB](https://steamdb.info/upcoming/free/) then send notification with Telegram bot.

**Seems that SteamDB really don't want people scraping their site, check [Things should be aware of](./Things should be aware of.md) before using.**

## Requirements

- python3
  - playwright
  - bs4(lxml)
  - pyTelegramBotAPI
  - ~~selenium~~ (Not using, but required)
  - ~~undetected_chromedriver~~ (Not using, but required)

## Usage

Install playwright components 

``` shell
pip3 install playwright
python3 -m playwright install
```

Fill your bot TOKEN and your account ID to CONFIG field in the app.py file, then run

```shell
python3 app.py
```

To schedule the script, use cron.d in Linux(macOS) or Task Scheduler in Windows.

**Notice**: when the script used as a scheduled task, change the "PATH" variable to your absolute path.

Tested on Windows Server 2019 (python3.9) and macOS Big Sur (python3.9).