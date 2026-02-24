import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

def run_app():
    app = QApplication(sys.argv)

    # Create the main window and show it
    main_window = MainWindow()
    main_window.show()

    # Run the event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    run_app()