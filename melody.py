import note
import presets
import utility
import random
import midi_note

class Melody():
    def __init__(self, channel, preset, previous_note="", **kargs):
        try:
            if kargs["random"]:
                self.preset = preset
                self._max_note_length = kargs["length"]
                self._max_length = kargs["length"]
                self.key = kargs["key"]
                self.channel = channel
                self.notes = [self._random_note(preset)]
                self._recalculate_max_note_length()
                while self._max_note_length > 0:
                    self.notes.append(self._random_note(preset))
                    self._recalculate_max_note_length()
            else:
                pass
        except KeyError:
            raise

    def _recalculate_max_note_length(self):
        self._length = sum([n.length for n in self.notes])
        self._max_note_length = self._max_length - self._length

    def copy(self):
        n = Melody(self.channel, self.preset, random=False)
        n.notes = list(self.notes)
        return self

    def _random_note(self, preset, previous_note=""):
        if previous_note == "":
            note_length = self._random_note_length(preset.length_dist)
            note_number = random.choice(self.key).number
            velocity = preset.velocity if random.random() > preset.rest_chance else 0 
            return midi_note.Midi_Note(self.channel, note_length, velocity, note_number)
        else:
            # if previous note was a rest, can't be a rest
            # chance for repeat beat is defined in 
            velocity = 0
            note_length = 0
            note_number = 0
            if previous_note.velocity == 0 or random.random() > preset.rest_chance:
                # Previous note was a rest or the chance for a rest was not chosen
                velocity = preset.velocity
            direction = 1 if random.random() < presets.step_up_chance else -1
            if self._max_note_length < presets.BEAT and random.random() < preset.repeat_note_length:
                note_length = previous_note.length
                note_number = self._random_note_number(preset.note_distro, direction, previous_note)
            else:
                note_length = self._random_note_length(preset.length_dist)
                note_number = self._random_note_number(preset.repeat_distro, direction, previous_note)
        return midi_note.Midi_Note(self.channel, note_length, velocity, note_number)

    def _random_note_number(self, relation_dist, direction, previous_note=""):
        if previous_note == "":
            return random.choice(self.key)
        res = {}
        for i in range(8): 
            res[i] = relation_dist[i]
        steps = utility.choose_random_weighted_choice(relation_dist)
        note_number = self.match_scale(previous_note)
        if direction == -1:
            note_number -= presets.OCTAVE_STEPS
        return note_number

    def match_scale(self, note_number):
        """ Rotates scale to start on the given note number"""
        result = list(self.key)[:7] # Exclude octave of first note
        note_name = note.Note(note_number).get_note()
        while (result[0].get_note() != note_name):
            result.insert(0, result.pop())    
        result.append(note.Note(result[0].note_number + presets.OCTAVE_STEPS))
        while result[0].note_number != note_number:
            step = (1 if result[0].note_number < note_number else -1) * presets.OCTAVE_STEPS
            for i in range(len(result)):
                result[i].note_number += step
        return result


    def _random_note_length(self, length_dist):
        """Chooses a random note length given a maximum length and distribution"""
        res = {}
        for choice, weight in length_dist.items():
            if choice <= self._max_note_length:
                res[choice] = weight
        return utility.choose_random_weighted_choice(res)
    
    def write_to_track(self, track):
        """Writes notes in the melody to a given mido track."""
        for note in self.notes:
            note.start(track)
            note.end(track)
