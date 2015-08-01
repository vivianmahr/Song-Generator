# Just notes for now

BEAT = 480
# bell curvy, slow (emphasis on quarter notes)
"""
LENGTH_DIST = {
    BEAT / 4  : 1,    #
    BEAT / 2  : 8,    # 
    BEAT / 1  : 16,    # Quarter in /4 time sig
    BEAT * 2  : 5,    #
    BEAT * 3  : 3,    #
    BEAT * 4  : 2     # 
}
"""
#Fast song
LENGTH_DIST = {
    BEAT / 4  : 18,    # sixteenth
    BEAT / 2  : 16,    # eigth
    BEAT / 1  : 10,    # Quarter note in X/4 time sig
    BEAT * 2  : 1,     # Half
    BEAT * 3  : 1,     # "
    BEAT * 4  : 0      # 
}

NOTE_DISTRO_LIST = [4, 7, 8, 3, 8, 1, 2, 3]
REPEAT_DISTRO_LIST = [8, 9, 5, 4, 3, 0, 0, 1]

bpm = 170
channel = 1
measures = 30
repeat_chance = .5
scale = "major"
#key = Note("C", 3).apply_relation("scale", scale=scale)

