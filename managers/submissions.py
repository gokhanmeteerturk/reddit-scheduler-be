from cursor import Database
from payloads import RedditPostPayload


class SubmissionsManager:
    def create_submission(self, submission: RedditPostPayload):
        db = Database()
        c = db.connect()
        c.execute(
            "INSERT INTO submissions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
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
                None, # crosspost_of,
                submission.submission_id,
            ),
        )
        submission_rowid = c.lastrowid
        db.connection.commit()

        if submission.crosspost_requests:
            self._handle_crosspost_requests(submission, submission_rowid)

        db.disconnect()
        return {"result": "Success"}

    def _handle_crosspost_requests(self, submission: RedditPostPayload, submission_rowid: int):
        for crosspost_request in submission.crosspost_requests:
            db = Database()
            c = db.connect()
            c.execute(
                "INSERT INTO submissions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    crosspost_request.planned_unix_datetime,
                    "wait",  # initial status
                    submission.username,
                    crosspost_request.sub,
                    submission.title,
                    None,submission.text,
                    None, # submission.link,
                    None, # submission.image_name,
                    None, # submission.video,
                    None, # submission.flairid,
                    submission.nsfw,
                    submission_rowid,
                    submission.submission_id,
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
                None, # crosspost_of,
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
            "SELECT rowid, * FROM submissions ORDER BY rowid ASC LIMIT ? OFFSET ?",  # Update the query
            (per_page, offset),
        )
        submission_tuples = c.fetchall()
        db.disconnect()

        submissions = []
        for submission_tuple in submission_tuples:
            submission = RedditPostPayload.from_tuple(submission_tuple)
            submissions.append(submission)

        return submissions

    def check_scheduled_submissions(self):
        try:
            # Find and handle scheduled submissions
            pass
        except Exception as e:
            print(e)
