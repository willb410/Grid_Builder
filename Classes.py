from utils import define_dynamic

        
class Bar:

    def __init__(self, previous_bar, beat_count=4, beat_unit=4):

        self._previous_bar = previous_bar # Reference bar just before current, use Sheet object for first bar
        
        self._beat_count = beat_count # top of time signature
        self._beat_unit = beat_unit # bottom of time signature

        self.rehearsal_marking = None

    @property
    def time_signature(self):
        return (self._beat_count, self._beat_unit)

    @ property
    def duration(self):
        return self._beat_count / self._beat_unit

    def set_time_signature(self, beat_count, beat_unit):
        self._beat_count, self._beat_unit = beat_count, beat_unit




class Sheet:
    ''' Contains overall information '''
    pass




class Crescendo:
    ''' Manage dynamic changes over a period '''
    pass
