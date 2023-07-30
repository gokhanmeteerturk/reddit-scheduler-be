# reddit-scheduler-be
A very convenient reddit scheduler backend with support for multiple credentials

## WARNING: WORK IN PROGRESS
## Development Status

- [x] CRUD operations for owned Reddit user credentials
- [x] CRUD operations for scheduling submissions
- [ ] Repeating task to trigger submissions on scheduled date (Work in progress)
- [ ] SSL support (Not started)
- [ ] Dockerization of the project (Not started)


## Installation
Just clone the repo, create a python environment and install the dependencies:
`pip install -r requirements.txt`

## Setup

First, run the server:
`uvicorn main:app --port 8080 --reload`

Get your master key by sending a GET request to:

    http://127.0.0.1:8080/init/

Once the request is completed, you will receive a master key in return:

```json
{
 "master_key": "cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA"
}
```

This will only work once.
Once created, you won't be able to view your master key again. Following requests will result in 404. In order to create a new key, you will need to delete the "db.sqlite3" file manually.

# Usage

API is simple and follows REST best practices. You will need to send a request with a valid master key in the "Authorization" header.

In case you still need a detailed documentation, below you can find a table showcasing the endpoints and their corresponding HTTP methods. As well as the examples of how to use the API for each endpoint.

---

## API Endpoints

| Endpoint | HTTP Method | Description |
| --- | --- | --- |
| reddit_users/ | GET | Get all saved users |
| reddit_users/{USER}/ | GET | Get specific user |
| reddit_users/ | POST | Save a new user |
| reddit_users/{USER}/ | PUT | Update user information |
| reddit_users/{USER}/ | DELETE | Delete a user |
| scheduled_submissions/ | GET | Get all scheduled submissions |
| scheduled_submissions/ | POST | Schedule a new submission |
| scheduled_submissions/{SUBMISSION_ROWID}/ | GET | Get details of a specific submission |
| scheduled_submissions/{SUBMISSION_ROWID}/ | PUT | Update a scheduled submission |
| scheduled_submissions/{SUBMISSION_ROWID}/ | DELETE | Delete a scheduled submission |

---

## API Examples

### 1. Get all saved users
**HTTP Method:** GET
**Endpoint:** /reddit_users/

**Example:**
```bash
curl -L 'http://127.0.0.1:8080/reddit_users/' \
-H 'Authorization: Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA'
```

### 2. Get specific user
**HTTP Method:** GET
**Endpoint:** /reddit_users/{USER}/

**Example:**
```bash
curl -L 'http://127.0.0.1:8080/reddit_users/spez/' \
-H 'Authorization: Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA'
```

### 3. Create a new user
**HTTP Method:** POST
**Endpoint:** /reddit_users/

**Example:**
```bash
curl -L 'http://127.0.0.1:8080/reddit_users/' \
-H 'Authorization: Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA' \
-H 'Content-Type: application/json' \
-d '{
    "username": "new_user",
    "password": "new_password",
    "client_id": "new_client_id",
    "client_secret": "new_client_secret"
}'
```

### 4. Update user information
**HTTP Method:** PUT
**Endpoint:** /reddit_users/{USER}/

**Example:**
```bash
curl -L -X PUT 'http://127.0.0.1:8080/reddit_users/spez/' \
-H 'Authorization: Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA' \
-H 'Content-Type: application/json' \
-d '{
    "username": "spez",
    "password": "new_password",
    "client_id": "new_client_id",
    "client_secret": "new_client_secret"
}'
```

### 5. Delete a user
**HTTP Method:** DELETE
**Endpoint:** /reddit_users/{USER}/

**Example:**
```bash
curl -L -X DELETE 'http://127.0.0.1:8080/reddit_users/spez/' \
-H 'Authorization: Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA'
```

### 6. Get all scheduled submissions
**HTTP Method:** GET
**Endpoint:** /scheduled_submissions/

**Example:**
```bash
curl -L 'http://127.0.0.1:8080/scheduled_submissions/' \
-H 'Authorization: Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA'
```

### 7. Schedule a new submission
**HTTP Method:** POST
**Endpoint:** /scheduled_submissions/

**Example:**
```bash
curl -L 'http://127.0.0.1:8080/scheduled_submissions/' \
-H 'Authorization: Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA' \
-H 'Content-Type: application/json' \
-d '{
    "username": "spez",
    "planned_unix_datetime": 1753876468,
    "sub": "ProgrammerHumor",
    "title": "New submission",
    "text": "Lorem ipsum dolor sit down",
    "flairid": null,
    "nsfw": false
}'
```

### 8. Get details of a specific submission
**HTTP Method:** GET
**Endpoint:** /scheduled_submissions/{SUBMISSION_ROWID}/

**Example:**
```bash
curl -L 'http://127.0.0.1:8080/scheduled_submissions/1/' \
-H 'Authorization: Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA'
```

### 9. Update a scheduled submission
**HTTP Method:** PUT
**Endpoint:** /scheduled_submissions/{SUBMISSION_ROWID}/

**Example:**
```bash
curl -L -X PUT 'http://127.0.0.1:8080/scheduled_submissions/1/' \
-H 'Authorization: Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA' \
-H 'Content-Type: application/json' \
-d '{
    "username": "spez",
    "planned_unix_datetime": 1753876468,
    "sub": "ProgrammerHumor",
    "title": "Updated submission",
    "text": "Lorem ipsum dolor sit down",
    "flairid": null,
    "nsfw": false
}'
```

### 10. Delete a scheduled submission
**HTTP Method:** DELETE
**Endpoint:** /scheduled_submissions/{SUBMISSION_ROWID}/

**Example:**
```bash
curl -L -X DELETE 'http://127.0.0.1:8080/scheduled_submissions/1/' \
-H 'Authorization: Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA'
```

---

Please remember to replace the placeholders such as `{USER}` and `{SUBMISSION_ROWID}` with actual values in your requests. This documentation should provide a clear overview of the API endpoints and how to interact with them professionally.


