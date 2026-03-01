import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from experiment.validator import Validator
import analysis.feature_extraction as feature_extraction

def test_validator():
    validator = Validator()
    # Test case 1: Valid track
    track1 = {
        "genre": "pop",
        "tempo": 120.0,
        "centroid_mean": 3000.0,
        "rmse_mean": 0.5
    }
    assert validator.validate_track(track1) == True

    # Test case 2: Invalid track
    track2 = {
        "genre": "pop",
        "tempo": 180.0,
        "centroid_mean": 3000.0,
        "rmse_mean": 0.5
    }
    assert validator.validate_track(track2) == False

    # Test case 3: Track with missing features (should be considered valid)
    track3 = {
        "genre": "pop",
        "tempo": 120.0,
        # Missing centroid_mean and rmse_mean
    }
    assert validator.validate_track(track3) == True
