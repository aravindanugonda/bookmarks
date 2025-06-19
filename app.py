# Streamlit Bookmark Manager
# This app allows users to add, view, and manage browser bookmarks using a Turso (SQLite) database.

import streamlit as st
import sqlite3
import os

# --- Turso DB connection setup ---
# You need to set TURSO_DB_URL and TURSO_DB_AUTH_TOKEN as environment variables
TURSO_DB_URL = os.getenv("TURSO_DB_URL")
TURSO_DB_AUTH_TOKEN = os.getenv("TURSO_DB_AUTH_TOKEN")

# For demonstration, we use sqlite3. For production, use Turso's HTTP API or client.
def get_connection():
    # Replace this with Turso's connection logic or HTTP API
    # Example: Use requests to interact with Turso HTTP API
    # For now, fallback to local SQLite for development
    return sqlite3.connect("bookmarks.db")

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bookmarks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        url TEXT NOT NULL,
        description TEXT,
        tags TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

init_db()

# Change sidebar menu to radio buttons
menu = ["Add Bookmark", "View Bookmarks"]
choice = st.sidebar.radio("Menu", menu, index=1)

# Helper to fetch bookmarks (with optional tag search)
def fetch_bookmarks(tag_query=None):
    conn = get_connection()
    c = conn.cursor()
    if tag_query:
        c.execute("SELECT id, title, url, description, tags, created_at FROM bookmarks WHERE tags LIKE ? ORDER BY created_at DESC", (f"%{tag_query}%",))
    else:
        c.execute("SELECT id, title, url, description, tags, created_at FROM bookmarks ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    return rows

# Helper to update a bookmark
def update_bookmark(bid, title, url, description, tags):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE bookmarks SET title=?, url=?, description=?, tags=? WHERE id=?", (title, url, description, tags, bid))
    conn.commit()
    conn.close()

# Helper to delete a bookmark
def delete_bookmark(bid):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM bookmarks WHERE id=?", (bid,))
    conn.commit()
    conn.close()

st.markdown('''
    <style>
    body {
        background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
        font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .colorful-header {
        background: linear-gradient(90deg, #6366f1 0%, #06b6d4 100%);
        color: #fff;
        border-radius: 16px;
        padding: 0.7rem 1.2rem 0.7rem 1.2rem; /* Even less padding */
        margin-bottom: 0.5rem; /* Even less margin */
        font-size: 2.1rem;
        font-weight: 700;
        letter-spacing: 1px;
        box-shadow: 0 4px 24px #b0b0b0;
        text-align: center;
    }
    .bookmark-card {
        background: #fff;
        border-radius: 14px;
        box-shadow: 0 4px 16px #e0e0e0;
        padding: 22px 28px 14px 28px;
        margin-bottom: 28px;
        border-left: 8px solid #06b6d4;
        transition: box-shadow 0.2s, border 0.2s;
        position: relative;
    }
    .bookmark-card:hover {
        box-shadow: 0 8px 32px #a5b4fc;
        border-left: 8px solid #6366f1;
    }
    .bookmark-title {
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 0.3em;
        color: #2563eb;
        display: flex;
        align-items: center;
    }
    .bookmark-title a {
        color: #2563eb;
        text-decoration: none;
    }
    .bookmark-title a:hover {
        color: #06b6d4;
    }
    .bookmark-desc {
        color: #334155;
        margin-bottom: 0.7em;
        font-size: 1.07rem;
    }
    .tag-pill {
        background: linear-gradient(90deg, #a5b4fc 0%, #67e8f9 100%);
        color: #0e7490;
        border-radius: 16px;
        padding: 4px 14px 4px 10px;
        margin-right: 7px;
        font-size: 1em;
        display: inline-flex;
        align-items: center;
        margin-bottom: 2px;
        font-weight: 500;
        box-shadow: 0 2px 8px #e0e7ff;
    }
    .tag-pill i {
        margin-right: 5px;
        font-size: 1em;
    }
    .action-btn {
        background: #f1f5f9;
        color: #6366f1;
        border: none;
        border-radius: 8px;
        padding: 7px 18px;
        margin-right: 10px;
        font-size: 1.1em;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.2s, color 0.2s;
    }
    .action-btn:hover {
        background: #6366f1;
        color: #fff;
    }
    .add-form {
        background: #fff;
        border-radius: 14px;
        box-shadow: none;
        padding: 10px 16px 6px 16px;
        margin-bottom: 1.2rem;
        border-left: none;
    }
    </style>
''', unsafe_allow_html=True)

st.markdown('<div class="colorful-header">📑 Bookmark Manager</div>', unsafe_allow_html=True)

if choice == "Add Bookmark":
    st.markdown('<div class="add-form">', unsafe_allow_html=True)
    st.subheader("Add a New Bookmark")
    with st.form(key="add_bookmark_form"):
        title = st.text_input("Title")
        url = st.text_input("URL")
        description = st.text_area("Description")
        tags = st.text_input("Tags (comma-separated)")
        submit = st.form_submit_button("Add Bookmark")
        if submit and title and url:
            url = str(url or "").strip()
            if url and not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            conn = get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO bookmarks (title, url, description, tags) VALUES (?, ?, ?, ?)",
                      (title, url, description, tags))
            conn.commit()
            conn.close()
            st.success("Bookmark added!")
    st.markdown('</div>', unsafe_allow_html=True)

elif choice == "View Bookmarks":
    st.subheader("")
    # New tag search with clear button
    # Use columns to align search box and clear button on the same row
    # If clear was pressed, reset the search box value before rendering
    if st.session_state.get('clear_tag_search_flag', False):
        st.session_state['tag_query'] = ''
        st.session_state['tag_search_box'] = ''
        st.session_state['clear_tag_search_flag'] = False
    search_col, clear_col = st.columns([0.8, 0.2])
    with search_col:
        tag_query = st.text_input("🔎 Search by tag (partial or full tag)", value=st.session_state.get('tag_query', ''), key="tag_search_box")
        st.session_state['tag_query'] = tag_query
    with clear_col:
        st.markdown("<div style='height:1.7em'></div>", unsafe_allow_html=True)
        if st.button("Clear", key="clear_tag_search"):
            st.session_state['clear_tag_search_flag'] = True
            st.rerun()
    bookmarks = fetch_bookmarks(st.session_state.get('tag_query', ''))
    PAGE_SIZE = 10
    total = len(bookmarks)
    if total == 0:
        st.info("No bookmarks found.")
    else:
        num_pages = (total - 1) // PAGE_SIZE + 1
        page = st.number_input("Page", min_value=1, max_value=num_pages, value=1, step=1, format="%d") if num_pages > 1 else 1
        start = (page - 1) * PAGE_SIZE
        end = start + PAGE_SIZE
        for row in bookmarks[start:end]:
            bid, title, url, description, tags, created_at = row
            # Use columns to align link and icon buttons inline
            link_col, edit_col, delete_col, spacer_col = st.columns([0.7, 0.08, 0.08, 0.14])
            with link_col:
                st.markdown(f"<div class='bookmark-title' style='display:flex; align-items:center; margin-bottom:0;'>"
                            f"<a href='{url}' target='_blank' title='Open link in new tab' style='margin-right:0.5em;'>{title} <span style='font-size:1.1em;'>🔗</span></a>"
                            f"</div>", unsafe_allow_html=True)
            with edit_col:
                edit_clicked = st.button("", key=f"edit_btn_{bid}", help="Edit this bookmark", use_container_width=True, type="secondary", icon="✏️")
                if edit_clicked:
                    st.session_state[f"edit_{bid}_active"] = True
            with delete_col:
                delete_clicked = st.button("", key=f"delete_btn_{bid}", help="Delete this bookmark", use_container_width=True, type="secondary", icon="🗑️")
                if delete_clicked:
                    delete_bookmark(bid)
                    st.success("Bookmark deleted!")
                    st.rerun()
            # Description preview: show only first three lines
            if description:
                desc_lines = description.splitlines()
                preview = '\n'.join(desc_lines[:3])
                if len(desc_lines) > 3:
                    preview += ' ...'
                st.markdown(f"<div class='bookmark-desc'>{preview}</div>", unsafe_allow_html=True)
            if tags:
                tag_list = [t.strip() for t in tags.split(',') if t.strip()]
                if tag_list:
                    tag_html = ' '.join([f"<span class='tag-pill'><i>🏷️</i>{t}</span>" for t in tag_list])
                    st.markdown(f"<div style='margin-bottom:0.5em;'>{tag_html}</div>", unsafe_allow_html=True)
            # Edit form logic remains unchanged
            if st.session_state.get(f"edit_{bid}_active"):
                with st.form(key=f"edit_form_{bid}"):
                    new_title = st.text_input("Title", value=title, key=f"title_{bid}")
                    new_url = st.text_input("URL", value=url, key=f"url_{bid}")
                    new_description = st.text_area("Description", value=description, key=f"desc_{bid}")
                    new_tags = st.text_input("Tags (comma-separated)", value=tags, key=f"tags_{bid}")
                    save = st.form_submit_button("Save Changes")
                    cancel = st.form_submit_button("Cancel")
                    if save:
                        new_url = str(new_url or "").strip()
                        if new_url and not new_url.startswith(('http://', 'https://')):
                            new_url = 'https://' + new_url
                        update_bookmark(bid, new_title, new_url, new_description, new_tags)
                        st.success("Bookmark updated!")
                        st.session_state[f"edit_{bid}_active"] = False
                        st.rerun()
                    if cancel:
                        st.session_state[f"edit_{bid}_active"] = False
                        st.rerun()
            st.markdown("---")
        if num_pages > 1:
            st.markdown(f"<div style='text-align:center; margin-top:1.5em; color:#6366f1; font-weight:600;'>Page {page} of {num_pages}</div>", unsafe_allow_html=True)
