import mido
import random
from midi_note import Midi_Note
from note import Note
import presets
from melody import Melody

# 1 beat = length=480 
#    def __init__(self, channel, preset, **kargs):

def random_song(name, settings, song_type=1):
    with mido.MidiFile(type=song_type) as mid:
        info_track = mido.MidiTrack()
        info_track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(settings.bpm)))
        mid.tracks.append(info_track)
        
        for i in range(settings.tracks):
            track = mido.MidiTrack()
            track.append(mido.MetaMessage('track_name', name="track" + str(i), time=1))
            mid.tracks.append(track)

            measure_length = settings.time_signature[1] * presets.BEAT
            for meas in range(settings.measures):
                num_melodies = random.choice([1, 2, 4]) # maybe change depending on time signature, 
                                                        # but not working thirds yet
                melody_length = measure_length / num_melodies
                melodies = [Melody(settings.channel, settings, key=settings.key, length=melody_length, random=True)]
                for i in range(num_melodies - 1):
                    if (random.random() < settings.melody_repeat_chance):
                        melodies.append((melodies[-1]).copy())
                    else:
                        melodies.append(Melody(settings.channel, settings, key=settings.key, length=melody_length, random=True))
                for m in melodies:
                    m.write_to_track(track)
            track.append(mido.MetaMessage('end_of_track', time=1))
        mid.save(name)

random_song("test", presets.FAST)