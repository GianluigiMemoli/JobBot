import praw
import re
config = {
    'client_id': 'mdqG2sGK2dqvGA',
    'client_secret': '6xI4XJ-3Q2fti5namgWMUwJgDCI',
    'password': 'QzJWH9BDb5gpPDz',
    'user_agent': 'desktop:job_bot:v0.1(by /u/gianja98)',
    'username': 'Gianja98'
}


class Scraper:
    BODY = 'selftext'
    TITLE = 'title'

    def __init__(self, keywords, match_in, must_match: []):
        if len(match_in) == 0:
            raise Exception("Must specify at least one value for match_in from Scraper.TITLE and Scraper.BODY")
        if len(keywords) == 0:
            raise Exception("Must specify at least one value for keyword")
        self.must_match = must_match
        self.keywords = [x.lower() for x in keywords]
        self.match_in = match_in
        self.listeners = []
        print("matchin: {}".format(self.match_in))

    def match_pattern(self, new_post: praw.reddit.Submission):

        texts = []
        for to_match in self.match_in:
            raw_text = getattr(new_post, to_match)
            texts.append(raw_text.lower())
        print("texts {}".format(texts))
        # If no must_match is specified it's given for satisfied
        must_matched = len(self.must_match) == 0

        for must_matching in self.must_match:
            for text in texts:
                if re.match(must_matching, text) is not None:
                    print("regex matched")
                    must_matched = True
                else:
                    print("regex: {} not matched on {}".format(must_matching, text))
        if not must_matched:
            return False

        keyword_matched = False
        for text in texts:
            for keyword in self.keywords:
                if keyword in text:
                    keyword_matched = True
                    print("matched kw: {} on: {}".format(keyword, text))
                else:
                    print("not matched kw: {} on: {}".format(keyword, text))
        return keyword_matched and must_matched


    def scraping(self):
        reddit = praw.Reddit(**config)
        while True:
            for submission in reddit.subreddit('forhire').stream.submissions(skip_existing=True):
                if self.match_pattern(submission):
                    self.on_new_post_match(submission)


    def add_listener(self, listener):
        self.listeners.append(listener)

    def remove_listener(self, listener):
        self.listeners.remove(listener)

    def on_new_post_match(self, post):
        for listener in self.listeners:
            listener.on_new_post(post)


