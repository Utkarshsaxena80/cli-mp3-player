
import os
import sys
import time
import random

# Hide pygame support prompt
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame
import keyboard
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from rich.console import Console
from rich.panel import Panel

console = Console()


# -----------------------------
# Utility Functions
# -----------------------------

def format_time(seconds):
    seconds = max(0, int(seconds))
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins}:{secs:02d}"



def get_song_info(file_path):
    """Read MP3 metadata safely."""

    title = os.path.basename(file_path).replace(".mp3", "")
    artist = "Unknown Artist"
    length = 0

    try:
        audio = MP3(file_path)
        length = audio.info.length

        try:
            tags = EasyID3(file_path)

            if "title" in tags:
                title = tags["title"][0]

            if "artist" in tags:
                artist = tags["artist"][0]

        except Exception:
            pass

    except Exception:
        pass

    return title, artist, length



def draw_ui(title, artist, volume):
    ui_content = (
        f"[bold cyan]Track:[/bold cyan]  {title}\n"
        f"[bold magenta]Artist:[/bold magenta] {artist}\n"
        f"[bold yellow]Volume:[/bold yellow] {int(volume * 100)}%\n\n"
        f"[dim]Controls:\n"
        f" [SPACE] Play/Pause | [UP/DOWN] Volume\n"
        f" [LEFT/RIGHT] Seek  | [N/P] Next/Prev\n"
        f" [S] Shuffle        | [ESC] Quit[/dim]"
    )

    console.print(
        Panel(
            ui_content,
            title="[bold green]Now Playing[/bold green]",
            border_style="green",
            expand=False,
        )
    )


# -----------------------------
# Main Player Logic
# -----------------------------

def play_mp3(folder_path):
    if not os.path.exists(folder_path):
        console.print(f"[bold red]Folder does not exist:[/bold red] {folder_path}")
        sys.exit(1)

    songs = sorted(
        [
            f
            for f in os.listdir(folder_path)
            if f.lower().endswith(".mp3")
        ]
    )

    if not songs:
        console.print("[bold red]No MP3 files found![/bold red]")
        sys.exit(1)

    try:
        pygame.mixer.init()
    except Exception as e:
        console.print(f"[bold red]Failed to initialize audio:[/bold red] {e}")
        sys.exit(1)

    current_volume = 0.5
    pygame.mixer.music.set_volume(current_volume)

    console.print(f"[bold green]Loaded {len(songs)} songs.[/bold green]\n")

    current_index = 0

    while current_index < len(songs):
        song_file = songs[current_index]
        full_path = os.path.join(folder_path, song_file)

        try:
            title, artist, song_length = get_song_info(full_path)

            pygame.mixer.music.load(full_path)
            pygame.mixer.music.play()

            is_paused = False
            current_time = 0.0
            paused_time = 0.0
            seek_offset = 0.0

            draw_ui(title, artist, current_volume)

            while True:
                # Song finished naturally
                if not pygame.mixer.music.get_busy() and not is_paused:
                    break

                # Update playback time
                if not is_paused:
                    mixer_pos = pygame.mixer.music.get_pos()

                    if mixer_pos >= 0:
                        current_time = seek_offset + (mixer_pos / 1000.0)

                current_time = min(current_time, song_length)

                # Draw progress bar
                if song_length > 0:
                    progress = int((current_time / song_length) * 30)
                else:
                    progress = 0

                progress = max(0, min(progress, 30))

                bar = "█" * progress + "░" * (30 - progress)

                print(
                    f"\r[{bar}] {format_time(current_time)} / {format_time(song_length)}",
                    end="",
                    flush=True,
                )

                # -----------------------------
                # Keyboard Controls
                # -----------------------------

                # Pause / Resume
                if keyboard.is_pressed("space"):
                    if is_paused:
                        pygame.mixer.music.unpause()
                        is_paused = False
                    else:
                        pygame.mixer.music.pause()
                        paused_time = current_time
                        is_paused = True

                    time.sleep(0.25)

                # Seek Forward
                elif keyboard.is_pressed("right"):
                    current_time += 10
                    current_time = min(current_time, song_length)

                    seek_offset = current_time

                    pygame.mixer.music.play(start=current_time)

                    if is_paused:
                        pygame.mixer.music.pause()

                    time.sleep(0.25)

                # Seek Backward
                elif keyboard.is_pressed("left"):
                    current_time -= 10
                    current_time = max(0, current_time)

                    seek_offset = current_time

                    pygame.mixer.music.play(start=current_time)

                    if is_paused:
                        pygame.mixer.music.pause()

                    time.sleep(0.25)

                # Volume Up
                elif keyboard.is_pressed("up"):
                    current_volume = min(1.0, current_volume + 0.05)
                    pygame.mixer.music.set_volume(current_volume)

                    console.print(
                        f"\n[green]Volume:[/green] {int(current_volume * 100)}%"
                    )

                    time.sleep(0.1)

                # Volume Down
                elif keyboard.is_pressed("down"):
                    current_volume = max(0.0, current_volume - 0.05)
                    pygame.mixer.music.set_volume(current_volume)

                    console.print(
                        f"\n[green]Volume:[/green] {int(current_volume * 100)}%"
                    )

                    time.sleep(0.1)

                # Next Song
                elif keyboard.is_pressed("n"):
                    pygame.mixer.music.stop()
                    time.sleep(0.25)
                    break

                # Previous Song
                elif keyboard.is_pressed("p"):
                    current_index = max(-1, current_index - 2)
                    pygame.mixer.music.stop()
                    time.sleep(0.25)
                    break

                # Shuffle Remaining Songs
                elif keyboard.is_pressed("s"):
                    remaining = songs[current_index + 1 :]
                    random.shuffle(remaining)
                    songs[current_index + 1 :] = remaining

                    console.print("\n[yellow]Playlist shuffled![/yellow]")
                    time.sleep(0.25)

                # Exit
                elif keyboard.is_pressed("esc"):
                    console.print("\n\n[bold red]Exiting player...[/bold red]")

                    pygame.mixer.music.stop()
                    pygame.mixer.quit()
                    sys.exit(0)

                time.sleep(0.05)

            print()
            current_index += 1

        except pygame.error as e:
            console.print(
                f"\n[bold red]Pygame error with {song_file}: {e}[/bold red]"
            )
            current_index += 1

        except Exception as e:
            console.print(
                f"\n[bold red]Unexpected error with {song_file}: {e}[/bold red]"
            )
            current_index += 1

    pygame.mixer.quit()
if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print(
            "[bold yellow]Usage:[/bold yellow] python cli_player.py <mp3_folder>"
        )
        sys.exit(1)

    folder = sys.argv[1]
    play_mp3(folder)
