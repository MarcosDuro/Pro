import telethon
import asyncio
import telebot
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton
import os, sys
import re
import time
import requests
from telethon import TelegramClient, events
from random_address import real_random_address
import names
from datetime import datetime
import random


from defs import getUrl, getcards, phone
API_ID =  20312658
API_HASH = '08be37f8bfeba7e29b2f76082a82ecd6'
SEND_CHAT = -1001894658176

client = TelegramClient('anon', API_ID, API_HASH)

Token = '6609889169:AAEhsyFL1Ims047hvXOLis2ZsC5QoU-WP0U'

bot = telebot.TeleBot(Token, parse_mode='html')


ccs = []

chats  = [
    #'@VegetaScrap','
    -1001430249581,
    -1001662786975,
    -1001718470703,
    -1001618707894,
    -1001727369020,
    -1001511533698,
    -1001174204744,
    -1001618707894,
    -1001299585491,
    -1001308865865,
    -1001559825481,
    -1001430249581,
    -1001507818302,
    -1001738669918,
    -1001601838491,
    -1001738669918,
    -1001494650944,
    -1001662786975,
    -1001505241286,
    -1001394924627,
    -1001718470703,
    -1001308137657,
    -1001332955146,
    -1001601838491,
    -1001852459380,
    -1001928513690,
    -1001709038803,
    -1001870528182,
    -1001840733158,
    -1001319643429,
    -1001695237496,
    -1001150051137,
    -1001605321928,
    -1001637892109,
    -1001896622173,
    -1001883856033,
    -1001821890401,
    -1001668693502,
    -1001478292022

]

def hidden_card_number(card_number):
    return card_number[:-4] + "xxxx"
    
async def format_card_message(message, keywords):
    card_info = re.search(r'(\d{16}\|\d{2}\|\d{4}\|\d{3})', message)
    if card_info:
        card_number, exp_month, exp_year, cvv = card_info.group(1).split('|')
        hidden_number = hidden_card_number =(card_number)
        fullinfo =  f'{card_number}|{exp_month}|{exp_year}|{cvv}'
        print(fullinfo)


with open('cards.txt', 'r') as r:
    temp_cards = r.read().splitlines()

with open('cards.txt', 'r') as r:
    temp_cards = r.read().splitlines()


for x in temp_cards:
    car = getcards(x)
    if car:
        ccs.append(car[0])
    else:
        continue

@client.on(events.NewMessage(chats=chats, func = lambda x: getattr(x, 'text')))
async def my_event_handler(m):
    global contador
    contador += 1
    if m.reply_markup:
        text = m.reply_markup.stringify()
        urls = getUrl(text)
        if not urls:
            return
        text = requests.get(urls[0]).text
    else:
        text = m.text
    cards = getcards(text)
    if not cards:
        return
    cc,mes,ano,cvv = cards
    if cc in ccs:
        return
    ccs.append(cc)
    bin_response = requests.get(f'https://bins.antipublic.cc/bins/{cc[:6]}')
    if not bin_response:
        return
    result = bin_response.json()
    level = result.get("level")
    brand = result.get("brand")
    bank = result.get("bank")
    card_type = result.get("type")
    country_name = result.get("country_name")
    country_flag = result.get("country_flag")
    fullinfo = f'{cc}|{mes}|{ano}|{cvv}'
    print(fullinfo)
        
    fullinfo = f"{cc}|{mes}|{ano}|{cvv}"
contador = 0

              
    text = f""" 
#Bin[<code>{cc[:6]}</code>]  {contador}: {text} [<code>#{message_counter}: {message.text}</code>
]
<b><i>Card: </i></b><code>{cc}|{mes}|{ano}|{cvv}</code>
<b><i>Extra: </i></b> <code>{hidden_card_number(cc)} {mes}/{ano} </code>
<b><i>Bank: </i></b>{bank}
<b><i>Info: </i></b>{level}-{card_type}-{brand} {country_name} [{country_flag}]
"""    
    print(f'{cc}|{mes}|{ano}|{cvv}')
    with open('cards.txt', 'a') as w:
        w.write(fullinfo + '\n')
    bot.send_message(SEND_CHAT, text,parse_mode='HTML')
                     


client.start()
client.run_until_disconnected()