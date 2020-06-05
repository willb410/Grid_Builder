from itertools import cycle

DYNAMICS = {'pp': 1, 
            'p': 3, 
            'mp': 6, 
            'mf': 9, 
            'f': 12, 
            'ff': 15}

STICKING = {'B': 2,
            'R': 1, 
            'L': 0}

MODIFIERS = {'articulation': {'accent': 1,
                                'marcato': 2,
                                'tenuto': 3,
                                'staccato': 4},
            'tremolo': {'diddle': 5,
                        'buzz': 6},
            'grace_note': {'flam': 7,
                            'drag': 8,
                            'three_stroke': 9},
            'duration': {'dot': 10}}

def define_dynamic(height):

    DYNAMICS = {'pp': 1, 'p': 3, 'mp': 6, 'mf': 9, 'f': 12, 'ff': 15}

    if height in DYNAMICS:
        return DYNAMICS[height]
    elif type(height) == int:
        return height
    else:
        raise Exception(f"Invalid value {height} passed to height")
