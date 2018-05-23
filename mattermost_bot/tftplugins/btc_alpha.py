# -*- encoding: utf-8 -*-
from mattermost_bot.utils import allow_only_direct_message
from mattermost_bot.bot import respond_to
from .helper import Table
from js9 import j


def check_configuration(func):
    def wrapped(*args, **kwargs):
        message = args[0]
        username = message.get_username()
        try:
            client = j.clients.btc_alpha.get(username, interactive=False)
            func(*args, client)
        except j.exceptions.Input:
            message.reply("You need to configure your instance first by calling `authorize KEY SECRET`")

    return wrapped


@respond_to('^configure\ (.*)\ (.*)$')
@allow_only_direct_message()
def configure(message, key, secret):
    username = message.get_username()
    client_data = {
        "key_": key,
        "secret_": secret
    }
    j.clients.btc_alpha.get(username, data=client_data)
    message.reply('You have configured your instance, Now start using my other commands')


configure.__doc__ = """`configure KEY SECRET`
Configure me using your api key and secret
"""


@respond_to('^currencies$')
@allow_only_direct_message()
@check_configuration
def get_currencies(message, client):
    currencies = client.get_currencies()
    table = Table(fields=['Name', "Sign"])
    for cur in currencies:
        table.add_row(fields=[cur['short_name'], cur['sign']])
    message.reply(table)


get_currencies.__doc__ = """`currencies` 
List all currencies available
"""


@respond_to('^pairs$')
@allow_only_direct_message()
@check_configuration
def get_pairs(message, client):
    pairs = client.get_pairs()
    table = Table(fields=['Currency1', 'Currency2', 'Maximum Order Size',
                          'Minimum Order Size', 'Pair Name', 'Price Precision'])
    for pair in pairs:
        table.add_row(fields=(
            pair['currency1'], pair['currency2'],
            pair['maximum_order_size'], pair['minimum_order_size'],
            pair['name'], pair['price_precision']
        ))
    message.reply(table)


get_pairs.__doc__ = """`pairs`
List all currencies pairs available
"""


@respond_to('^wallets$')
@allow_only_direct_message()
@check_configuration
def get_wallets(message, client):
    wallets = client.get_wallets()
    table = Table(fields=['Currency', 'Balance', 'Reserved'])
    for wallet in wallets:
        table.add_row(fields=(
            wallet['currency'], wallet['balance'], wallet['reserve']
        ))
    message.reply(table)


get_wallets.__doc__ = """`wallets`
List your own wallets
"""


@respond_to('^orderbook ([A-Za-z]+\_[A-Za-z]+)( limit\_buy=[\d]+)?( limit\_sell=[\d]+)?( group)?$')
@allow_only_direct_message()
@check_configuration
def get_order_book(message, pair, limit_buy, limit_sell, group, client):
    def generate_orders_table(order_type, orders_list, group_option):
        title = "### {} orders".format(order_type)
        if group_option:
            table = Table(fields=['Price', 'Amount'])
            for order in orders_list:
                table.add_row(fields=(order['price'], order['amount']))
        else:
            table = Table(fields=['Id', 'Price', 'Amount', 'Timestamp'])
            for order in orders_list:
                table.add_row(fields=(order['id'], order['price'], order['amount'], order['timestamp']))
        return "{title}\n\n{table}\n\n".format(title=title, table=table)

    limit_buy_filter = limit_sell_filter = 10 ** 10
    group_filter = 0
    if limit_buy:
        limit_buy_filter = int(limit_buy.split("=")[1])
    if limit_sell:
        limit_sell_filter = int(limit_sell.split("=")[1])
    if group:
        group_filter = 1
    orders = client.get_orderbook(pair, group=group_filter, limit_buy=limit_buy_filter, limit_sell=limit_sell_filter)
    output = ""
    if orders['sell']:
        output += generate_orders_table("sell", orders['sell'], group)
    if orders['buy']:
        output += generate_orders_table("buy", orders['buy'], group)
    message.reply(output)


get_order_book.__doc__ = """`orderbook PAIR [limit_buy=NUMBER] [limit_sell=NUMBER] [group]`
list all orders in btc-alpha. You need to provide the command with the currency pair to list orders for, 
also can limit the resulted buy orders or sell orders using limit_buy and limit_sell
also you can group orders by price 
"""


@respond_to('^my_(buy|sell)_orders$')
@allow_only_direct_message()
@check_configuration
def get_my_orders(message, order_type, client):
    orders_statuses = {
        1: "Active",
        2: "Cancelled",
        3: "Done"
    }
    fields = ['id', 'pair', 'amount', 'price', 'status']
    table = Table(fields=fields)

    orders = getattr(client, 'get_own_{}_orders'.format(order_type))()

    for order in orders:
        values = [order[field] for field in fields[:-1]]
        values.append(orders_statuses[order['status']])
        table.add_row(fields=values)
    message.reply(table)


get_order_book.__doc__ = """`my_buy_orders` or `my_sell_orders`
list all your orders based on their type 
"""


@respond_to('^order (sell|buy) ([A-Za-z]+\_[A-Za-z]+) ([0-9]*\.?[0-9]+) ([0-9]*\.?[0-9]+)$')
@allow_only_direct_message()
@check_configuration
def create_order(message, order_type, pair, amount, price, client):
    if order_type == 'sell':
        order = client.create_sell_order(pair, amount, price)
    else:
        order = client.create_buy_order(pair, amount, price)
    message.reply(order)


create_order.__doc__ = """`order TYPE PAIR AMOUNT PRICE`
create new exchange order with TYPE (buy or sell) and choose PAIR (i.e TFT_BTC)
"""
