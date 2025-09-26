# Mini Blog API (Tier 1 — In-Memory)

# Mini Blog API (Tier 1 — In-Memory)


📝 Project Overview

Mini Blog API is a Django REST Framework (DRF) project that allows users to:

Create, update, delete, and fetch blog posts.

Add comments to posts, and manage (update/delete) their comments.

Supports pagination and returns posts in reverse chronological order (latest first).

Includes authentication for secure operations.


⚙️ Setup Instructions
1. Clone Repository
git clone https://github.com/<YOUR-USERNAME>/MiniBlogAPI.git
cd MiniBlogAPI


2. Create & Activate Virtual Environment
# Windows (cmd)
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt


4. Run Development Server
python manage.py runserver


API will be available at:
👉 http://127.0.0.1:8000/api/




🚀 API Endpoints
🔹 Posts
Method	Endpoint	Description	Auth Required
GET	/api/posts/	List all posts (latest first, paginated)	❌ No
POST	/api/posts/	Create a new post	✅ Yes
GET	/api/posts/<id>/	Retrieve a single post + comments	❌ No
PUT	/api/posts/<id>/	Update a post (only author)	✅ Yes
DELETE	/api/posts/<id>/	Delete a post (only author)	✅ Yes
🔹 Comments
Method	Endpoint	Description	Auth Required
POST	/api/posts/<id>/comments/	Add comment to a post	✅ Yes
PUT	/api/comments/<id>/	Update a comment (author)	✅ Yes
DELETE	/api/comments/<id>/	Delete a comment (author)	✅ Yes



## 📌 Example Requests & Responses

### 1. List Posts (Initially Empty)
**Request:**
```
GET http://127.0.0.1:8000/api/posts/
```
**Response:**
```json
[]
```

---

### 2. Create Post (Authentication Required)
**Request:**
```
POST http://127.0.0.1:8000/api/posts/
Headers:
  Authorization: Token abc123
  Content-Type: application/json

Body:
{
  "title": "Introduction to Mini Blog",
  "content": "This is the first test post to verify the API functionality."
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Introduction to Mini Blog",
  "content": "This is the first test post to verify the API functionality.",
  "author": 1,
  "created_at": "2025-09-24T18:27:35.071049Z"
}
```

**Unauthorized Example:**
```json
{
  "detail": "Authentication required"
}
```
Status: `401 Unauthorized`

---

### 3. Add Comment to a Post (Authentication Required)
**Request:**
```
POST http://127.0.0.1:8000/api/posts/3/comments/
Headers:
  Authorization: Token abc123
  Content-Type: application/json

Body:
{
  "text": "Nice post!"
}
```

**Response:**
```json
{
  "id": 1,
  "post": 3,
  "text": "Nice post!",
  "author": 1,
  "created_at": "2025-09-24T18:32:03.841280Z"
}
```

---

### 4. List All Posts (Latest-First)
**Request:**
```
GET http://127.0.0.1:8000/api/posts/
```
**Response:**
```json
[
  {
    "id": 6,
    "title": "Final Post",
    "content": "Final post to check that latest posts appear first and pagination works.",
    "author": 1,
    "created_at": "2025-09-24T18:29:13.167681Z"
  },
  {
    "id": 5,
    "title": "Pagination Test",
    "content": "We are now testing pagination using multiple posts.",
    "author": 1,
    "created_at": "2025-09-24T18:29:04.241767Z"
  }
]
```

---

### 5. Get Single Post with Comments
**Request:**
```
GET http://127.0.0.1:8000/api/posts/3/
```
**Response:**
```json
{
  "id": 3,
  "title": "API Authentication",
  "content": "Checking that unauthorized requests fail and authorized requests succeed.",
  "author": 1,
  "created_at": "2025-09-24T18:28:45.378235Z",
  "comments": [
    {
      "id": 1,
      "post": 3,
      "text": "Nice post!",
      "author": 1,
      "created_at": "2025-09-24T18:32:03.841280Z"
    }
  ]
}
```

---

### 6. Pagination Example
**Request:**
```
GET http://127.0.0.1:8000/api/posts/?page=1&page_size=5
```
**Response:**
```json
[
  {
    "id": 6,
    "title": "Final Post",
    "content": "Final post to check that latest posts appear first and pagination works.",
    "author": 1,
    "created_at": "2025-09-24T18:29:13.167681Z"
  },
  {
    "id": 5,
    "title": "Pagination Test",
    "content": "We are now testing pagination using multiple posts.",
    "author": 1,
    "created_at": "2025-09-24T18:29:04.241767Z"
  }
]
```

---

### 7. Input Validation (Empty Title)
**Request:**
```
POST http://127.0.0.1:8000/api/posts/
Headers:
  Authorization: Token abc123
  Content-Type: application/json

Body:
{
  "title": "",
  "content": "Hello world!"
}
```

**Response:**
```json
{"title":"Title is required."}
```

---

### 8. Input Validation (Empty Content)
**Request:**
```
POST http://127.0.0.1:8000/api/posts/
Headers:
  Authorization: Token abc123
  Content-Type: application/json

Body:
{
  "title": "Shubham Vharamble",
  "content": ""
}
```

**Response:**
```json
{"content":"Content is required."}
```

---

## ✅ Features Implemented
- Input validation (title & content required, non-empty).
- Authentication with token (`abc123`).
- Posts ordered latest first.
- Pagination (`?page=1&page_size=5`).
- Comment system.
- Clean, readable code with comments.
