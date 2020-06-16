from copy import deepcopy
import functools

import music21 as m21

try:
    from .Classes import *
    from .Rhythms import *
    from .Modifiers import *
except:
    from Classes import *
    from Rhythms import *
    from Modifiers import *

def action(func):
    ''' Record function calls and parameters used to build up MultiRhythm object '''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
       
        call = func(*args, **kwargs)

        if kwargs.get('_save_action') != False:
            args[0].actions.append((func.__name__, call))

    return wrapper

class MultiRhythm(m21.stream.Stream):
    ''' Controller class for duplicating and modulating rhythms '''

    def __init__(self, rhythm=None):

        super().__init__()

        if rhythm == None: raise TypeError("__init__() missing 1 required positional argument: 'rhythm'")
        self.default_rhythm = rhythm
        self.current_rhythm = deepcopy(rhythm)
        self.rhythms = [self.current_rhythm]

        # Store all actions taken to repeat them later
        self.actions = []

    def __repr__(self):
        return f"MultiRhythm(default_rhythm={self.default_rhythm})"

    @property
    def notes(self):
        return [note for rhythm in self.rhythms for note in rhythm.notes]

    @action
    def copy(self, copies=1, _save_action=True):
        ''' Duplicate rhythm in current state
        
            Parameters
                copies: int
                    how many copies of the current rhythm to make
                save_action: bool
                    record this in the actions attribute for rebuilding
                    for internal usage when this function is called within another function '''

        for i in range(copies):
            self.rhythms.append(deepcopy(self.current_rhythm))

        if _save_action:
            return (('copies', copies), ('_save_action', _save_action))

    @action
    def modulate(self, direction='forward', name=None, copies=1, _save_action=True):
        ''' Modulate and create add copies to object '''
        
        self.current_rhythm.modulate(direction, name)
        self.copy(copies, _save_action=False)

        if _save_action:
            return (('direction', direction), ('name', name), ('copies', copies), ('_save_action', _save_action))

###############################################################################
#                                                                             #
#                                                                             #
#                                    Grids                                    #
#                                                                             #
#                                                                             #
###############################################################################

def make_16th_note_grid(rhythm=None):

    # Define default rhythm and modulator
    if not rhythm:
        rhythm = Rhythm(1/16)
        rhythm.add_note('R')
        rhythm.add_note('L')
        rhythm.add_note('R')
        rhythm.add_note('L')
        rhythm.add_modulator(Accent(), 0, 'accent')

    mr = MultiRhythm(rhythm)
    mr.copy(3) # Fill out first bar
    [mr.modulate(copies=int(dur)) for dur in '4'*3 + '2'*4 + '1'*4]

    return mr
        
