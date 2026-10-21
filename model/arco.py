from dataclasses import dataclass

from model.artist import Artist


@dataclass
class Arco:
    a1: Artist
    a2: Artist
    peso: int