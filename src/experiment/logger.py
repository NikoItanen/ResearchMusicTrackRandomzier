import json
from pathlib import Path
from datetime import datetime

class Logger:
    def __init__(self, output_dir="data/raw"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.events = []
        
        self.subject_id = None
        self.session_id = None

    def start_session(self, subject_id, session_id):
        self.subject_id = subject_id
        self.session_id = session_id
        self.events = []  # Clear previous events
        self.log_event("session_start", {})

    def log_event(self, event_type, data):
        timestamp = datetime.now().isoformat()
        event = {
            "timestamp": timestamp,
            "subject_id": self.subject_id,
            "session_id": self.session_id,
            "event_type": event_type,
            "data": data
        }

        self.events.append(event)
        print(f"Logged event: {event_type} at {timestamp}")

    def log_track_start(self, track):
        self.log_event("track_start", {
            "genre": track["genre"],
            "track_name": track["name"],
            "track_path": track["path"]
        })
    
    def log_track_end(self, track):
        self.log_event("track_end", {
            "genre": track["genre"],
            "track_name": track["name"]
        })

    def log_break_start(self, break_type="short"):
        self.log_event("break_start", {"break_type": break_type})

    def log_break_end(self, break_type="short"):
        self.log_event("break_end", {"break_type": break_type})

    def save_session(self):
        if not self.subject_id or not self.session_id:
            raise ValueError("Subject ID and Session ID must be set before saving session data.")
        
        filename = self.output_dir / f"{self.subject_id}_session_{self.session_id}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.events, f, indent=4)
        print(f"Session data saved to {filename}")