# Examples using Axios

## 1. Get all saved users
<table>
<tr>
<th>HTTP Method</th>
<td>

![GET](https://img.shields.io/badge/GET-blue?style=flat-square)
</td>
</tr>
<tr>
<th>Endpoint</th>
<td>/reddit_users/</td>
</tr>
<tr>
<th>Example</th>
<td>

```js
const axios = require('axios');

axios.get('http://127.0.0.1:8080/reddit_users/', {
  headers: {
    Authorization: 'Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA',
  },
})
  .then(response => console.log(response.data))
  .catch(error => console.error(error));
```

</td>
</tr>
</table>

## 2. Get specific user
<table>
<tr>
<th>HTTP Method</th>
<td>

![GET](https://img.shields.io/badge/GET-blue?style=flat-square)
</td>
</tr>
<tr>
<th>Endpoint</th>
<td>/reddit_users/{USER}/</td>
</tr>
<tr>
<th>Example</th>
<td>

```js
const axios = require('axios');

axios.get('http://127.0.0.1:8080/reddit_users/spez/', {
  headers: {
    Authorization: 'Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA',
  },
})
  .then(response => console.log(response.data))
  .catch(error => console.error(error));
```

</td>
</tr>
</table>

## 3. Create a new user
<table>
<tr>
<th>HTTP Method</th>
<td>

![POST](https://img.shields.io/badge/POST-forestgreen?style=flat-square)
</td>
</tr>
<tr>
<th>Endpoint</th>
<td>/reddit_users/</td>
</tr>
<tr>
<th>Example</th>
<td>

```js
const axios = require('axios');

axios.post('http://127.0.0.1:8080/reddit_users/', {
  username: 'new_user',
  password: 'new_password',
  client_id: 'new_client_id',
  client_secret: 'new_client_secret',
}, {
  headers: {
    Authorization: 'Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA',
    'Content-Type': 'application/json',
  },
})
  .then(response => console.log(response.data))
  .catch(error => console.error(error));
```

</td>
</tr>
</table>

## 4. Update user information
<table>
<tr>
<th>HTTP Method</th>
<td>

![PUT](https://img.shields.io/badge/PUT-darkgoldenrod?style=flat-square)
</td>
</tr>
<tr>
<th>Endpoint</th>
<td>/reddit_users/{USER}/</td>
</tr>
<tr>
<th>Example</th>
<td>

```js
const axios = require('axios');

axios.put('http://127.0.0.1:8080/reddit_users/spez/', {
  username: 'spez',
  password: 'new_password',
  client_id: 'new_client_id',
  client_secret: 'new_client_secret',
}, {
  headers: {
    Authorization: 'Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA',
    'Content-Type': 'application/json',
  },
})
  .then(response => console.log(response.data))
  .catch(error => console.error(error));
```

</td>
</tr>
</table>

## 5. Delete a user
<table>
<tr>
<th>HTTP Method</th>
<td>

![DELETE](https://img.shields.io/badge/DELETE-firebrick?style=flat-square)
</td>
</tr>
<tr>
<th>Endpoint</th>
<td>/reddit_users/{USER}/</td>
</tr>
<tr>
<th>Example</th>
<td>

```js
const axios = require('axios');

axios.delete('http://127.0.0.1:8080/reddit_users/spez/', {
  headers: {
    Authorization: 'Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA',
  },
})
  .then(response => console.log(response.data))
  .catch(error => console.error(error));
```

</td>
</tr>
</table>

## 6. Get all scheduled submissions
<table>
<tr>
<th>HTTP Method</th>
<td>

![GET](https://img.shields.io/badge/GET-blue?style=flat-square)
</td>
</tr>
<tr>
<th>Endpoint</th>
<td>/scheduled_submissions/</td>
</tr>
<tr>
<th>Example</th>
<td>

```js
const axios = require('axios');

axios.get('http://127.0.0.1:8080/scheduled_submissions/', {
  headers: {
    Authorization: 'Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA',
  },
})
  .then(response => console.log(response.data))
  .catch(error => console.error(error));
```

</td>
</tr>
</table>

## 7. Schedule a new submission
<table>
<tr>
<th>HTTP Method</th>
<td>

![POST](https://img.shields.io/badge/POST-forestgreen?style=flat-square)
</td>
</tr>
<tr>
<th>Endpoint</th>
<td>/scheduled_submissions/</td>
</tr>
<tr>
<th>Example</th>
<td>

```js
const axios = require('axios');

axios.post('http://127.0.0.1:8080/scheduled_submissions/', {
  username: 'spez',
  planned_unix_datetime: 1753876468,
  sub: 'ProgrammerHumor',
  title: 'New submission',
  text: 'Lorem ipsum dolor sit down',
  flairid: null,
  nsfw: false,
  crosspost_requests: [{
    sub: 'EtsyMemes',
    planned_unix_datetime: 1753877470,
  }],
}, {
  headers: {
    Authorization: 'Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA',
    'Content-Type': 'application/json',
  },
})
  .then(response => console.log(response.data))
  .catch(error => console.error(error));
```

</td>
</tr>
</table>

## 8. Get details of a specific submission
<table>
<tr>
<th>HTTP Method</th>
<td>

![GET](https://img.shields.io/badge/GET-blue?style=flat-square)
</td>
</tr>
<tr>
<th>Endpoint</th>
<td>/scheduled_submissions/{SUBMISSION_ROWID}/</td>
</tr>
<tr>
<th>Example</th>
<td>

```js
const axios = require('axios');

axios.get('http://127.0.0.1:8080/scheduled_submissions/1/', {
  headers: {
    Authorization: 'Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA',
  },
})
  .then(response => console.log(response.data))
  .catch(error => console.error(error));
```

</td>
</tr>
</table>

## 9. Update a scheduled submission
<table>
<tr>
<th>HTTP Method</th>
<td>

![PUT](https://img.shields.io/badge/PUT-darkgoldenrod?style=flat-square)
</td>
</tr>
<tr>
<th>Endpoint</th>
<td>/scheduled_submissions/{SUBMISSION_ROWID}/</td>
</tr>
<tr>
<th>Example</th>
<td>

```js
const axios = require('axios');

axios.put('http://127.0.0.1:8080/scheduled_submissions/1/', {
  username: 'spez',
  planned_unix_datetime: 1753876468,
  sub: 'ProgrammerHumor',
  title: 'Updated submission',
  text: 'Lorem ipsum dolor sit down',
  flairid: null,
  nsfw: false,
}, {
  headers: {
    Authorization: 'Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA',
    'Content-Type': 'application/json',
  },
})
  .then(response => console.log(response.data))
  .catch(error => console.error(error));
```

</td>
</tr>
</table>

## 10. Delete a scheduled submission
<table>
<tr>
<th>HTTP Method</th>
<td>

![DELETE](https://img.shields.io/badge/DELETE-firebrick?style=flat-square)
</td>
</tr>
<tr>
<th>Endpoint</th>
<td>/scheduled_submissions/{SUBMISSION_ROWID}/</td>
</tr>
<tr>
<th>Example</th>
<td>

```js
const axios = require('axios');

axios.delete('http://127.0.0.1:8080/scheduled_submissions/1/', {
  headers: {
    Authorization: 'Basic cAebyYIUtX-3urYrp05_GlxtrVgLUKX7rQxDBdG5mGA',
  },
})
  .then(response => console.log(response.data))
  .catch(error => console.error(error));
```

</td>
</tr>
</table>
```

Make sure to replace the placeholders such as `{USER}` and `{SUBMISSION_ROWID}` with the actual values in your requests.