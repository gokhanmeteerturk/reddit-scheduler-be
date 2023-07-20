# reddit-scheduler-be
A very convenient reddit scheduler backend with support for multiple credentials

## WARNING: WORK IN PROGRESS

## Installation

First, run the server:
`uvicorn main:app --port 8080 --reload`

Get your master key by sending a GET request to:

    http://127.0.0.1:8080/init/


Once the request is completed, you will receive a master key in return:

```json

{
    "master_key": "yYIUt5FAdb-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA"
}

```

This will only work once.
Once created, you won't be able to view your master key again. Following requests will result in 404. In order to create a new key, you will need to delete the "db.sqlite3" file manually.


