from utility import stringify_list_of_notes 

class Note():
    """ Base note class that contains musical logic and relations """
    # both scales are used to convert string <-> midi - octaves increase 
    # on C but the midi notes start on A
    scale_A = ("A", "A#/Bb", "B", "C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab")
    scale_C = ("C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B")
    scale_start = 21
    scale_end = 108

    def __init__(self, *args):
        # either args = [note_number] or args = [note, octave]
        if len(args) == 1:
            self._create_from_note_number(args[0])
        elif len(args) == 2:
            self._create_from_string(args[0], args[1])
        else: 
            raise ValueError("Incorrect inputs: {}".format(args))

    def get_octave(self):
        """ Returns the octave number of the note """
        return int(self.number / 12) - 1

    def get_note(self, sharp=True):
        """ Returns the letter part of the note """
        note = Note.scale_A[(self.number - 21) % 12]
        if "/" in note:
            if sharp:
                note = note[:2]
            else:
                note = note[3:]
        return note

    def to_string(self, sharp=True):
        """ Returns a string representation of the note """
        note = self.get_note(sharp)
        octave = self.get_octave()
        return "{:2} {}".format(note, octave)

    def _create_from_string(self, note, octave):
        """ Creates a note given a string representation of a note and an octave"""
        note_number = 0
        if "#" in note or "b" in note:
            for (i, note_string) in enumerate(Note.scale_C):
                if note in note_string:
                    note_number = i
                    continue
        else:
            note_number = Note.scale_C.index(note)
        self.number = note_number + (octave * 12) + 12

    def _create_from_note_number(self, note_number):
        """ Creates a note from a note number """ 
        assert(note_number <= Note.scale_end and note_number >= Note.scale_start)
        self.number = note_number

    def apply_relation(self, relation, direction=1, sharp=True, **kargs):
        """ General note relations """
        steps = tuple()
        if relation == "2nd":
            steps = (2,)
        elif relation == "3rd":
            if kargs['scale'] == "major":
                steps = (4,)
            elif kargs['scale'] == "minor":
                steps = (3)
        elif relation == "5th":
            steps = (5,)
        elif relation == "chord":
            if kargs['scale'] == "major":
                steps = (4, 3)
            elif kargs['scale'] == "minor":
                steps = (3, 4)
        elif relation == "4th":
            steps = (5,)
        elif relation == "scale":
            return self.generate_scale(kargs["scale"], sharp=sharp)
        elif relation == "7th":
            if kargs['scale'] == "major":
                steps = (11,)
            elif kargs['scale'] == "minor":
                steps = (10,)
        elif relation == "octave":
            steps = (12,)
        elif relation == "repeat":
            steps = (12,)
        else: 
            raise ValueError("Incorrect arguments {} for {}".format(kargs, relation))
        steps = [s * direction for s in steps]
        return self._generate_notes_from_note(steps)

    def _generate_rotated_notes(self, sharp=False):
        """ Generates a list of notes with the current note at the beginning """
        note = self.get_note(sharp)
        rotated_notes = list(Note.scale_A)
        if "#" in note:
            for i in range(len(rotated_notes)):
                if "#" in rotated_notes[i]:
                    rotated_notes[i] = rotated_notes[i][:2] 
        elif "b" in note:
            for i in range(len(rotated_notes)):
                if "b" in rotated_notes[i]:
                    rotated_notes[i] = rotated_notes[i][3:] 
        while rotated_notes[0] != note:
            rotated_notes.insert(0, rotated_notes.pop());
        return rotated_notes

    def generate_scale(self, scale="major", sharp=True):
        """Generates a scale starting on this note."""
        note = self.get_note(sharp)
        rotated_notes = self._generate_rotated_notes(sharp)
        steps = []

        if scale == "major":
            steps = (2, 2, 1, 2, 2, 2, 1)
        elif scale == "natural minor":
            steps = (2, 1, 2, 2, 1, 2, 2)
        elif scale == "harmonic minor":
            steps = (2, 1, 2, 2, 1, 3, 1)
        elif scale == "melodic minor":
            steps = (2, 1, 2, 2, 2, 2, 1)
        else:
            raise ValueError("{} is not a valid scale".format(scale))

        return self._generate_notes_from_note(steps)

    def _generate_notes_from_note(self, steps):
        """ Helps generate note relations based on the number of steps between notes """
        result = [self]
        difference = 0
        for step in steps:
            difference += step
            result.append(Note(self.number + difference))
        return result

if __name__ == "__main__":
    for i in range(21, 109):
        n = Note(i)
        n2 = Note(n.get_note(), n.get_octave())
        assert(n.to_string() == n2.to_string())

    c = Note("C", 3)
    scale = c.generate_scale("major", True)
    assert(stringify_list_of_notes(scale) == "C|D|E|F|G|A|B|C|")

    a = Note("A", 3)
    scale = a.generate_scale("natural minor", True)
    assert(stringify_list_of_notes(scale) == "A|B|C|D|E|F|G|A|")

    assert(stringify_list_of_notes(c.apply_relation("2nd")) == "C|D|")
    assert(stringify_list_of_notes(c.apply_relation("2nd")) == "C|D|")

    assert(stringify_list_of_notes(c.apply_relation("chord", scale="major")) == "C|E|G|")
    assert(stringify_list_of_notes(a.apply_relation("chord", scale="minor")) == "A|C|E|")
