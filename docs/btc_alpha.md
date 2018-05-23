# Btc Alpha Bot

## Installation:
- Prerequisites

    - Make sure Jumpscale is installed [docs](https://github.com/jumpscale/bash)
    - Make sure you have configured the config manager on the machine
        ```bash
        js9_config init
        ```

#### 1 - Installation on the same mattermost server machine using prefab
- Install mattermost bot
```python
machine.prefab.apps.mattermostbot.install(BOT_USER_NAME, BOT_EMAIL, BOT_PASSWORD)
machine.prefab.apps.mattermostbot.start()
```

where `BOT_USER_NAME`, `BOT_EMAIL` and `BOT_PASSWORD` are the details of you new bot user.

#### 2 - Installation on your machine
- Create a bot user manually on the chat server and add it to a team
- Install mattermost bot on your machine
```bash
git clone https://github.com/gigforks/mattermost_bot 
cd mattermost_bot
python3 setup.py install
touch local_settings.py
```
- Edit local_settings.py to be:
```python
BOT_URL = 'https://{CHAT_SERVER_UTL}/api/v4'
BOT_LOGIN = '{BOT_EMAIL}'
BOT_PASSWORD = "{BOT_PASSWORD}"
BOT_TEAM = "{BOT_TEAM}"
SSL_VERIFY = True
PLUGINS = [
    'mattermost_bot.tftplugins',
]
```
- Run The bot
```bash
MATTERMOST_BOT_SETTINGS_MODULE=local_settings PYTHONPATH=. matterbot
```


# Bot Usage
To start using BTC-Alpha bot you will need to start a direct chat with the bot user created then use any of the following commands:
 - `wallets`
List your own wallets

 - `configure KEY SECRET`
Configure me using your api key and secret

 - `currencies` 
List all currencies available
 
 - `pairs`
List all currencies pairs available
 
 - `order TYPE PAIR AMOUNT PRICE`
create new exchange order with TYPE (buy or sell) and choose PAIR (i.e TFT_BTC)

 - `my_buy_orders` or `my_sell_orders`
list all your orders based on their type 

- `orderbook PAIR [limit_buy=NUMBER] [limit_sell=NUMBER] [group]`
list all orders in btc-alpha. You need to provide the command with the currency pair to list orders for, 
also can limit the resulted buy orders or sell orders using limit_buy and limit_sell
also you can group orders by price

Note that you will need to authorize yourself firstly using `configure` command with your api keys and secret from [here](https://btc-alpha.com/accounts/api/settings/)
