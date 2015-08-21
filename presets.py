# Just notes for now
import note
BEAT = 480
class Preset():
    def __init__(self):
        # Default is a bell curve kind of distribution - rather slow with a heavy emphasis on quarter notes
        self.time_signature = [4, 4]
        self.length_dist = {
            BEAT / 4  : 1,     # Sixteenth
            BEAT / 2  : 8,     # Eighth
            BEAT / 1  : 16,    # Quarter in /4 time sig
            BEAT * 2  : 5,     # Half Note
            BEAT * 3  : 3,     # Dotted Half Note
            BEAT * 4  : 2      # Whole Note
        }
        # Chance of note relation in scale
        #                   r  2  3  4  5  6  7  octave
        self.note_distro = [4, 7, 8, 3, 8, 1, 2, 3]
        # Chance of note relation for repeat beat notes
        #                     r  2  3  4  5  6  7  octave
        self.repeat_distro = [8, 9, 5, 4, 3, 0, 0, 1]
        self.bpm = 120
        self.channel = 1
        self.measures = 1
        self.melody_repeat_chance = .5
        self.scale = "major"
        self.rest_chance = .3
        self.key = note.Note("C#", 3).apply_relation("scale", scale=self.scale)
        self.tracks = 1
        self.velocity = 127
    def set_tracks(self, tracks):
        self.tracks = tracks
    def set_time_signature(self, time_sig):
        self.time_signature = time_sig
    def set_length_distribution(self, length_dist):
        self.length_dist = length_dist
    def set_note_distribution(self, new_distro):
        self.note_distro = new_distro  
    def set_repeat_distribution(self, new_distro):
        self.repeat_distro = new_distro
    def set_bpm(self, new_bpm):
        self.bpm = new_bpm
    def set_channel(self, new_channel):
        self.channel = new_channel
    def set_measures(self, new_measures):
        self.measures = new_measures
    def set_melody_repeat_chance(self, new_chance):
        self.melody_repeat_chance = new_chance
    def set_scale(self, letter_note, scale):
        self.scale = scale
        self.key = note.Note(letter_note, 3).apply_relation("scale", scale=self.scale)
        
DEFAULT = Preset()

FAST = Preset()
FAST.set_bpm(170)
FAST.set_length_distribution({
    BEAT / 4  : 18,    
    BEAT / 2  : 16,    
    BEAT / 1  : 10,    
    BEAT * 2  : 1,     
    BEAT * 3  : 1,     
    BEAT * 4  : 0      
})
FAST.set_note_distribution([6, 6, 5, 1, 6, 3, 1, 4])
FAST.set_repeat_distribution([12, 6, 9, 2, 8, 0, 0, 1])