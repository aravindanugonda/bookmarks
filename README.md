# Bookmarks App (Turso Edition)

A modern Python + Streamlit application to manage bookmarks with a beautiful UI. Bookmarks are stored in a Turso cloud database using the HTTP API.

## Features
- Add, view, edit, and delete bookmarks
- Search bookmarks by tag with a clear/reset button
- Modern sidebar navigation (radio buttons)
- Edit and delete icons inline with each bookmark link
- Description preview (first 3 lines shown)
- Responsive, clean UI with custom styles
- **Multi-user authentication**: Each user logs in with their own email and password (set via environment variables)
- **User isolation**: Each user only sees and manages their own bookmarks
- **Cloud-native**: Uses Turso HTTP API (no local SQLite)

## Requirements
- Python 3.8+
- See `requirements.txt` for dependencies
- A Turso database (see below)

## Setup
1. **Create a Turso database** ([Turso Console](https://console.turso.tech/))
2. **Create a Turso auth token** for your database
3. **Create a `.env` file** in the project root with:
   ```env
   TURSO_DB_URL="https://<your-db-name>-<org>.turso.io"
   TURSO_DB_AUTH_TOKEN=<your-turso-token>
   USER1_CRED="user1@example.com:password1"
   USER2_CRED="user2@example.com:password2"
   USER3_CRED="user3@example.com:password3"
   ```
   - Replace values with your actual Turso DB URL, token, and user credentials. The URL must start with `https://` for the HTTP API.

4. **Update your database schema:**
   - Add a `user_email` column to your bookmarks table:
     ```sql
     ALTER TABLE bookmarks ADD COLUMN user_email TEXT;
     ```
   - For existing bookmarks, associate them with a user:
     ```sql
     UPDATE bookmarks SET user_email = 'user1@example.com';
     ```
     (Repeat for each user as needed.)

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Run the app:**
   ```bash
   streamlit run app.py
   ```

7. **Login:**
   - When prompted, enter your email and password as set in the `.env` file.

## Turso Table Schema
Create this table in your Turso database before running the app:
```sql
CREATE TABLE bookmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    description TEXT,
    tags TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_email TEXT
);
```

## Deployment
- Works on [Render.com](https://render.com/) and other cloud platforms.
- Set the same environment variables (`TURSO_DB_URL`, `TURSO_DB_AUTH_TOKEN`, `USER1_CRED`, etc.) in your deployment settings.

## Notes
- This app uses the Turso HTTP API `/v2/pipeline` endpoint for all SQL operations.
- No local database is used or created.
- `.env` is for local development only; use environment variables in production.

## License
MIT
