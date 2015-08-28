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
                    print(self._max_note_length)
                    #direction = random.choice([0, -1]) 
                    #possible_notes = self.notes[-1].calibrate_scale(self.key, direction)
                    #is_rest = random.random() < preset.rest_chance
                    # 0 is going up - scales go up by default
                    #... this is not a good algorithm
                    #possible_notes = [s + up * 12 for s in possible_notes]
                    """
                    note = weighted_choice(dict(zip(possible_notes, NOTE_DISTRO_LIST)))
                    next_length = random_note_length(max_length) 
                    note_to_append = Midi_Note(channel, next_length, 127 * is_rest, note)
                    self.notes.append(note_to_append)
                    self.length += note_to_append.length
                    max_length = length - self.length
                    if note_length < BEAT and self.length < length: #repeat
                        if (random.random() > .8):
                            continue
                        repeat_beats = random.choice([1/4, 1/2, 1, 2, 3, 4])
                        total = note_length
                        while total < BEAT *repeat_beats and self.length < length:
                            possible_notes = rotate_scale_to_note(key, self.notes[-1])
                            up = random.choice([1, -1])
                            possible_notes = [s +   up * 12 for s in possible_notes]


                            note = weighted_choice(dict(zip(possible_notes, REPEAT_DISTRO_LIST)))
                            is_rest = random.random() < REST_CHANCE
                            note_to_append = Midi_Note(channel, next_length, 127 * is_rest, note)
                            self.notes.append(note_to_append)
                            self.length += note_to_append.length
                            total += note_length
                """
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

    def _random_note(self, dist):
        note_length = self._random_note_length(dist.length_dist)
        note_number = random.choice(self.key).number
        velocity = dist.velocity if random.random() > dist.rest_chance else 0 
        return midi_note.Midi_Note(self.channel, note_length, velocity, note_number)

    def _random_note_length(self, dist):#length_dist
        """Chooses a random note length given a maximum length and distribution"""
        res = {}
        for choice, weight in dist.items():
            if choice <= self._max_note_length:
                res[choice] = weight
        return utility.choose_random_weighted_choice(res)
    
    def write_to_track(self, track):
        for note in self.notes:
            note.start(track)
            note.end(track)
