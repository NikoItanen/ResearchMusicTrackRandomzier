GENRES = ["Classical", "Jazz", "Hip-Hop", "Electronic", "Experimental"]

DEFAULT_BASELINE_DURATION = 5 * 60 # Baseline duration of 5 minutes
DEFAULT_GENRE_DURATION = 8 * 60 # Duration of each genre played
DEFAULT_BREAK_DURATION = 3 * 60 # Break duration of 3 minutes

GENRE_RULES = {
    "Classical": {
        "tempo_range": (70, 110),
        "centroid_range": (900, 2100),
        "rmse_mean_range": (0.02, 0.10),
        "spectral_rolloff_range": (2000, 4500)
    },
    "Jazz": {
        "tempo_range": (75, 170),
        "centroid_range": (1200, 2600),
        "rmse_mean_range": (0.04, 0.16),
        "spectral_rolloff_range": (2800, 5200)
    },
    "Hip-Hop": {
        "tempo_range": (65, 110),
        "centroid_range": (850, 2300),
        "rmse_mean_range": (0.09, 0.22),
        "spectral_rolloff_range": (2200, 4800)
    },
    "Electronic": { # Focusing on techno music
        "tempo_range": (120, 150),
        "centroid_range": (2000, 4500),
        "rmse_mean_range": (0.30, 0.80),
        "spectral_rolloff_range": (4200, 8500)
    },
    "Experimental": { # Focusing on noise music
        "tempo_range": (70, 200),
        "centroid_range": (2000, 4500),
        "rmse_mean_range": (0.22, 0.65),
        "spectral_rolloff_range": (5500, 11000)
    }
}