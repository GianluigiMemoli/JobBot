import json
import os
import logging
import configparser
import threading
import telegram
from telegram.ext import Updater, CommandHandler
from Scraper.scraper import Scraper

cnfParser = configparser.ConfigParser()
cnfParser.read("config.ini")
TOKEN = cnfParser["Bot"]["TOKEN"]

interested_clients = set()

with open("match_words.json") as kwords_file:
    json_read = json.load(kwords_file)
    kwords = json_read["kwords"]




def start(update, ctx):
    interested_clients.add(update.effective_chat.id)
    ctx.bot.send_message(chat_id=update.effective_chat.id, text="Now you'll start reiceve messages for each post matches your needings")

def get_logs(update, ctx):
    files = os.listdir("logs")
    print("chiesti logs")
    for file in files:
        print("trovat: {}".format(file))
        ofile = open("logs/"+file, 'rb')
        ctx.bot.send_document(chat_id=update.effective_chat.id,
                         document=ofile)
        ofile.close()
class bot:

    def __init__(self):
        self.bot = telegram.Bot(token=TOKEN)
        self.updater = Updater(use_context=True, bot=self.bot)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(CommandHandler('start', start))
        self.dispatcher.add_handler(CommandHandler('logs', get_logs))

        self.x = threading.Thread(target=self.async_scraping, daemon=True)
        self.x.start()
        self.updater.start_polling()


    def async_scraping(self):
        self.scraper = Scraper(kwords, [Scraper.TITLE, Scraper.BODY], ['^\s*\[\s*HIRING\s*\]'])
        self.scraper.add_listener(self)
        self.scraper.analyze_stream()

    def on_new_post(self, post):
        for id in interested_clients:
            self.bot.send_message(chat_id=id, text="<b>{}</b>\n{}\n\n{}".format(post.title, post.selftext, post.url), parse_mode=telegram.ParseMode.HTML)


bot()
