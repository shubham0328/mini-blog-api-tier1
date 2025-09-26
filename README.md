# Mini Blog API (Tier 1 — In-Memory)

## 📌 Setup Instructions

### 1. Create & activate virtual environment
- **Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```
or
```powershell
.venv\Scripts\activate
```

- **Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies
```bash
pip install django djangorestframework
```

### 3. Run the development server
```bash
python manage.py runserver
```

---

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
