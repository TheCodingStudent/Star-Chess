import os
import math
import pygame
import random
from scripts import functions


class Mixer:
    """Mixer is a class to handle all the music and sound of the game"""
    def __init__(self, path: str):

        # PROPERTIES
        self.path = os.path.dirname(path)
        self.music_path = functions.resource_path(f'{self.path}/audio/music')
        self.sound_path = functions.resource_path(f'{self.path}/audio/sounds')

        # SONGS AND SOUNDS
        self.volume = 1
        self.next_song = ''
        self.playing = False
        self.current_song = ''

        # LOAD SONGS
        self.songs = [
            functions.resource_path(f'{self.music_path}/{song}')
            for song in os.listdir(self.music_path)
        ]

        # LOAD SOUNDS
        self.sounds = {
            sound:pygame.mixer.Sound(functions.resource_path(f'{self.sound_path}/{sound}'))
            for sound in os.listdir(self.sound_path)
        }

        # EVENTS
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

    def set_music_volume(self, volume: int) -> None:
        """Sets the volumen of the music"""
        self.volume = volume/100
        pygame.mixer.music.set_volume(self.volume)
    
    def set_sound_volume(self, volume: int, play_sound: bool=True) -> None:
        """Sets the volume of the sounds"""
        for sound in self.sounds.values():
            sound.set_volume(volume/100)
        if play_sound: self.play_sound('move.wav')

    def load_queue(self) -> None:
        """Loads the next song in queue"""
        while True:
            song = random.choice(self.songs)
            if song != self.current_song: break
        pygame.mixer.music.queue(song)
        pygame.mixer.music.set_volume(self.volume)
        self.next_song = song
    
    def play(self, loops: int=0) -> None:
        """Plays the songs"""
        self.playing = True
        pygame.mixer.music.play(loops=loops)
        pygame.mixer.music.set_volume(self.volume)
    
    def start(self, song=None) -> None:
        """Inits the mixer"""
        if not song: song = random.choice(self.songs)
        pygame.mixer.music.load(song)
        pygame.mixer.music.set_volume(self.volume)
        self.current_song = song
        self.load_queue()

    def stop(self) -> None:
        """Stops the mixer"""
        pygame.mixer.music.stop()
    
    def next(self) -> None:
        """Loads the next song and updates the new"""
        self.current_song = self.next_song
        self.load_queue()

    def play_sound(self, sound: str) -> None:
        """Plays a sound"""
        pygame.mixer.Sound.play(self.sounds[sound])
    
    def pause(self) -> None:
        """Pauses the mixer"""
        self.playing = False
        pygame.mixer.music.pause()
    
    def unpause(self) -> None:
        """Unpauses the mixer"""
        self.playing = True
        pygame.mixer.music.unpause()
