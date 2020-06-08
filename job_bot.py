import os
import logging
import threading
import telegram
from telegram.ext import Updater, CommandHandler
from Scraper.scraper import Scraper

TOKEN = '1231856261:AAEP2kvBYIPg2YwCXaCnEeidiQF7cYdA-Lw'
interested_clients = set()

kwords = ["js", "javascript", "java", "sql", "mysql", "c", "golang", "python", "database", "angular", "react", "desktop", "site", "website", "html", "css", "developer", "dev", "programmer", "code", "coder", "cloud", "bootstrap", "linux", "developers", "node", "node.js"]

file = open("logs", "a+")

def start(update, ctx):
    interested_clients.add(update.effective_chat.id)
    ctx.bot.send_message(chat_id=update.effective_chat.id, text="Now you'll start reiceve messages for each post matches your needings")

def get_logs(update, ctx):
    global file
    file.close()
    file = open("logs", "a+")
    log_content = file.read()
    ctx.bot.send_message(chat_id=update.effective_chat.id,
                         text=log_content if len(log_content) > 0 else "nope")
    file = open("logs", "a+")
class bot:

    def __init__(self):
        PORT = int(os.environ.get('PORT', 5000))
        self.bot = telegram.Bot(token=TOKEN)
        self.updater = Updater(use_context=True, bot=self.bot)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(CommandHandler('start', start))
        self.dispatcher.add_handler(CommandHandler('logs', get_logs))

        self.x = threading.Thread(target=self.async_scraping, daemon=True)
        self.updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
        self.updater.bot.setWebhook('https://redjobot.herokuapp.com/' + TOKEN)
        self.x.start()

    def async_scraping(self):

        self.scraper = Scraper(kwords, [Scraper.TITLE, Scraper.BODY], ['^\s*\[\s*HIRING\s*\]'], output_stream=file)
        self.scraper.add_listener(self)
        self.scraper.scraping()

    def on_new_post(self, post):
        for id in interested_clients:
            self.bot.send_message(chat_id=id, text="<b>{}</b>\n{}\n\n{}".format(post.title, post.selftext, post.url), parse_mode=telegram.ParseMode.HTML)

bot()