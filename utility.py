from mido import MidiFile

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



if __name__ == "__main__":
	print_song("test.mid")