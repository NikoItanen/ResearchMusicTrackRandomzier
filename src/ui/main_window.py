from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar
from PyQt6.QtCore import Qt, QTimer
from experiment.randomizer import Randomizer
from experiment.player import Player
from experiment.logger import Logger

class MainWindow(QMainWindow):
    def __init__(self):
        # Initialize the main window
        super().__init__()
        self.setWindowTitle("Music Track Randomizer")
        self.setGeometry(200, 200, 600, 400)

        # Set up the central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        # Add UI Elements

        # Subject label to display current subject ID
        self.subject_label = QLabel("Subject ID: None")
        self.layout.addWidget(self.subject_label)

        # Session label to display current session status
        self.session_label = QLabel("Status: Waiting")
        self.layout.addWidget(self.session_label)

        # Track label to display current track name
        self.track_label = QLabel("Current Track: None")
        self.layout.addWidget(self.track_label)

        # Genre label to display current track genre
        self.track_genre_label = QLabel("Current Genre: None")
        self.layout.addWidget(self.track_genre_label)

        # Session time label to display elapsed session time
        self.session_time_label = QLabel("Session Time: 0s")
        self.layout.addWidget(self.session_time_label)

        # Progress bar to show track progress
        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

        # Start button to begin the session
        self.start_button = QPushButton("Start Session")
        self.start_button.clicked.connect(self.start_session)
        self.layout.addWidget(self.start_button)

        # Next button to move to the next track (FOR TESTING PURPOSES)
        self.next_button = QPushButton("Next Track")
        self.next_button.clicked.connect(self.next_track)
        self.next_button.setEnabled(False)
        self.layout.addWidget(self.next_button)

        # Initialize the timer, randomizer, player, and logger
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.randomizer = Randomizer()
        self.player = Player()
        self.player.track_finished.connect(self.next_track)
        self.logger = Logger()


        # Define track index variable
        self.current_track_index = 0
        
        # Retrive the track order for the session
        session_tracks = self.randomizer.get_track_order(subject_id="test_subject", session_id="test_session")
        self.session_tracks = session_tracks

        # Define variable to track elapsed time for the session
        self.session_elapsed_time = 0


    # Method to start the session and play the first track
    def start_session(self):
        # Handle session start logic here
        if self.current_track_index < len(self.session_tracks): # Track index cannot exceed the number of tracks
            self.play_track(self.session_tracks[self.current_track_index])
            self.next_button.setEnabled(True)
        else: # Otherwise, if there are no tracks to play, end the session
            self.session_label.setText("Status: Session Complete")
            self.next_button.setEnabled(False)
            self.progress_bar.setValue(0)

    # Method to move to the next track in the session
    def next_track(self):
        self.current_track_index += 1
        if self.current_track_index < len(self.session_tracks):
            self.play_track(self.session_tracks[self.current_track_index])
        else:
            self.session_label.setText("Status: Session Complete")
            self.next_button.setEnabled(False)
            self.progress_bar.setValue(0)

    def play_track(self, track):
        self.track_label.setText(f"Current Track: {track['name']}")
        self.track_genre_label.setText(f"Current Genre: {track['genre']}")
        self.player.play(track['path'])
        self.logger.log_track_start(track)
        self.progress_bar.setValue(0)
        self.timer.start(1000)

    def update_progress(self):
        current_value = self.progress_bar.value()
        if current_value < self.progress_bar.maximum():
            self.progress_bar.setValue(current_value + 1)
        else:
            self.timer.stop()

        # Update session elapsed time
        self.session_elapsed_time += 1
        self.session_time_label.setText(f"Session Time: {self.session_elapsed_time}s")
