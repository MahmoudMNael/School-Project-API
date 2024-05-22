<h1> Authentication API </h1>

### POST /api/auth/register/

Registers a new user.

Request

```JSON
{
    "email": "testuser@example.com",
    "full_name": "Test User",
    "password": "testpassword",
    "role": "student"
}
```

Response

```json
{
	"id": 1,
	"email": "testuser@example.com",
	"full_name": "Test User",
	"role": "student",
	"is_pending": true
}
```

### POST /api/auth/login/

Logs in a user.

Request

```json
{
	"email": "testuser@example.com",
	"password": "testpassword"
}
```

Response

```json
{
	"message": "user logged in"
}
```

### GET /api/auth/profile/

Response

```json
{
	"id": 1,
	"email": "testuser@example.com",
	"full_name": "Test User",
	"role": "student",
	"is_pending": false
}
```

### GET /api/auth/pending/

Response

```json
[
	{
		"id": 1,
		"email": "testuser@example.com",
		"full_name": "Test User",
		"role": "student",
		"is_pending": true
	},
	...
]
```

### POST /api/auth/pending/`int:user_id`/

Response

```json
{
	"message": "user approved"
}
```

### DELETE /api/auth/pending/`int:user_id`/

Response

```json
{
	"message": "user rejected"
}
```
