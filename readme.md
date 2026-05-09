# CLI MP3 Player

A terminal-based MP3 player built using Python, featuring keyboard controls, live progress tracking, metadata support, playlist navigation, shuffle functionality, and a clean Rich-powered UI.
UI was vibecoded . Rest was written by me .
## Features

* Play/Pause music
* Seek forward/backward
* Volume control
* Shuffle playlist
* Previous/Next track
* Live progress bar
* MP3 metadata support
* Beautiful terminal UI using Rich

---

# Tech Stack

* Python
* Pygame
* Mutagen
* Rich
* Keyboard

---

# Installation

## Clone the repository

```bash
git clone https://github.com/Utkarshsaxena80/cli-mp3-player.git
cd mp3player
```

## Install dependencies

```bash
pip install -r requirements.txt
```

---

# Run the Project

```bash
python new.py "<path_to_mp3_folder>"
```

Example:

```bash
python cli_player.py "D:/Music"
```

---

# Controls

| Key         | Action           |
| ----------- | ---------------- |
| SPACE       | Play / Pause     |
| RIGHT ARROW | Forward 10 sec   |
| LEFT ARROW  | Backward 10 sec  |
| UP ARROW    | Increase Volume  |
| DOWN ARROW  | Decrease Volume  |
| N           | Next Song        |
| P           | Previous Song    |
| S           | Shuffle Playlist |
| ESC         | Exit Player      |

---

# Project Structure

```bash
cli-mp3-player/
│
├── cli_player.py
├── README.md
└── requirements.txt
```

---

# Known Limitations

* `keyboard` library may require admin/sudo permissions on Linux.
* Some MP3 files with corrupted metadata may not display artist/title correctly.
* Seeking accuracy depends on MP3 encoding.

---

# About This Project

This project was built as a learning and experimentation project focused on:

* audio handling
* terminal UI
* keyboard event handling
* real-time playback control

Around **40% of this project was vibe coded**, while the remaining part involved debugging, playback handling fixes, architecture decisions, and integration work.

---

# Future Improvements

* Playlist saving
* Repeat mode
* Search songs
* Album art support
* Better cross-platform hotkey handling
* Streaming support

---

# License

MIT License
