import mido
import random
from midi_note import Midi_Note
from note import Note
import presets

def random_note_length(max_len, length_dist):
    res = {}
    for choice, weight in LENGTH_DIST.items():
        if choice <= max_len:
            res[choice] = weight
    return weighted_choice(res)

def rotate_scale_to_note(scale, note):
    result = list(scale)
    while Note(result[0]).get_note()[0] != note.get_note()[0]:
        result.insert(0, result.pop())
    return result


watot = [0,0]

class Melody():
    def __init__(self, channel, **kargs):
        try:
            if kargs["random"]:
                #key, length
                length = kargs["length"]
                key = kargs["key"]
                num_beats = length / BEAT
                
                # def __init__(self, channel, length, velocity, *args):
                note_length = random_note_length(length)
                note_number = random.randint(0, 7)
                self.notes = [Midi_Note(channel, note_length, 127, key[note_number])]
                self.length = note_length
                max_length = length - note_length
                while self.length < length:
                    possible_notes = rotate_scale_to_note(key, self.notes[-1])
                    is_rest = random.random() < REST_CHANCE
                    watot[0] += 1
                    watot[1] += is_rest
                    up = random.choice([1, -1])
                    possible_notes = [s + up * 12 for s in possible_notes]
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
                            watot[0] += 1
                            watot[1] += is_rest
                            note_to_append = Midi_Note(channel, next_length, 127 * is_rest, note)
                            self.notes.append(note_to_append)
                            self.length += note_to_append.length
                            total += note_length
                #print("62 ----", stringify_list_of_notes(self.notes))
            else:
                pass
        except Exception as E:
            raise E


    def copy(self):
        return self

    def write_to_track(self, track):
        for note in self.notes:
            note.start(track)
            note.end(track)

# 1 beat = length=480 

with mido.MidiFile(type=1) as mid:

    song_name = "exported_song" + ".mid"
    song_name = "test" + ".mid"
    time_signature = "4/4".split("/")
    time_signature = [int(n) for n in time_signature]
    bpm = 170
    channel = 1
    measures = 30
    repeat_chance = .5
    scale = "major"
    key = Note("C", 3).apply_relation("scale", scale=scale)
    key = [n.number for n in key]
    info_track = mido.MidiTrack()
    info_track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm)))
    mid.tracks.append(info_track)
    
    for i in range(1):
        track = mido.MidiTrack()
        track.append(mido.MetaMessage('track_name', name="track_name", time=1))
        mid.tracks.append(track)

        measure_length = time_signature[1] * BEAT
        for meas in range(measures):
            # going to be used later in more complicated melodies with rests
            progress = 0

            num_melodies = random.choice([1, 2, 4]) # maybe change depending on time signature, 
                                                    # but not working thirds yet
            melody_length = measure_length / num_melodies
            # "energy" and pacing should be around here 
            melodies = [Melody(channel, key=key, length=melody_length, random=True, scale=scale)]
            for i in range(num_melodies - 1):
                if (random.random() < repeat_chance):
                    melodies.append((melodies[-1]).copy())
                else:
                    melodies.append(Melody(channel, key=key, length=melody_length, random=True, scale=scale))
            for m in melodies:
                m.write_to_track(track)
            print("173--- measure={}".format(meas))
        track.append(mido.MetaMessage('end_of_track', time=1))
    mid.save(song_name)
    print (Midi_Note.tot, Midi_Note.rest, watot)
