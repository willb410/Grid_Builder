from copy import deepcopy
import music21 as m21
from utils import define_dynamic

class Modifier:
    ''' A notation object that modifies a note 
        Values of 0 passed to parameter indicate no modification '''

    name = 'Modifier'
    modifier_type = 'Parent'

    def __init__(self, location, duration=0, dynamic=0, note=None):

        self.location = location # Placement around Note
        self.duration = duration
        self.dynamic = define_dynamic(dynamic)

        # Note the Modifier is being applied to
        self._note = note

        # Mark this Modifier as a modulator, if not it is a constant
        self.modulator = False

    def __repr__(self):
        att_vals = [f"{att}={val}, " for att, val in self.__dict__.items() if val]
        return f"{self.name}({''.join(att_vals)})"


class BaseModifier:
    ''' Defining interaction attributes for Note objects 
        Should not be instantiated directly as some methods are set to feed
        into child classes'''
    def __init__(self):
        
        self.modulator = False
        self._note = None

    def add(self, note):
        note.modifiers.append(self)
        self._note = note

    def remove(self):
        note = self._note
        self._note = None

        for i, mod in enumerate(note.modifiers):
            if mod is self:
                note.modifiers.pop(i)
                return i, note
        else:
            return 0, None

###############################################################################
#                                                                             #
#                                  Duration                                   #
#                                                                             #
###############################################################################

class Dot(Modifier):
    ''' Make a Note dotted
        Multiplies the duration of a Note by 1.5 
        Should not be created directly, requires Note object for context'''

    name = 'Dot'
    modifier_type = 'duration'

    def __init__(self, note):
        super().__init__(location='right', note=note)
        self.duration = self._note.duration * 1.5

class DoubleDot(Modifier):
    ''' Make a Note double dotted
        Multiplies the duration of a Note by 1.75
        Should not be created directly, requires Note object for context'''

    name = 'DoubleDot'
    modifier_type = 'duration'

    def __init__(self, note):
        super().__init__(location='right', note=note)
        self.duration = self._note.duration * 1.75

###############################################################################
#                                                                             #
#                                Articulations                                #
#                                                                             #
###############################################################################

# class Accent(Modifier):

#     name = 'Accent'
#     modifier_type = 'articulation'

#     def __init__(self, location: str='top', dynamic=12):
#         super().__init__(location=location, dynamic=dynamic)

class Articulation(BaseModifier):

    def __init__(self):
        super().__init__()

    def add(self, note):
        super().add(note)
        note.articulations.append(self)
        
    # def copy(self, note):
    #     self.add(note)

    def move(self, new_note):
        self.remove()
        self.add(new_note)

    def remove(self):
        i, note = super().remove()
        return note.articulations.pop(i)

class Accent(m21.articulations.Accent, Articulation):

    name = 'Accent'
    modifier_type = 'articulation'

    def __init__(self, modulator=False, location='above'):
        super().__init__()

        # Where the Accent goes in relation to the note, one of ['above', 'below']
        self.placement = location

        self.modulator = modulator

class Marcato(Modifier):

    name = 'Marcato'
    modifier_type = 'articulation'

    def __init__(self, location: str='top', dynamic=15):
        super().__init__(location=location, dynamic=dynamic)

class Staccato(Modifier):
    ''' For purposes of marching percussion, Staccato is used as an Accent 
        variation since note duration is not a concern '''
    name = 'Staccato'
    modifier_type = 'articulation'

    def __init__(self, location: str='top', dynamic=6):
        super().__init__(location=location, dynamic=dynamic)

class Tenuto(Modifier):

    name = 'Tenuto'
    modifier_type = 'articulation'

    def __init__(self, location: str='top', dynamic=9):
        super().__init__(location=location, dynamic=dynamic)

###############################################################################
#                                                                             #
#                                   Tremolo                                   #
#                                                                             #
###############################################################################

class Diddle(Modifier):

    name = 'Diddle'
    modifier_type = 'tremolo'

    def __init__(self, location: str='stem'):
        super().__init__(location=location)

class Buzz(Modifier):

    name = 'Buzz'
    modifier_type = 'tremolo'

    def __init__(self, location: str='stem'):
        super().__init__(location=location)

###############################################################################
#                                                                             #
#                                 Grace Notes                                 #
#                                                                             #
###############################################################################

class Flam(Modifier):

    name = 'Flam'
    modifier_type = 'grace note'

    def __init__(self, location: str='left'):
        super().__init__(location=location)

class Drag(Modifier):

    name = 'Drag'
    modifier_type = 'grace note'

    def __init__(self, location: str='left'):
        super().__init__(location=location)

class ThreeStrokeDrag(Modifier):

    name = 'ThreeStrokeDrag'
    modifier_type = 'grace note'

    def __init__(self, location: str='left'):
        super().__init__(location=location)

###############################################################################
#                                                                             #
#                              Repeats and Jumps                              #
#                                                                             #
###############################################################################

class StartRepeat(Modifier):
    ''' Marks Bar an EndRepeat will return to 
        Assign to a Bar object '''

    name = 'StartRepeat'
    modifier_type = 'repeat and jump'

    def __init__(self):
        super().__init__(location='left')

class EndRepeat(Modifier):
    ''' Marks Bar after which it will return to the associated StartRepeat
        Assign to a Bar object '''

    name = 'EndRepeat'
    modifier_type = 'repeat and jump'

    def __init__(self):
        super().__init__(location='right')

class RepeatBar(Modifier):

    name = 'RepeatBar'
    modifier_type = 'repeat and jump'

    def __init__(self):
        super().__init__(location='center')