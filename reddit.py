from typing import List
import praw

from cursor import Database


class RedditManager:
    def __init__(self):
        self.reddit = None
        self.username = None
        self.password = None
        self.client_id = None
        self.client_secret = None
        self.user_agent = None

    def get_user(self):
        return self.reddit.user.me()

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
            self.user_agent = (
                "android:reddit-scheduler-for-"
                + self.username
                + ":v0.1.1 (by /u/"
                + self.username
                + ")"
            )
            try:
                self.reddit = praw.Reddit(
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                    password=self.password,
                    user_agent=self.user_agent,
                    username=self.username,
                )
                if str(self.get_user()) == self.username:
                    return True
                else:
                    raise Exception("Trouble with returned username")
            except:
                return False

    def create_crosspost(self, parent_submission_id, target_sub):
        try:
            submission = self.reddit.submission(parent_submission_id)
            cross_post = submission.crosspost(target_sub)
            return cross_post
        except Exception as e:
            return None

    def create_submission(self, sub, title, text, link, image, video, flairid, nsfw):
        try:
            if image is None and video is None:
                submission = self.reddit.subreddit(sub).submit(
                    title, selftext=text, url=link, flair_id=flairid, nsfw=nsfw
                )
            else:
                if video is None:
                    image_dir = "./"
                    image_path = image_dir + image
                    submission = self.reddit.subreddit(sub).submit_image(
                        title, image_path=image_path, flair_id=flairid, nsfw=nsfw
                    )
                else:
                    image_dir = "./"
                    video_dir = "./"
                    submission = self.reddit.subreddit(sub).submit_video(
                        title,
                        video_path=video_dir+video,
                        thumbnail_path=image_dir+image,
                        flair_id=flairid,
                        nsfw=nsfw,
                    )
            return submission.id
        except:
            return None

    def crosspostable_subs(self) -> List:
        if self.reddit is not None:
            result = list(self.reddit.get("/api/crosspostable_subreddits"))
            try:
                result.remove("u_{}".format(self.username))
            except ValueError:
                pass
            return result
        else:
            return []
