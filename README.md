# Bookmarks App

A modern Python + Streamlit application to manage bookmarks with a beautiful UI. Bookmarks are stored in a SQLite database.

## Features
- Add, view, edit, and delete bookmarks
- Search bookmarks by tag with a clear/reset button
- Modern sidebar navigation (radio buttons)
- Edit and delete icons inline with each bookmark link
- Description preview (first 3 lines shown)
- Responsive, clean UI with custom styles

## Requirements
- Python 3.x
- See `requirements.txt` for dependencies

## Usage
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   streamlit run app.py
   ```

## Notes
- The database file `bookmarks.db` is excluded from version control.
- The virtual environment directory `.venv` is also excluded.

## License
MIT
