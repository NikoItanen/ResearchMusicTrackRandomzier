from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl, QObject, pyqtSignal

class Player(QObject):
    track_finished = pyqtSignal()
    
    def __init__(self, volume=0.5):
        super().__init__()
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(volume)
        self.player.mediaStatusChanged.connect(self._on_media_status_changed)

    def play(self, track_path):
        url = QUrl.fromLocalFile(track_path)
        self.player.setSource(url)
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def set_volume(self, volume):
        self.audio_output.setVolume(volume)

    def _on_media_status_changed(self, status):
        from PyQt6.QtMultimedia import QMediaPlayer
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.track_finished.emit()