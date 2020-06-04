import logging
import threading
import telegram
from telegram.ext import Updater, CommandHandler
from Scraper.scraper import Scraper

interested_clients = set()

kwords = ["js", "javascript", "java", "sql", "mysql", "c", "golang", "python", "database", "angular", "react", "desktop", "site", "website", "html", "css", "developer", "dev", "programmer", "code", "coder", "cloud", "bootstrap", "linux"]

def start(update, ctx):
    interested_clients.add(update.effective_chat.id)
    ctx.bot.send_message(chat_id=update.effective_chat.id, text="Now you'll start reiceve messages for each post matches your needings")


class bot:

    def __init__(self):
        self.bot = telegram.Bot(token='1231856261:AAEP2kvBYIPg2YwCXaCnEeidiQF7cYdA-Lw')
        self.updater = Updater(use_context=True, bot=self.bot)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(CommandHandler('start', start))
        self.x = threading.Thread(target=self.async_scraping, daemon=True)
        self.updater.start_polling()
        self.x.start()

    def async_scraping(self):
        self.scraper = Scraper(kwords, [Scraper.TITLE, Scraper.BODY], ['^\s*\[\s*HIRING\s*\]'])
        self.scraper.add_listener(self)
        self.scraper.scraping()

    def on_new_post(self, post):
        for id in interested_clients:
            self.bot.send_message(chat_id=id, text="<b>{}</b>\n{}\n\n{}".format(post.title, post.selftext, post.url), parse_mode=telegram.ParseMode.HTML)

bot()