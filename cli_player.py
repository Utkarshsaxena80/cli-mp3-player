import sys
import time
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT']="hide"

import pygame

def play_mp3(file_path):
    if not os.path.exists(file_path):
        print(f"no folder exists")
        sys.exit(1)

    pygame.mixer.init()
    songs=os.listdir(file_path)
    print(f"Found songs {songs}")   
    for song in songs:
        if not song.endswith('.mp3'):
            continue
        full_song_path=os.path.join(file_path,song)
        try:
            pygame.mixer.music.load(full_song_path)
            pygame.mixer.music.play()
            
            print(f"\n Now playing: {song}") 
            print("Press Ctrl+C to skip to the next song, or stop if it's the last one.")

            
            while pygame.mixer.music.get_busy():
                 time.sleep(0.1)
            pygame.mixer.music.stop()
            time.sleep(1)     
                
        except pygame.error as e:
           print(f"an error occured {e}")
            
        except KeyboardInterrupt:   
           print("playback stopped by user, next song playing ...")  
           pygame.mixer.music.stop()    
           time.sleep(1)

if __name__=="__main__":
    if len(sys.argv)<2:
        print("usage pyhton cli_palyer.py <path to mp3 file>")
        sys.exit(1)        
        
    mp3_file=sys.argv[1]
    play_mp3(mp3_file)