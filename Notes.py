import music21 as m21

try:
    from .Classes import *
    from .Rhythms import *
    from .Modifiers import *
except:
    from Classes import *
    from Rhythms import *
    from Modifiers import *

class Note(m21.note.Note):

    def __init__(self, duration: float, sticking: str, *modifiers, dynamic=3, dotted=False):

        super().__init__()

        # Base properties
        self._duration = m21.duration.Duration(duration * 4) # Space taken up by rhythm, eigth note would be .125
        self._duration_default = self._duration
        self.sticking = sticking # R or L
        self._sticking_default = sticking
        self.dynamic = define_dynamic(dynamic) # dynamics dict or 1-15
        self._dynamic_default = self.dynamic

        # Visual attributes for displaying modifiers
        self.head = 0
        self.stem = 0
        self.tail = 0
        self.top = []
        self.bottom = []
        self.left = []
        self.right = []

        # Note objects to connect tail to
        self.stem_connection_left = None
        self.stem_connection_right = None

        self.stem_direction = 'up' #one of [up, down, none, double]

        # Modifier objects to change base properties
        self.modifiers = [*modifiers]
        if dotted in [True, 'single']: 
            self.modifiers.append(Dot(self))
        elif dotted == 'double': 
            self.modifiers.append(DoubleDot(self))
        self.apply_modifiers()

    def __repr__(self):
        mod_names = [(modifier.name, modifier.modulator) for modifier in self.modifiers]
        
        return f"Note({self.duration.type}, sticking={self.sticking}, dynamic={self.dynamic}, modifiers={mod_names})"

    #########################################
    #           Modifier Actions            #
    #########################################

    def add_modifier(self, modifier):

        # Skip modifier if it is already applied to Note
        if modifier.name in self.get_modifier_names() and not modifier.modulator: return
        self.modifiers.append(modifier)
        self.apply_modifiers()

    def add_modifiers(self, *modifiers):
        for mod in modifiers:
            self.add_modifier(mod)
    
    def apply_modifiers(self):
        
        for modifier in self.modifiers:
            
            modifier._note = self

            # Apply modified values
            [setattr(self, att, val) for att, val in modifier.__dict__.items() if hasattr(self, att) and val]

            # Attach to location
            loc = getattr(self, modifier.location)
            if loc != modifier: 
                loc.append(modifier)
            setattr(self, modifier.location, loc)

    def get_modifier_names(self):
        return [mod.name for mod in self.modifiers]

    def remove_modifier(self, name):
        ''' Remove modifier and reset values '''
        
        # Remove modifier from Note
        for i, modifier in enumerate(self.modifiers):
            if modifier.name == name:
                break
        removed_modifier = self.modifiers.pop(i)
        removed_modifier._note = None
        
        # Reset modified values in Note
        for att, val in modifier.__dict__.items():
            if hasattr(self, att) and val:
                setattr(self, att, self.__dict__[f"_{att}_default"])

        # Remove from location
        self.reset_locations()

        # Reapply modifiers in case another modifier of the same type exists
        self.apply_modifiers()

        return removed_modifier
        

    #########################################
    #             Other Actions             #
    #########################################

    def flip_sticking(self):
        if self.sticking == 'R':
            self.sticking = 'L'
        elif self.sticking == 'L':
            self.sticking = 'R'

    def get_musicxml(self):
        ''' Return MusicXML formatted string for the current Note state '''

        f"<note> \
             <unpitched> \
                <display-step>A</display-step> \
                <display-octave>3</display-octave> \
            </unpitched> \
            <duration>{'self.duration * self.beat_unit'}</duration> \
            <type>{'text version of note duration, ex. eigth'}</type> \
            <stem>{self.stem_direction}</stem> \
            "


    def reset_locations(self):
        self.head = 0
        self.stem = 0
        self.tail = 0
        self.top = []
        self.bottom = []
        self.left = []
        self.right = []