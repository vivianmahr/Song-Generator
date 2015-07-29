class Note():
    scale_A = ["A", "A#/Bb", "B", "C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab"]
    scale_C = ["C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"]
    scale_start = 21
    scale_end = 108

    def __init__(self, *args):
        # either args = [note_number] or args = [note, octave]
        if len(args) == 1:
            self._create_from_note_number(args[0])
        elif len(args) == 2:
            self._create_from_note(args[0], args[1])
        else: 
            raise ValueError("Incorrect inputs: {}".format(args))

    def _create_from_note(self, note, octave):
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
        if (note_number > Note.scale_end) or (note_number < Note.scale_start):
            raise IndexError("Invalid midi note")
        self.number = note_number

    def get_octave(self):
        # 11 = 21 (starting note) - 10 (because for some reason, 
        # pianos start on A but octave numbers are incremented on C)
        return int(self.number / 12) - 1

    def get_note(self, sharp=True):
        note = Note.scale_A[(self.number - 21) % 12]
        if "/" in note:
            if sharp:
                note = note[:2]
            else:
                note = note[3:]
        return note

    def to_string(self, sharp=True):
        note = self.get_note(sharp)
        octave = self.get_octave()
        return "{:2} {}".format(note, octave)

if __name__ == "__main__":
    for i in range(21, 109):
        n = Note(i)
        n2 = Note(n.get_note(), n.get_octave())
        assert(n.to_string() == n2.to_string())