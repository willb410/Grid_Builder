class MultiRhythm():

    def __init__(self, *rhythms):

        self.rhythms = [*rhythms]

    @property
    def notes(self):
        return [note for rhythm in self.rhythms for note in rhythm.notes]
    
    def add(self, *rhythms):

        self.rhythms.extend()

