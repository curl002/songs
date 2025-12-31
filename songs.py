import tkinter as tk
from tkinter import ttk
import webbrowser
import json
import subprocess
import os

songs_by_genre = {
    "Unlisted": []
}

SAVE_FILE = "songs.json"

def save_songs():
    with open(SAVE_FILE, "w") as f:
        json.dump(songs_by_genre, f)

def delete_song():
    selected_item = song_tree.selection()
    if selected_item:
        song_data = song_tree.item(selected_item)['values']
        current_genre = genre_combo.get()

        if current_genre in songs_by_genre:
            # Remove the selected song from the genre
            try:
                songs_by_genre[current_genre].remove(tuple(song_data))
                # Refresh the song list
                display_songs(current_genre)
                save_songs()
            except ValueError:
                print("Error: Song not found in the genre list.")
    else:
        print("No song selected for deletion.")

def load_songs():
    global songs_by_genre
    try:
        with open(SAVE_FILE, "r") as f:
            loaded_songs = json.load(f)
            # Validate and normalize data
            for genre, songs in loaded_songs.items():
                normalized_songs = []
                for entry in songs:
                    if len(entry) == 3:
                        normalized_songs.append(tuple(entry))
                    elif len(entry) == 2:
                        # Add a placeholder artist if missing
                        normalized_songs.append((entry[0], "Unknown Artist", entry[1]))
                songs_by_genre[genre] = normalized_songs
    except FileNotFoundError:
        pass

def open_link(url):
    """Open the given URL in an incognito tab in Google Chrome."""
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe'

    if os.path.exists(chrome_path):
        try:
            # Use subprocess to open Chrome with the incognito flag
            subprocess.Popen([chrome_path, '--incognito', url])
        except Exception as e:
            print(f"Failed to open Chrome in incognito mode: {e}")
    else:
        print("Chrome executable not found. Opening in the default web browser.")
        webbrowser.open(url)

def display_songs(genre):
    for item in song_tree.get_children():
        song_tree.delete(item)

    # Add songs for the selected genre
    for entry in songs_by_genre.get(genre, []):
        if len(entry) == 3:
            song_tree.insert("", "end", values=entry)
        else:
            print(f"Invalid entry in genre '{genre}': {entry}")


def add_song():
    genre = genre_combo.get()
    if genre in songs_by_genre:
        song_name = song_name_entry.get()
        artist = artist_entry.get()
        song_url = song_url_entry.get()
        if song_name and artist and song_url:
            songs_by_genre[genre].append((song_name, artist, song_url))
            display_songs(genre)
            move_to_genre_combo['values'] = list(songs_by_genre.keys())  # Update move_to_genre dropdown
            save_songs()

def add_genre():
    new_genre = new_genre_entry.get().strip()
    if new_genre and new_genre not in songs_by_genre:
        songs_by_genre[new_genre] = []
        # Update the dropdowns
        genre_combo['values'] = list(songs_by_genre.keys())
        move_to_genre_combo['values'] = list(songs_by_genre.keys())
        save_songs()
        print(f"Genre '{new_genre}' added.")
    elif not new_genre:
        print("Genre name cannot be empty.")
    else:
        print(f"Genre '{new_genre}' already exists.")

def delete_genre():
    genre = genre_combo.get()
    if genre in songs_by_genre and genre != "Unlisted":
        songs_by_genre["Unlisted"].extend(songs_by_genre.pop(genre))
        genre_combo['values'] = list(songs_by_genre.keys())
        move_to_genre_combo['values'] = list(songs_by_genre.keys())  # Update move_to_genre dropdown
        genre_combo.set("Unlisted")
        display_songs("Unlisted")
        save_songs()

def move_song():
    selected_item = song_tree.selection()
    if selected_item:
        song_data = song_tree.item(selected_item)['values']
        current_genre = genre_combo.get()
        target_genre = move_to_genre_combo.get()

        if current_genre in songs_by_genre and target_genre in songs_by_genre:
            songs_by_genre[current_genre].remove(tuple(song_data))
            songs_by_genre[target_genre].append(tuple(song_data))
            display_songs(current_genre)
            save_songs()

# Load songs from file
load_songs()

# Create the main application window
app = tk.Tk()
app.title("Song Browser")

# Start the window maximized
app.state('zoomed')

app.title("Song Browser")
app.geometry("1920x1080")

# Genre selection dropdown
genre_label = ttk.Label(app, text="Select Genre:")
genre_label.pack(pady=10)

genre_combo = ttk.Combobox(app, values=list(songs_by_genre.keys()))
genre_combo.pack()
genre_combo.bind("<<ComboboxSelected>>", lambda e: display_songs(genre_combo.get()))

# Song list treeview
song_tree = ttk.Treeview(app, columns=("Song", "Artist", "URL"), show="headings")
song_tree.heading("Song", text="Song")
song_tree.heading("Artist", text="Artist")
song_tree.heading("URL", text="URL")
song_tree.column("Song", width=200)
song_tree.column("Artist", width=200)
song_tree.column("URL", width=350)

song_tree.pack(pady=20, fill=tk.BOTH, expand=True)

# Open link on double-click
song_tree.bind("<Double-1>", lambda e: open_link(song_tree.item(song_tree.selection())['values'][2]))

# Input fields to add a song
song_name_label = ttk.Label(app, text="Song Name:")
song_name_label.pack(pady=5)

song_name_entry = ttk.Entry(app)
song_name_entry.pack(pady=5)

artist_label = ttk.Label(app, text="Artist:")
artist_label.pack(pady=5)

artist_entry = ttk.Entry(app)
artist_entry.pack(pady=5)

song_url_label = ttk.Label(app, text="Song URL:")
song_url_label.pack(pady=5)

song_url_entry = ttk.Entry(app)
song_url_entry.pack(pady=5)

# Dropdown to select target genre for moving songs
move_to_genre_label = ttk.Label(app, text="Move Song To:")
move_to_genre_label.pack(pady=5)

move_to_genre_combo = ttk.Combobox(app, values=list(songs_by_genre.keys()))
move_to_genre_combo.pack()

move_song_button = ttk.Button(app, text="Move Song", command=move_song)
move_song_button.pack(pady=10)

delete_song_button = ttk.Button(app, text="Delete Song", command=delete_song)
delete_song_button.pack(pady=10)

add_song_button = ttk.Button(app, text="Add Song", command=add_song)
add_song_button.pack(pady=10)

# Input field to add a new genre
new_genre_label = ttk.Label(app, text="New Genre Name:")
new_genre_label.pack(pady=5)

new_genre_entry = ttk.Entry(app)
new_genre_entry.pack(pady=5)

add_genre_button = ttk.Button(app, text="Add Genre", command=add_genre)
add_genre_button.pack(pady=10)

# Button to delete a genre
delete_genre_button = ttk.Button(app, text="Delete Genre", command=delete_genre)
delete_genre_button.pack(pady=10)

# Run the application
app.mainloop()
