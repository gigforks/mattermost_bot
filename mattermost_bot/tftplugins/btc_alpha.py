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


@respond_to('^currencies$')
@allow_only_direct_message()
@check_configuration
def get_currencies(message, client):
    currencies = client.get_currencies()
    table = Table(fields=['Name', "Sign"])
    for cur in currencies:
        table.add_row(fields=[cur['short_name'], cur['sign']])
    message.reply(table)


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
