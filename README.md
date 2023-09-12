# Reddit Scheduler Backend
A very convenient reddit scheduler backend with support for multiple credentials

## Development Status

- [x] ~~CRUD operations for owned Reddit user credentials~~
- [x] ~~CRUD operations for scheduling submissions~~
- [x] ~~Repeating task to trigger submissions on scheduled date~~
- [x] ~~Dockerization of the project (Work in progress)~~
- [x] ~~SSL support (now possible via nginx proxy etc)~~


## Installation
Just clone the repo, create a python environment and install the dependencies:
`pip install -r requirements.txt`

Or use Docker:
`docker compose up -d`

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

### Users

| Endpoint | HTTP Method | Description |
| --- | --- | --- |
| reddit_users/ | ![GET](https://img.shields.io/badge/GET-blue?style=flat-square)  | Get all saved users |
| reddit_users/{USER}/ | ![GET](https://img.shields.io/badge/GET-blue?style=flat-square) | Get specific user |
| reddit_users/ | ![POST](https://img.shields.io/badge/POST-forestgreen?style=flat-square) | Save a new user |
| reddit_users/{USER}/ | ![PUT](https://img.shields.io/badge/PUT-darkgoldenrod?style=flat-square) | Update user information |
| reddit_users/{USER}/ | ![DELETE](https://img.shields.io/badge/DELETE-firebrick?style=flat-square) | Delete a user |

### Submissions

| Endpoint | HTTP Method | Description |
| --- | --- | --- |
| scheduled_submissions/ | ![GET](https://img.shields.io/badge/GET-blue?style=flat-square) | Get all scheduled submissions |
| scheduled_submissions/{SUBMISSION_ROWID}/ | ![GET](https://img.shields.io/badge/GET-blue?style=flat-square) | Get details of a specific submission |
| scheduled_submissions/ | ![POST](https://img.shields.io/badge/POST-forestgreen?style=flat-square) | Schedule a new submission |
| scheduled_submissions/{SUBMISSION_ROWID}/ | ![PUT](https://img.shields.io/badge/PUT-darkgoldenrod?style=flat-square) | Update a scheduled submission |
| scheduled_submissions/{SUBMISSION_ROWID}/ | ![DELETE](https://img.shields.io/badge/DELETE-firebrick?style=flat-square) | Delete a scheduled submission |

---

## API Parameters, Payloads and Examples

### 0. Axios Examples

See [Examples For Axios](examples/axios.md).


### 1. Get all saved users

<table>
  <tr>
    <th>HTTP Method</th>
    <td>GET</td>
  </tr>
  <tr>
    <th>Endpoint</th>
    <td>/reddit_users/</td>
  </tr>
  <tr>
    <th>Parameters</th>
    <td>page, per_page</td>
  </tr>
  <tr>
    <th>Example</th>
    <td>

```bash
curl -L 'http://127.0.0.1:8080/reddit_users/?page=1&per_page=10' \
-H 'Authorization: Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA'
```

   </td>
  </tr>
</table>

### 2. Get specific user

<table>
  <tr>
    <th>HTTP Method</th>
    <td>GET</td>
  </tr>
  <tr>
    <th>Endpoint</th>
    <td>/reddit_users/{USER}/</td>
  </tr>
  <tr>
    <th>Parameters</th>
    <td>with_crosspostable_subs (bool)</td>
  </tr>
  <tr>
    <th>Example</th>
    <td>

```bash
curl -L 'http://127.0.0.1:8080/reddit_users/spez/' \
-H 'Authorization: Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA'
```

   </td>
  </tr>
</table>

### 3. Create a new user

<table>
  <tr>
    <th>HTTP Method</th>
    <td>POST</td>
  </tr>
  <tr>
    <th>Endpoint</th>
    <td>/reddit_users/</td>
  </tr>
  <tr>
    <th>Example</th>
    <td>

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

   </td>
  </tr>
</table>

### 4. Update user information

<table>
  <tr>
    <th>HTTP Method</th>
    <td>PUT</td>
  </tr>
  <tr>
    <th>Endpoint</th>
    <td>/reddit_users/{USER}/</td>
  </tr>
  <tr>
    <th>Example</th>
    <td>

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

   </td>
  </tr>
</table>

### 5. Delete a user

<table>
  <tr>
    <th>HTTP Method</th>
    <td>DELETE</td>
  </tr>
  <tr>
    <th>Endpoint</th>
    <td>/reddit_users/{USER}/</td>
  </tr>
  <tr>
    <th>Example</th>
    <td>

```bash
curl -L -X DELETE 'http://127.0.0.1:8080/reddit_users/spez/' \
-H 'Authorization: Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA'
```

   </td>
  </tr>
</table>

### 6. Get all scheduled submissions

<table>
  <tr>
    <th>HTTP Method</th>
    <td>GET</td>
  </tr>
  <tr>
    <th>Endpoint</th>
    <td>/scheduled_submissions/</td>
  </tr>
  <tr>
    <th>Parameters</th>
    <td>page, per_page</td>
  </tr>
  <tr>
    <th>Example</th>
    <td>

```bash
curl -L 'http://127.0.0.1:8080/scheduled_submissions/?page=1&per_page=10' \
-H 'Authorization: Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA'
```

   </td>
  </tr>
</table>

### 7. Schedule a new submission

<table>
  <tr>
    <th>HTTP Method</th>
    <td>POST</td>
  </tr>
  <tr>
    <th>Endpoint</th>
    <td>/scheduled_submissions/</td>
  </tr>
  <tr>
    <th>Example</th>
    <td>

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
    "nsfw": false,
    "crosspost_requests":[
        {
            "sub":"EtsyMemes",
            "planned_unix_datetime":1753877470
        }
    ]
}'
```

   </td>
  </tr>
</table>

### 8. Get details of a specific submission

<table>
  <tr>
    <th>HTTP Method</th>
    <td>GET</td>
  </tr>
  <tr>
    <th>Endpoint</th>
    <td>/scheduled_submissions/{SUBMISSION_ROWID}/</td>
  </tr>
  <tr>
    <th>Example</th>
    <td>

```bash
curl -L 'http://127.0.0.1:8080/scheduled_submissions/1/' \
-H 'Authorization: Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA'
```

   </td>
  </tr>
</table>

### 9. Update a scheduled submission

<table>
  <tr>
    <th>HTTP Method</th>
    <td>

PUT</td>
  </tr>
  <tr>
    <th>Endpoint</th>
    <td>/scheduled_submissions/{SUBMISSION_ROWID}/</td>
  </tr>
  <tr>
    <th>Example</th>
    <td>

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

   </td>
  </tr>
</table>

### 10. Delete a scheduled submission

<table>
  <tr>
    <th>HTTP Method</th>
    <td>DELETE</td>
  </tr>
  <tr>
    <th>Endpoint</th>
    <td>/scheduled_submissions/{SUBMISSION_ROWID}/</td>
  </tr>
  <tr>
    <th>Example</th>
    <td>

```bash
curl -L -X DELETE 'http://127.0.0.1:8080/scheduled_submissions/1/' \
-H 'Authorization: Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA'
```

   </td>
  </tr>
</table>


---

Please remember to replace the placeholders such as `{USER}` and `{SUBMISSION_ROWID}` with actual values in your requests. This documentation should provide a clear overview of the API endpoints and how to interact with them professionally.


