GENRES = ["Classical", "Jazz", "Hip-Hop", "Electronic", "Experimental"]

DEFAULT_BASELINE_DURATION = 5 * 60 # Baseline duration of 5 minutes
DEFAULT_GENRE_DURATION = 8 * 60 # Duration of each genre played
DEFAULT_BREAK_DURATION = 3 * 60 # Break duration of 3 minutes

GENRE_RULES = {
    "Classical": {
        "tempo_range": (110, 150),
        "centroid_range": (1100, 2300),
        "rmse_mean_range": (0.025, 0.12)
    },
    "Jazz": {
        "tempo_range": (100, 160),
        "centroid_range": (1200, 2800),
        "rmse_mean_range": (0.05, 0.18)
    },
    "Hip-Hop": {
        "tempo_range": (75, 110),
        "centroid_range": (1300, 3200),
        "rmse_mean_range": (0.08, 0.28)
    },
    "Electronic": { # Focusing on techno music
        "tempo_range": (110, 160),
        "centroid_range": (1300, 3800),
        "rmse_mean_range": (0.25, 0.75)
    },
    "Experimental": { # Focusing on noise music
        "tempo_range": (100, 200),
        "centroid_range": (1200, 4000),
        "rmse_mean_range": (0.20, 0.75)
    }
}