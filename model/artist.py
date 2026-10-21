from dataclasses import dataclass


@dataclass
class Artist:
    ArtistId: int
    Name: str
    listaBrani: int
    playlist: int

    def __hash__(self):
        return hash(self.ArtistId)

    def __eq__(self, other):
        return self.ArtistId == other.ArtistId

    def __str__(self):
        return f'{self.Name}'