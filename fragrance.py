from enum import Enum
from collections import defaultdict

class Fragrance:
    class NoteTypes(Enum):
        TOP = "top"
        MIDDLE = "middle"
        BASE = "base"
    
    def __init__(self, brand="", name="", unparsed_name="", website_link="", notes=None):
      
        self.brand = brand
        self.name = name
        self.unparsed_name = unparsed_name
        self.website_link = website_link
        if notes is None:
            notes = {note_type: [] for note_type in Fragrance.NoteTypes}
        self.notes = notes 

    def add_note(self, note_type, note):
        """Adds a note to the notes dictionary under the specified NoteType."""
        if note_type not in self.notes:
            self.notes[note_type] = []
        self.notes[note_type].append(note)

    def __repr__(self):
        return (f"Fragrance(brand='{self.brand}', name='{self.name}', "
                f"unparsed_name='{self.unparsed_name}', website_link='{self.website_link}', "
                f"notes={self.notes})")
