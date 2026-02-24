import random
from pathlib import Path

class Randomizer:
    def __init__(self, assets_dir="assets/audio"):
        self.assets_dir = Path(assets_dir)
        self.genres = [p.name for p in self.assets_dir.iterdir() if p.is_dir()]
        self.genre_tracks = {genre: list((self.assets_dir / genre).glob("*.mp3")) for genre in self.genres}

    def get_track_order(self, subject_id=None, session_id=None):
        seed_str = f"{subject_id}_{session_id}" if subject_id and session_id else None
        if seed_str:
            random.seed(seed_str)

        genres = self.genres.copy()
        random.shuffle(genres)

        session_tracks = []
        for genre in genres:
            tracks = self.genre_tracks[genre].copy()
            random.shuffle(tracks)
            for t in tracks:
                session_tracks.append({"genre": genre, "path": str(t), "name": t.name, "duration": 0})

        return session_tracks