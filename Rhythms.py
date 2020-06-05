import functools
from copy import deepcopy

try:
    from .Classes import *
    from .Notes import *
    from .Modifiers import *
except:
    from Classes import *
    from Notes import *
    from Modifiers import *


class Rhythm:

    def __init__(self, default_duration: float, notes: list=None):
        
        self._default_duration = default_duration # Default duration value for Notes

        self.notes = [] if notes is None else notes # Container for Note objects

        self.modulators = {}
        
        # Space taken up by rhythm, eigth note would be .125
        self._duration: float = self.duration

    def __repr__(self):
        return f"Rhythm(duration={round(self.duration, 4)}, notes={self.notes})"
        
    @property
    def duration(self):
        ''' Sum of duration from Note objects in the rhythm '''
        self._duration = 0
        for note in self.notes:
            self._duration += note.duration
        return self._duration

    def set_duration(self, *new_durations):
        ''' Adjust the duration of all notes in the Rhythm '''
        dur_list = [*new_durations]

        if len(dur_list) > len(self.notes):
            raise Exception(f"{len(dur_list)} duration values passed, only {len(self.notes)} Notes in Rhythm object")
        
        while len(dur_list) < len(self.notes):
            dur_list.append(dur_list[-1])
        
        for note, new in zip(self.notes, dur_list):
            if not new: continue
            note.duration = new

    #########################################
    #               Add Notes               #
    #########################################

    def add(self, *notes):
        ''' Add new Notes to the end of the Rhythm'''
        self.notes.extend([*notes])

    def add_note(self, sticking=None, dur_mod=None, *mods, **kwargs):
        ''' Add a single Note by passing Note parameters '''

        if type(dur_mod) == float: # Duration
            _duration = dur_mod
            _modifiers = [*mods]
        elif dur_mod == None: # No value passed
            _duration = self._default_duration
            _modifiers = []
        else: # Modifier passed
            _duration = self._default_duration
            _modifiers = dur_mod if type(dur_mod) == list else [dur_mod]


        if not sticking: raise Exception('Provide a sticking value')
        note = Note(_duration, sticking, *_modifiers, **kwargs)
        
        self.add(note)

    #########################################
    #               Copy Notes              #
    #########################################

    def copy_note(self, flip=False):
        ''' Copy the most recent note '''
        recent = deepcopy(self.notes[-1])
        if flip: recent.flip_sticking()
        self.add(recent)

    #########################################
    #              Remove Notes             #
    #########################################

    def remove_note(self, position=-1):
        ''' Remove Note from rhythm'''
        return self.notes.pop(position)

    #########################################
    #           Modulate Modifiers          #
    #########################################    

    def add_modulator(self, modifier, name, position=None):
        ''' Add modulator to the Rhythm '''
        # Mark modifier to allow it to be applied more than once
        modifier.modulator = True 
        if position != None:
            self.notes[position].add_modifier(modifier)
        self.modulators[name] = modifier


    #########################################
    #                Sticking               #
    #########################################

    @property
    def sticking(self):
        ''' Get the sticking of notes in the rhythm as a string '''
        return''.join([note.sticking for note in self.notes])

    def set_sticking(self, new_sticking):
        ''' Change the sticking of each note in the Rhythm from left to right
            If the string is shorter than the number of notes, predefined sticking will be maintained 
            Keep current value by passing "_" instead of a sticking value'''
        
        for note, new in zip(self.notes, new_sticking):
            if new == '_': continue
            note.sticking = new

    def flip_sticking(self):
        ''' Flip the hand for all notes in the Rhythm '''
        pass


def rhythm_duration(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
       
        rhythm = func(*args, **kwargs)

        if args:
            duration, *_ = args
        else:
            duration, *_ = func.__defaults__

        if type(duration) in [float, int]:
            duration = [duration / len(rhythm.notes)]
        rhythm.set_duration(*duration)

        return rhythm

    return wrapper


###############################################################################
#                                                                             #
#                                                                             #
#                                  Rudiments                                  #
#                                                                             #
#                                                                             #
###############################################################################

''' Functions for common rudiments
    
    Use rhythm_duration decorator and define duration as the first parameter 
    
    Template:

    @rhythm_duration
    def make_rudiment(duration: float=<default value>):

        rudiment = Rhythm(default_duration: float=<default Note duration)
        rudiment.add_note(sticking: str=<one of ['R', 'L', 'B']>, Modifier(), Modifier(), ...)
        rudiment.add_note(...)
        ...
        rudiment.add_note(...)

        return rudiment 
'''

@rhythm_duration
def make_paradiddle(duration=1/4, downbeat_accent=True):
    
    paradiddle = Rhythm(1/16)
    if downbeat_accent:
        paradiddle.add_note('R', Accent())
    else:
        paradiddle.add_note('R')
    paradiddle.add_note('L')
    paradiddle.add_note('R')
    paradiddle.add_note('R')
    
    return paradiddle

@rhythm_duration
def make_paradiddlediddle(duration=1/4):
    ''' Extend paradiddle rudiment '''

    paradiddle = make_paradiddle(4/24)
    
    # _let = Note(1/24, 'L')
    # _letand = Note(1/24, 'L')
    
    paradiddle.add_note('L')
    paradiddle.add_note('L')
    
    # return paradiddle.add(_let, _letand)
    return paradiddle
    

@rhythm_duration
def make_flam_accent(duration=1/4):

    # _tri = Note(1/12, 'R', Flam())
    # _po = Note(1/12, 'L')
    # _let = Note(1/12, 'R')

    flam_accent = Rhythm(1/12)
    flam_accent.add_note('R', [Flam(), Accent()])
    flam_accent.add_note('L')
    flam_accent.add_note('R')
    
    # return Rhythm(_tri, _po, _let)
    return flam_accent

@rhythm_duration
def make_flamacue(duration=5/16):

    flamacue = Rhythm(1/16)
    flamacue.add_note('R', Flam())
    flamacue.add_note('L', Accent())
    flamacue.add_note('R')
    flamacue.add_note('L')
    flamacue.add_note('R', Flam())

    return flamacue

if __name__ == '__main__':

    print('\n', make_paradiddle())
    print('\n', make_paradiddlediddle())
    print('\n', make_flam_accent())
    print('\n', make_flamacue())
