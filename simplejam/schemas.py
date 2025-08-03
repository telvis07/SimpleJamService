from typing import Tuple

from pydantic import BaseModel


class KeyChordProgression(BaseModel):
    key: str
    number_chord_sequence: Tuple[str, ...]
