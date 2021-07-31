# SteamDB-FreeGames

Gathering Steam free games information from [SteamDB](https://steamdb.info/upcoming/free/) then send notification with Telegram bot.

**Seems that SteamDB really don't want people scraping their site, check [Things should be aware of](https://github.com/azhuge233/SteamDB-FreeGames/blob/master/Things%20should%20be%20aware%20of.md) before using.**

There's a [dotnet version](https://github.com/azhuge233/SteamDB-FreeGames-dotnet), any future updates will be added there first.

## Usage

Clone repo

```shell
git clone https://github.com/azhuge233/SteamDB-FreeGames.git
```

Install packages

``` shell
pip3 install -r requirements.txt
```

Fill your bot TOKEN and your account ID to CONFIG field in the app.py file, then run

```shell
python3 app.py
```

To schedule the script, use cron.d in Linux(macOS) or Task Scheduler in Windows.

**Notice**: when the script used as a scheduled task, change the "PATH" variable to your absolute path.

Tested on Windows Server 2019 (python3.9) and macOS Big Sur (python3.9).