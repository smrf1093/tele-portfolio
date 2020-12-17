TelePortfolio
======
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
![ci](https://github.com/seyedrezafar/tele-portfolio/workflows/ci/badge.svg)
[![LICENSE](https://img.shields.io/github/license/seyedrezafar/tele-portfolio?style=flat-square)](https://github.com/seyedrezafar/tele-portfolio/blob/master/LICENSE.md)
## Overview
TelePortFolio is your personal cryptocurrency portfolio tracking/alerting software. this software is made using Covalent api, Flask, Influxdb and Telegram api.

[![TelePortfolio](../assets/dashboard.png)](https://github.com/seyedrezafar/tele-portfolio)
## Demo
Demo link here
## Quickstart
### Create a `.env` file
This app reads configuration from a dot env file. see example:
```sh
$ cat env.example
 BOT_TOKEN=your bot token
 SECRET_KEY=long alphanumeric string
 COVALENT_API_KEY=covalent api key
 INFLUXDB_HOST=localhost
 INFLUXDB_PORT=8086
 CURRENCY_SIGN=$
```
Please move this file to `.env` and provide your configurations:
```sh
$ move env.example .env 
```

### Create a telegram bot
To enable alerting functionallity you need to provide a `BOT_TOKEN`.
To creat a bot please follow the instructions in [here](https://core.telegram.org/bots#3-how-do-i-create-a-bot)
#### Find your chat id
This app uses BOT_CHATID to send a direct telegram message to the wallet owner. to find your chat id you can use [this telegram bot](https://t.me/useridgetbot).
### Run using docker
This app consist of two components: An alerting component that alert when there is a change in portfolio balance value, second a flask app that provides a dashboard to view current portfolio.  


You can simply run both components using docker-compose:
```console
docker-compose up -d
```  
Next open up your browser and head to https://localhost:5000 to see the dashboard
## Credits
This software is powered by Covalent api. so special thanks to Covalent for the awesome api <3
![powered by](https://www.covalenthq.com/static/images/covalent-logo.png)
## License
See [LICENSE.md](LICENCE.md)
