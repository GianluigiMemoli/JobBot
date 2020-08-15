import datetime
import os
import logging
import configparser
import threading
import telegram
from telegram.ext import Updater, CommandHandler
from Scraper.scraper import Scraper

TOKEN = '1231856261:AAEP2kvBYIPg2YwCXaCnEeidiQF7cYdA-Lw'
interested_clients = set()

kwords = [
    "js",
    "javascript",
    "java",
    "sql",
    "mysql",
    "c",
    "golang",
    "python",
    "database",
    "angular",
    "react",
    "desktop",
    "site",
    "website",
    "html",
    "css",
    "developer",
    "dev",
    "programmer",
    "code",
    "coder",
    "cloud",
    "bootstrap",
    "linux",
    "developers",
    "node",
    "node.js"
]

if not os.path.exists("logs"):
    os.mkdir("logs")

def write_logs(text):
    filename = "{}/{}".format("logs",str(datetime.date.today()))
    with open(filename, "a+") as log_file:
        time = str(datetime.datetime.now())
        log_file.write("[{}] {}\n".format(time.split('.')[0], text))



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
        PORT = int(os.environ.get('PORT', 5000))
        self.bot = telegram.Bot(token=TOKEN)
        self.updater = Updater(use_context=True, bot=self.bot)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(CommandHandler('start', start))
        self.dispatcher.add_handler(CommandHandler('logs', get_logs))

        self.x = threading.Thread(target=self.async_scraping, daemon=True)
        self.x.start()
        write_logs("started")
        self.updater.start_polling()


    def async_scraping(self):
        self.scraper = Scraper(kwords, [Scraper.TITLE, Scraper.BODY], ['^\s*\[\s*HIRING\s*\]'])
        self.scraper.add_listener(self)
        self.scraper.analyze_stream()

    def on_new_post(self, post):
        for id in interested_clients:
            self.bot.send_message(chat_id=id, text="<b>{}</b>\n{}\n\n{}".format(post.title, post.selftext, post.url), parse_mode=telegram.ParseMode.HTML)


bot()
