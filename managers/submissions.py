from typing import List
from cursor import Database
from payloads import CrosspostRequestPayload, RedditPostPayload
import time

from reddit import RedditManager


class SubmissionsManager:
    def create_submission(self, submission: RedditPostPayload):
        db = Database()
        c = db.connect()
        if not submission.image_name:
            submission.image_name = None
        if not submission.link:
            submission.link = None
        if not submission.text:
            submission.text = None
        c.execute(
            "INSERT INTO submissions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                submission.planned_unix_datetime,
                "wait",  # initial status
                submission.username,
                submission.sub,
                submission.title,
                submission.text,
                submission.link,
                submission.image_name,
                submission.video,
                submission.flairid,
                submission.nsfw,
                None,  # submission_id,
                None,  # crosspost_of
            ),
        )
        submission_rowid = c.lastrowid
        db.connection.commit()

        if submission.crosspost_requests:
            self._handle_crosspost_requests(submission, submission_rowid)

        db.disconnect()
        return {"result": "Success"}

    def _handle_crosspost_requests(
        self,
        parent_submission: RedditPostPayload,
        parent_submission_rowid: int,
    ):
        for crosspost_request in parent_submission.crosspost_requests:
            db = Database()
            c = db.connect()

            c.execute(
                "INSERT INTO submissions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    crosspost_request.planned_unix_datetime,
                    "wait",  # initial status
                    parent_submission.username,
                    crosspost_request.sub,
                    parent_submission.title,
                    parent_submission.text,
                    None,  # parent_submission.link,
                    None,  # parent_submission.image_name,
                    None,  # parent_submission.video,
                    None,  # parent_submission.flairid,
                    parent_submission.nsfw,
                    parent_submission.submission_id,
                    parent_submission_rowid,  # crosspost_of,
                ),
            )
        db.connection.commit()

    def read_submission(self, rowid: int):  # Update parameter name here
        db = Database()
        c = db.connect()
        c.execute(
            "SELECT rowid, * FROM submissions WHERE rowid = ?",  # Update the query
            (rowid,),
        )
        submission_tuple = c.fetchone()
        db.disconnect()
        if submission_tuple:
            return RedditPostPayload.from_tuple(submission_tuple)
        else:
            return None

    def update_submission(self, submission: RedditPostPayload):
        db = Database()
        c = db.connect()
        c.execute(
            "UPDATE submissions SET planned_unix_datetime=?, status=?, username=?, sub=?, title=?, text=?, link=?, image_name=?, video=?, flairid=?, nsfw=?, submission_id=? WHERE rowid=?",
            (
                submission.planned_unix_datetime,
                submission.status,  # initial status
                submission.username,
                submission.sub,
                submission.title,
                submission.text,
                submission.link,
                submission.image_name,
                submission.video,
                submission.flairid,
                submission.nsfw,
                submission.submission_id,
                submission.rowid,  # The rowid of the row you want to update
            ),
        )

        db.connection.commit()
        db.disconnect()
        return {"result": "Success"}

    def delete_submission(self, rowid: int):  # Update parameter name here
        db = Database()
        c = db.connect()
        c.execute(
            "DELETE FROM submissions WHERE rowid = ?",  # Update the query
            (rowid,),
        )
        db.connection.commit()
        db.disconnect()
        return {"result": "Success"}

    def list_submissions(self, page: int = 1, per_page: int = 10):
        db = Database()
        c = db.connect()
        offset = (page - 1) * per_page
        c.execute(
            "SELECT rowid, * FROM submissions WHERE crosspost_of IS NULL ORDER BY rowid ASC LIMIT ? OFFSET ?",  # Update the query
            (per_page, offset),
        )
        submission_tuples = c.fetchall()
        db.disconnect()
        sub_rowids = []
        submissions = []
        submissions_by_rowid = {}
        for submission_tuple in submission_tuples:
            submission = RedditPostPayload.from_tuple(submission_tuple)
            submissions_by_rowid[submission.rowid] = submission

        sub_rowids = list(submissions_by_rowid.keys())

        if len(sub_rowids) > 0:
            sql = "select rowid, * from submissions where crosspost_of in ({seq}) LIMIT 900".format(
                seq=",".join(["?"] * len(sub_rowids))
            )
            c = db.connect()
            c.execute(
                sql,
                sub_rowids,
            )
            crosspost_submission_tuples = c.fetchall()
            db.disconnect()

            for crosspost_submission_tuple in crosspost_submission_tuples:
                crosspost_submission = RedditPostPayload.from_tuple(
                    crosspost_submission_tuple
                )
                crosspost_request = CrosspostRequestPayload(
                    sub=crosspost_submission.sub,
                    planned_unix_datetime=crosspost_submission.planned_unix_datetime,
                )
                submissions_by_rowid[
                    crosspost_submission.crosspost_of
                ].crosspost_requests.append(crosspost_request)

        submissions = list(submissions_by_rowid.values())
        return submissions

    def check_scheduled_submissions(self):
        try:
            db = Database()
            c = db.connect()
            c.execute(
                "SELECT rowid, * FROM submissions WHERE status = 'wait' AND planned_unix_datetime <= ?",
                (time.time(),),
            )
            submission_tuples = c.fetchall()
            db.disconnect()

            submissions = []
            for submission_tuple in submission_tuples:
                submission = RedditPostPayload.from_tuple(submission_tuple)
                submissions.append(submission)

            self._post_scheduled_submissions(submissions)
        except Exception as e:
            print(e)

    def _post_scheduled_submissions(
        self, submissions: List[RedditPostPayload]
    ):
        for submission in submissions:
            print("trying to post a submission. Title: " + submission.title)
            self._post_submission(submission)

    def _post_submission(self, submission: RedditPostPayload):
        if submission.status == "wait":
            submission.status = "posting"
            self.update_submission(submission)
            try:
                if not submission.crosspost_of:
                    reddit_manager = RedditManager()
                    reddit_manager.set_user(submission.username)
                    submission_id = reddit_manager.create_submission(
                        sub=submission.sub,
                        title=submission.title,
                        text=submission.text,
                        link=submission.link,
                        image=submission.image_name,
                        video=submission.video,
                        flairid=submission.flairid,
                        nsfw=bool(submission.nsfw),
                    )
                    submission.submission_id = submission_id
                    self.update_submission(submission)
                else:
                    # TODO: get original submission, and submit crosspost
                    parent_submission = self.read_submission(
                        rowid=submission.crosspost_of
                    )
                    if (
                        parent_submission is not None
                        and parent_submission.submission_id is not None
                    ):
                        reddit_manager = RedditManager()
                        reddit_manager.set_user(submission.username)
                        reddit_manager.create_crosspost(
                            parent_submission_id=parent_submission.submission_id,
                            target_sub=submission.sub,
                        )

            except Exception as e:
                print(e)
                submission.status = "error"
                self.update_submission(submission)
                return
            submission.status = "posted"
            # TODO: save created submission id as well.
            self.update_submission(submission)
