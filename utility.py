from mido import MidiFile
import random

def print_song(song_name):
    """ Prints all the messages in a song. """
    with MidiFile(song_name) as mid:
        for i, track in enumerate(mid.tracks):
            print('Track {}: {}'.format(i, track.name))
            for message in track:
                print(" " + str(message))

def stringify_list_of_notes(l, sharp=True):
    """ Returns a readable list of notes """
    result = ""
    for note in l:
        result += note.get_note(sharp) + "|"
    return result


def choose_random_weighted_choice(choices):
    """ Takes a dictionary of { choice: weight } and 
        returns a random using the weighted values """
    total = sum([weight for weight in choices.values()])
    rand = random.uniform(0, total)
    upto = 0
    for choice, weight in choices.items():
        if upto + weight > rand:
            return choice
        upto += weight



if __name__ == "__main__":
    print_song("test.mid")
    choices = {
        "10": 10,
        "5" : 5,
        "1" : 1
    }
    results = {
        "10": 0,
        "5" : 0,
        "1" : 0
    }

    for i in range(160): # results should be around a ratio of 1:5:10
        results[choose_random_weighted_choice(choices)] += 1
    print(results)





