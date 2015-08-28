
import pygame
import base64


def play_music(music_file):
    """
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    """
    pygame.mixer.init()
    clock = pygame.time.Clock()
    pygame.mixer.music.load(music_file)

    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)
    print("done")

play_music("test.mid")
