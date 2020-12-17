TelePortfolio
======
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
![ci](https://github.com/seyedrezafar/tele-portfolio/workflows/ci/badge.svg)
[![LICENSE](https://img.shields.io/github/license/seyedrezafar/tele-portfolio?style=flat-square)](https://github.com/seyedrezafar/tele-portfolio/blob/master/LICENSE.md)
## Overview
TelePortFolio is your personal cryptocurrency portfolio tracking/alerting software. this software is made using Covalent api, Flask, Influxdb and Telegram api.
[![TelePortfolio](../assets/dashboard.png)](https://github.com/seyedrezafar/tele-portfolio)

## Quickstart
### Create a `.env` file
This app reads configuration from a dot env file. see example:
```sh
$ cat env.example
export BOT_CHATID=must be a number
export BOT_TOKEN=your bot token
export SECRET_KEY=long alphanumeric string
export COVALENT_API_KEY=covalent api key
export WALLET_ADDRESS=an ethereum wallet addres
export CURRENCY=fill with a supported Covalent currency
export INFLUXDB_HOST=localhost
export INFLUXDB_PORT=8086
export CURRENCY_SIGN=$
```
Please move this file to `.env` and provide your configurations:
```sh
$ move env.example .env 
```

### Create a telegram bot
To enable alerting functionallity you need to provide a `BOT_TOKEN` and a `BOT_CHATID`.
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
## License
See [LICENSE.md](LICENCE.md)
#### Special thanks to Covalent for the awesome api
![powered by](https://www.covalenthq.com/static/images/covalent-logo.png)
