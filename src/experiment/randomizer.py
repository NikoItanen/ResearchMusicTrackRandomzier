import random
from pathlib import Path
import experiment.config
import pandas as pd
from experiment.validator import Validator
import analysis.feature_extraction as feature_extraction

# Randomizer class to generate a randomized track order for each genre
class Randomizer:
    # Initialize the randomizer with the path to the audio assets
    def __init__(self, assets_dir="assets/audio/fma_medium", metadata_path="assets/metadata/fma_metadata/tracks.csv"):
        self.assets_dir = Path(assets_dir)
        self.genres = experiment.config.GENRES # Get the list of genres from the config file
        self.session_played_genres = set() # Set to track genres played in the current session
        self.genre_tracks = self._build_genre_index(metadata_path)
        self.validator = Validator()

    # Method to randomize the genre
    def randomize_genre(self):
        randomized_genre = random.choice(self.genres)
        return randomized_genre
    
    # Method to add the played genre to the session tracking set
    def addPlayedGenre(self, genre):
        self.session_played_genres.add(genre)

    def _isGenreValid(self, track_dict):
        # Do feature extraction for the track
        features = feature_extraction.extract_features(track_dict["path"])

        # Combine the track information and features into a single dictionary for validation
        features["genre"] = track_dict["genre"]
        return self.validator.validate_track(features)

    # Method to build an index of tracks for each genre based on the metadata CSV file
    def _build_genre_index(self, metadata_path):
        # Read the metadata file and filter for the relevant columns
        df = pd.read_csv(metadata_path, index_col=0, header=[0, 1])
        # FMA data has a multi-index column structure, so we need to select the "track" level and then the relevant columns
        df = df["track"][["genre_top", "duration"]]

        # Initialize a dictionary to hold the tracks for each genre
        genre_dict = {genre: [] for genre in self.genres}

        #  Iterate through the metadata and populate the genre dictionary with track paths and durations
        for track_id, row in df.iterrows():
            # Find the genre for the track and check if it is in our list of genres
            genre = row["genre_top"]
        
            if genre not in genre_dict:
                continue

            # Construct the file path for the track based on its ID
            track_id_str = f"{track_id:06d}"
            folder = track_id_str[:3]
            filename = f"{track_id_str}.mp3"

            full_path = self.assets_dir / folder / filename
                
            # Check if the file exists before adding it to the genre dictionary
            if full_path.exists():
                genre_dict[genre].append({
                    "path": full_path,
                    "duration": row["duration"]
                })

        return genre_dict
        

    # Method to gather randomized track from the dataset for each genre
    def fetch_random_track(self, selected_genre):
        # Define the list of tracks for the selected genre
        tracks = self.genre_tracks.get(selected_genre, [])

        if not tracks:
            raise ValueError(f"No tracks found for genre: {selected_genre}")
        
        # Try to find a valid track
        max_attempts = 200
        for _ in range(max_attempts):
            # Randomly select a track from the list of tracks for the selected genre
            selected = random.choice(tracks)

            track_dict = {
                "genre": selected_genre,
                "path": str(selected["path"]),
                "name": selected["path"].name,
                "duration": selected["duration"]
            }
        

            if self._isGenreValid(track_dict):
                return track_dict
        
        raise ValueError(f"Could not find a valid track for genre: {selected_genre} after {max_attempts} attempts.")
    
    # Method to get the track order for a session based on the randomized genre selection
    def get_track_order(self, subject_id=None, session_id=None):

        track_list = []

        # Randomly select a genre and ensure it has not been played in the current session
        selected_genre = self.randomize_genre()

        # Prevent repetition of genres within the same session
        while selected_genre in self.session_played_genres:
            selected_genre = self.randomize_genre()

        # Finally, add the selected genre to the session tracking set to prevent future repetition
        self.addPlayedGenre(selected_genre)

        # Use previously made method to fetch a random track from the selected genre
        for _ in range(10): # Add 10 tracks from the selected genre to the track list
            track = self.fetch_random_track(selected_genre)
            track_list.append(track)

        return track_list