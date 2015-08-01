import note
import mido

class Midi_Note(note.Note):
    """ Notes that write themselves to a mido track """
    def __init__(self, channel, length, velocity, *args):
        note.Note.__init__(self, *args)
        self.channel = channel
        self.length = int(length)
        self.velocity = velocity

    def start(self, track, time=0):
        """ Starts the note on a midi track """
        track.append(mido.Message('note_on', note=self.number, channel=self.channel, velocity=self.velocity, time=time))

    def end(self, track, use_length=""):
        """ Ends the note on a midi track """
        # use length shouldn't be used in simultaneous chords
        track.append(mido.Message('note_off', note=self.number, channel=self.channel, velocity=0, time=self.length))

    def copy(self):
        """ Copies the current note """
        return Midi_Note(self.channel, self.length, self.velocity, self.number)