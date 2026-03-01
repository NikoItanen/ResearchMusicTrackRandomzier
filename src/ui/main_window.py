from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from experiment.randomizer import Randomizer
from experiment.player import Player
from experiment.logger import Logger

class TrackPreperationThread(QThread):
    finished = pyqtSignal(list)

    def __init__(self, randomizer, subject_id, session_id):
        super().__init__()
        self.randomizer = randomizer
        self.subject_id = subject_id
        self.session_id = session_id

    def run(self):
        track_list = self.randomizer.get_track_order(self.subject_id, self.session_id)
        self.finished.emit(track_list)

class MainWindow(QMainWindow):
    def __init__(self):
        # Initialize the main window
        super().__init__()
        self.setWindowTitle("Music Track Randomizer")
        self.setGeometry(200, 200, 600, 400)

        # ----- UI Components -----

        # Set up the central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)


        # Subject label to display current subject ID
        self.subject_label = QLabel("Subject ID: None")

        # Session label to display current session status
        self.session_label = QLabel("Status: Waiting")

        # Track label to display current track name
        self.track_label = QLabel("Current Track: None")

        # Genre label to display current track genre
        self.track_genre_label = QLabel("Current Genre: None")

        # Session time label to display elapsed session time
        self.session_time_label = QLabel("Session Time: 0s")

        # Progress bar to show track progress
        self.progress_bar = QProgressBar()

        # Start button to begin the session
        self.start_button = QPushButton("Start Session")

        # Next button to move to the next track (FOR TESTING PURPOSES)
        #self.next_button = QPushButton("Next Track")

        # Add widgets to the layout
        for w in [
            self.subject_label,
            self.session_label,
            self.track_label,
            self.track_genre_label,
            self.session_time_label,
            self.progress_bar,
            self.start_button,
            #self.next_button
        ]:
            self.layout.addWidget(w)
        
        # Connect button signals to their respective slots
        self.start_button.clicked.connect(self.start_session)
        #self.next_button.clicked.connect(self.next_track)
        #self.next_button.setEnabled(False) # Disable the next button until the session starts

        # Core components
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.randomizer = Randomizer()
        self.player = Player()
        self.player.track_finished.connect(self.next_track)
        self.logger = Logger()

        # State variables
        self.session_tracks = []
        self.current_track_index = 0
        self.session_elapsed_time = 0
        self.prep_thread = None

        # Run preparation after initializing the UI
        self.start_preparation()

    # ----- Session Control Methods -----

    # Method to start the session and play the first track if track list is available
    def start_session(self):
        self.logger.start_session(subject_id="subject_001", session_id="session_001")
        self.play_track(self.session_tracks[self.current_track_index])
        self.start_button.setEnabled(False) # Disable the start button once the session starts
        # self.next_button.setEnabled(True) # FOR TESTING PURPOSES

    def start_preparation(self):
        if self.prep_thread and self.prep_thread.isRunning():
            return
        
        self.prep_thread = TrackPreperationThread(self.randomizer, subject_id="subject_001", session_id="session_001")
        self.prep_thread.finished.connect(self.on_preparation_finished)
        self.prep_thread.start()
        self.session_label.setText("Status: Preparing Tracks...")

    def on_preparation_finished(self, track_list):
        self.session_tracks = track_list
        self.session_label.setText("Status: Tracks prepared. Waiting for break to finish...")

    # Method to move to the next track in the session (USED FOR TESTING PURPOSES)
    def next_track(self):
        self.current_track_index += 1
        if self.current_track_index < len(self.session_tracks):
            self.play_track(self.session_tracks[self.current_track_index])
        else:
            last_track = self.session_tracks[self.current_track_index - 1]
            self.session_break(last_track)
            self.session_label.setText("Status: Session Complete")

    def play_track(self, track):
        self.track_label.setText(f"Current Track: {track['name']}")
        self.track_genre_label.setText(f"Current Genre: {track['genre']}")
        self.player.play(track['path'])
        self.logger.log_track_start(track)
        self.progress_bar.setMaximum(30)
        self.progress_bar.setValue(0)
        self.timer.start(1000)
        self.session_label.setText("Status: Playing")

    def session_break(self, track):
        self.player.stop()
        self.logger.log_track_end(track)
        self.progress_bar.setValue(0)
        self.session_label.setText("Status: Break")
        self.track_label.setText("Current Track: None")
        self.track_genre_label.setText(f"Last genre: {track['genre']}")
        self.randomizer.clearTrackList() # Clear the track list to reset the session for the next round of tracks
        self.current_track_index = 0 # Reset track index for the next session
        self.session_tracks = []

        self.start_preparation() # Start preparing the next session's tracks in the background

        # Wait for a two minutes before starting the next track list
        QTimer.singleShot(20000, self.start_session)
        

    def update_progress(self):
        current_value = self.progress_bar.value()
        if current_value < self.progress_bar.maximum():
            self.progress_bar.setValue(current_value + 1)
        else:
            self.timer.stop()

        # Update session elapsed time
        self.session_elapsed_time += 1
        self.session_time_label.setText(f"Session Time: {self.session_elapsed_time}s")
