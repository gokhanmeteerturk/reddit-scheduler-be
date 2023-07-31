import praw

from cursor import Database


class RedditManager:
    def __init__(self):
        self.reddit = None
        self.username = None
        self.password = None
        self.client_id = None
        self.client_secret = None
        self.user_agent = (
            "android:reddit-scheduler-for-"
            + self.username
            + ":v0.1.1 (by /u/"
            + self.username
            + ")"
        )

    def set_user(self, username):
        db = Database()
        c = db.connect()
        c.execute("SELECT * FROM users WHERE username = ? LIMIT 1", (username,))
        record = c.fetchone()
        db.disconnect()
        if record is None:
            return False
        else:
            (
                self.username,
                self.password,
                self.client_id,
                self.client_secret,
            ) = record
            try:
                self.reddit = praw.Reddit(
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                    password=self.password,
                    user_agent=self.user_agent,
                    username=self.username,
                )
                if str(self.reddit.user.me()) == self.username:
                    return True
                else:
                    raise Exception("Trouble with returned username")
            except:
                return False

    def create_submission(self):
        sub, title, text, link, image, video, flairid, nsfw = None
        try:
            if image == None and video == None:
                submission = self.reddit.subreddit(sub).submit(
                    title, selftext=text, url=link, flair_id=flairid, nsfw=nsfw
                )
            else:
                if video == None:
                    submission = self.reddit.subreddit(sub).submit_image(
                        title, image_path=image, flair_id=flairid, nsfw=nsfw
                    )
                else:
                    submission = self.reddit.subreddit(sub).submit_video(
                        title,
                        video_path=video,
                        thumbnail_path=image,
                        flair_id=flairid,
                        nsfw=nsfw,
                    )
            return submission.id
        except:
            return None


x = RedditManager()
x.set_user("u")
