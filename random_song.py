import mido
import random
#import Midi_Note from midi_note
from midi_note import Midi_Note
from note import Note
# See what's less confusing in the end - generating a bunch of notes 
# and then their messages, or generating and working note by note
# Things to consider
#   Repetition
#   Key
#   Pacing in relation to closeby notes 

# 1 beat = length=480
BEAT = 480
"""

class Note():
    def __init__(self, note, length, velocity, channel):
        self.channel = channel
        self.note = note
        self.length = length
        self.velocity = velocity
    def start(self, track, time=0):
        track.append(mido.Message('note_on', note=self.note, channel=self.channel, velocity=self.velocity, time=time))
    def end(self, track):
        track.append(mido.Message('note_off', note=self.note, channel=self.channel, velocity=0, time=self.length))

class Chord():
    def __init__(self, note):
        pass
"""
# Wrap in function according to inputs later

with mido.MidiFile() as mid:
    bpm = 60
    # Try and find a decent tempo range that holds most songs
    # any songs that should be outside can be altered in another program
    #mid.ticks_per_beat = random.randint(150, 200)
    #mid.ticks_per_beat = 120
    key = Note("A", 3).generate_scale("natural minor", True)
    key = Note("C", 3).apply_relation("4th", True)
    key = Note("C", 3).apply_relation("scale", scale="major")

    key = [n.number for n in key]

    # For now, only one track
    track = mido.MidiTrack()
    mid.tracks.append(track)
    
    # 1-96 should be a good number of instrument types
    track.append(mido.Message('control_change', channel=10, control=random.randint(0, 95), value=0, time=1))
    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm)))
    # 50 random notes for now - later, change to measures if possible 
    for i in range(0, 20):
        # Note range for midi is 21-108
        # I haven't actually a clue how tempo and length relates to measures yet
        # default channel = 2
        # no overlapping notes yet
        # def __init__(self, channel, length, velocity, *args):

        # 480  = quarter note
        note = Midi_Note(2, BEAT, 127, random.choice(key)) # find way to write this nicely later
        #print(note.to_string(), note.length) #note = Midi_Note(random.randint(21, 108), random.randint(1, 6) * 48, velocity=127, channel=2) # find way to write this nicely later
        note.start(track)
        note.end(track)
    track.append(mido.MetaMessage('end_of_track', time=0))
    # Custom song name later
    mid.save('exported_song.mid')
    print(mid.length)

    """
        Notes
            2nd - rare
            chord = should be common if melody? 
            Fourth - read up on what it's supposed to be again but it shouldn't happen too often
            next-note-in-scale = often?
            repeat note = I have a feeling this will have to do mroe with tempo, but give it a scale depending on pacing of the song
            Octave - I don't think often?
                actually, this might be a "calculate, and see if it jumps/falls an octave"
            Play additional note in chord = only if it's on an emphasis beat, then maybe a percentage
            Look up more on how the key of a song affects things and changing it
        For now, since I can handle harmonies okay, focus on melody generating - HOWEVER, for future considerations, consider unsynced chords
            (mainly where the notes are like)
            -------
            ---- 
            or 
            -------
               ----
    """