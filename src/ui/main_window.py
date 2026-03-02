from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from experiment.randomizer import Randomizer
from experiment.player import Player
from experiment.logger import Logger
from ui.logger_menu import LoggerMenu

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
        
        # Session label to display current session ID
        self.session_number_label = QLabel("Session Number: None")

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

        # Logger menu button to handle logging information
        self.logger_menu_button = QPushButton("Logger Menu")

        # Next button to move to the next track (FOR TESTING PURPOSES)
        #self.next_button = QPushButton("Next Track")

        # Add widgets to the layout
        for w in [
            self.subject_label,
            self.session_number_label,
            self.session_label,
            self.track_label,
            self.track_genre_label,
            self.session_time_label,
            self.progress_bar,
            self.start_button,
            self.logger_menu_button,
            #self.next_button,
        ]:
            self.layout.addWidget(w)
        
        # Connect button signals to their respective slots
        self.start_button.clicked.connect(self.start_session)
        self.logger_menu_button.clicked.connect(self.open_logger_menu)
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
        self.subject_id = None
        self.session_id = None
        self.current_track = None
        self.event_counter = 0

        # Run preparation after initializing the UI
        self.start_preparation()

    # ----- Session Control Methods -----

    # Method to start the session and play the first track if track list is available
    def start_session(self):
        if self.subject_id is None or self.session_id is None:
            self.session_label.setText("Status: Please enter subject and session information in the Logger Menu before starting the session.")
            return
        elif self.event_counter >= 1:
            self.event_counter += 1
            self.logger.log_break_end(block_id=self.event_counter - 1) # Log the break end event for the first break
            self.play_track(self.session_tracks[self.current_track_index])
        else:
            self.event_counter += 1
            self.logger.start_session(subject_id=self.subject_id, session_id=self.session_id)
            self.play_track(self.session_tracks[self.current_track_index])
            self.start_button.setEnabled(False) # Disable the start button once the session starts
            self.logger_menu_button.setEnabled(False) # Disable the logger menu button once the session starts
            # self.next_button.setEnabled(True) # FOR TESTING PURPOSES

    def start_preparation(self):
        if self.prep_thread and self.prep_thread.isRunning():
            return
        
        self.prep_thread = TrackPreperationThread(self.randomizer, subject_id=self.subject_id, session_id=self.session_id)
        self.prep_thread.finished.connect(self.on_preparation_finished)
        self.prep_thread.start()
        self.session_label.setText("Status: Preparing Tracks...")

    def on_preparation_finished(self, track_list):
        self.session_tracks = track_list
        self.session_label.setText("Status: Tracks prepared. Waiting for break to finish...")

    # Method to move to the next track in the session
    def next_track(self):
        if self.current_track is not None:
            self.logger.log_track_end(self.current_track, self.event_counter)  # Log the track end event
            self.current_track = None

        self.current_track_index += 1
        if self.current_track_index < len(self.session_tracks):
            self.play_track(self.session_tracks[self.current_track_index])
        else:
            last_track = self.session_tracks[self.current_track_index - 1]
            self.session_break(last_track)

    def play_track(self, track):
        # Update UI wth track informations
        self.track_label.setText(f"Current Track: {track['name']}")
        self.track_genre_label.setText(f"Current Genre: {track['genre']}")
        self.current_track = track

        # Play the track
        self.player.play(track['path'])

        # Log the track start event
        self.logger.log_track_start(track, self.event_counter)

        # Set up the progress bar and timer
        self.progress_bar.setMaximum(30)
        self.progress_bar.setValue(0)
        self.timer.start(1000)

        # Change session status to playing
        self.session_label.setText("Status: Playing")

    def session_break(self, track):
        if self.event_counter >= 3:
            self.session_label.setText("Status: Session Completed!")
            self.logger.end_session()
            return
        else:
            # Stop the player
            self.player.stop()

            # Log the track ending and the break start event
            self.logger.log_break_start(block_id=self.event_counter)

            # Reset UI for break
            self.progress_bar.setValue(0)
            self.session_label.setText("Status: Break")
            self.track_label.setText("Current Track: None")
            self.track_genre_label.setText(f"Last genre: {track['genre']}")

            # Initialization for the next event
            self.current_track_index = 0 # Reset track index for the next session
            self.session_tracks = []
            self.start_preparation() # Start preparing the next session's tracks in the background

            # Wait for a two minutes before starting the next track list
            QTimer.singleShot(15000, self.start_session)
        
    # Method to update the progress bar and session elapsed time every second
    def update_progress(self):
        current_value = self.progress_bar.value()
        if current_value < self.progress_bar.maximum():
            self.progress_bar.setValue(current_value + 1)
        else:
            self.timer.stop()

        # Update session elapsed time
        self.session_elapsed_time += 1
        self.session_time_label.setText(f"Session Time: {self.session_elapsed_time}s")

    # Logger menu method to open the logger dialog
    def open_logger_menu(self):
        # Open the logger menu dialog to get subject and session information
        logger_menu = LoggerMenu()
        
        # If the user clicks the save button in the logger menu, update the subject and session information in the main window
        if logger_menu.exec():
            subject_id, session_id = logger_menu.get_data()
            
            self.subject_id = subject_id
            self.session_id = session_id

            self.subject_label.setText(f"Subject ID: {self.subject_id}")
            self.session_number_label.setText(f"Session Number: {self.session_id}")