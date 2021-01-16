# A Telegram bot realized for scraping subreddits looking for jobs
The script is composed by two classes, the `job_bot.py` that's also the main class, that sends notifictions to the telegram bot whenever the other class `Scraper.py` finds some match in a given subreddit.
In `match_words.json` there's the array of keywords that the `Scraper.py` will try to match reading all the posts of a given subreddit.
In order to try the bot run:


- `pip install -r requiremnts.txt` 


- `python job_bot.py`