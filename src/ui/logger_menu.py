from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit

class LoggerMenu(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Subject Information Logger")
        self.setGeometry(300, 300, 400, 200)

        self.layout = QVBoxLayout()

        # ---- UI Components ----
        self.info_label = QLabel("This is where you can log subject information and session details.")

        self.close_button = QPushButton("Close")

        self.subject_input = QLineEdit()

        self.session_input = QLineEdit()

        self.save_button = QPushButton("Save Information")
        self.save_button.setEnabled(False)  # Disable save button until both fields are filled

        # Add components to the layout
        for w in [
            self.info_label,
            QLabel("Subject ID:"),
            self.subject_input,
            QLabel("Session ID:"),
            self.session_input,
            self.save_button,
            self.close_button
        ]:
            self.layout.addWidget(w)

        self.setLayout(self.layout)

        # --- Connections ---
        self.close_button.clicked.connect(self.close)
        self.save_button.clicked.connect(self.accept)  # Accept the dialog to close it and return data
        self.subject_input.textChanged.connect(self.check_inputs)
        self.session_input.textChanged.connect(self.check_inputs)
    def get_data (self):
        subject_id = self.subject_input.text()
        session_id = self.session_input.text()
        return subject_id, session_id
    
    def check_inputs(self):
        if self.subject_input.text() and self.session_input.text():
            self.save_button.setEnabled(True)
        else:
            self.save_button.setEnabled(False)