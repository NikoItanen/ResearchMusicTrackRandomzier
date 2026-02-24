from dataclasses import dataclass

@dataclass
class Segment:
    subject_id: str
    session_id: str
    genre: str
    track_id: str
    start_time: float
    end_time: float