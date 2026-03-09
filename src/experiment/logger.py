import csv
from pathlib import Path
from datetime import datetime

class Logger:
    def __init__(self, output_dir="data/raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.subject_id = None
        self.session_id = None
        self.events = []
        self.file = None
        self.writer = None

    def start_session(self, subject_id, session_id):
        self.subject_id = subject_id
        self.session_id = session_id
        filename = self.output_dir / f"{self.subject_id}_session_{self.session_id}.csv"

        self.file = open(filename, "w", newline="", encoding="utf-8")
        self.writer = csv.DictWriter(self.file, fieldnames=[
            "timestamp_ISO",
            "timestamp_epoch",
            "subject_id",
            "session_id",
            "block_id",
            "event_type",
            "genre",
            "track_name",
            ])
        self.writer.writeheader()

        self.log_event("session_start")

    def log_event(self, event_type, **kwargs):
        if not self.writer:
            raise ValueError("Session has not been started. Call start_session() before logging events.")

        row = {
            "timestamp_ISO": datetime.now().isoformat(),
            "timestamp_epoch": datetime.now().timestamp(),
            "subject_id": self.subject_id,
            "session_id": self.session_id,
            "block_id": None,
            "event_type": event_type,
            "genre": None,
            "track_name": None
        }

        row.update(kwargs)
        self.writer.writerow(row)
        self.file.flush()  # Ensure data is written to disk immediately

    def log_track_start(self, track, block_id=None):
        self.log_event("track_start",
            genre=track["genre"],
            track_name=track["name"],
            block_id=block_id
        )
    
    def log_track_end(self, track, block_id=None):
        self.log_event("track_end", 
            genre=track["genre"],
            track_name=track["name"],
            block_id=block_id
        )

    def log_break_start(self, block_id=None):
        self.log_event("break_start", block_id=block_id)

    def log_break_end(self, block_id=None):
        self.log_event("break_end", block_id=block_id)

    def log_baseline_start(self, block_id=None):
        self.log_event("baseline_start", block_id=block_id)

    def log_baseline_end(self, block_id=None):
        self.log_event("baseline_end", block_id=block_id)

    def log_recovery_start(self, block_id=None):
        self.log_event("recovery_start", block_id=block_id)

    def log_recovery_end(self, block_id=None):
        self.log_event("recovery_end", block_id=block_id)

    def end_session(self):
        self.log_event("session_end")
        if self.file:
            self.file.close()
            self.file = None
            self.writer = None