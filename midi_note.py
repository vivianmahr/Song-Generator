import note
import mido

class Midi_Note(note.Note):
    def __init__(self, channel, length, velocity, *args):
        note.Note.__init__(self, *args)
        self.channel = channel
        self.length = length
        self.velocity = velocity
    def start(self, track, time=0):
        track.append(mido.Message('note_on', note=self.number, channel=self.channel, velocity=self.velocity, time=time))
    def end(self, track, use_length=""):
        # use length shouldn't be used in simultaneous chords
        if use_length == "":
            track.append(mido.Message('note_off', note=self.number, channel=self.channel, velocity=0, time=self.length))
        else: 
            track.append(mido.Message('note_off', note=self.number, channel=self.channel, velocity=0, time=use_length))    