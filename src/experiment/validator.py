from pathlib import Path
from .config import GENRE_RULES

class Validator:
    def __init__ (self, genre_rules=None):
        self.genre_rules = genre_rules or GENRE_RULES
        
    def validate_track(self, track) -> bool:
        genre = track.get("genre")
        if genre not in self.genre_rules:
            return True # If no rules defined for the genre, consider it valid
        
        rule = self.genre_rules[genre]

        # Check tempo
        tempo = track.get("tempo")
        if tempo is not None:
            if not (rule["tempo_range"][0] <= tempo <= rule["tempo_range"][1]):
                return False
            
        # Check spectral centroid
        centroid_mean = track.get("centroid_mean")
        if centroid_mean is not None:
            low, high = rule.get("centroid_range", (None, None))
            if low is not None and centroid_mean < low:
                return False
            if high is not None and centroid_mean > high:
                return False
        
        # Check RMSE mean
        rmse_mean = track.get("rmse_mean")
        if rmse_mean is not None:
            low, high = rule.get("rmse_mean_range", (None, None))
            if low is not None and rmse_mean < low:
                return False
            if high is not None and rmse_mean > high:
                return False
        
        print(f"Track '{track.get('name')}' passed validation for genre '{genre}'.")
        return True