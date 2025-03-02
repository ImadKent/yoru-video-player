from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import (QApplication,
                               QMainWindow,
                               QVBoxLayout,
                               QWidget,
                               QHBoxLayout,
                               QPushButton,
                               QSlider,
                               QFileDialog)
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QIcon
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main Window Settings
        self.setWindowTitle("Yoru Video Player")
        self.setFixedSize(1280,720)
        self.setWindowIcon(QIcon("yoru.png"))
        # Create a Parent layout
        vertical_layout = QVBoxLayout()

        # Create Horizontal Layout for Buttons
        horizontal_layout = QHBoxLayout()

        # Create Media Player Settings
        self.player = QMediaPlayer()


        # Create Video Player
        self.video_player = CustomPlayer()

        # Audio output
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(50)

        # Video output
        self.player.setVideoOutput(self.video_player)
        # add Video Player to the layout
        vertical_layout.addWidget(self.video_player)

        # Add video Url
        self.player.setSource(QUrl.fromLocalFile(r"")) # Choose Path if you to load specific video

        # Create Play, Pause, Stop button
        self.play = QPushButton("▶️")
        self.pause = QPushButton("⏸")
        self.stop = QPushButton("⏹")
        self.add_video = QPushButton("📂")


        # Create Slider
        self.slider = QSlider()
        self.slider.setOrientation(Qt.Horizontal)


        # Create Buttons (Play,pause,etc) functions
        self.play.clicked.connect(self.triggerPlay)
        self.pause.clicked.connect(self.triggerPause)
        self.stop.clicked.connect(self.triggerStop)
        self.add_video.clicked.connect(self.openFileDir)
        self.slider.valueChanged.connect(self.sliderChanged)
        self.player.mediaStatusChanged.connect(self.resetSlider)
        self.player.durationChanged.connect(self.updateSliderRange)




        # Add Play Pause Stop to Horizontal layout

        horizontal_layout.addWidget(self.play)
        horizontal_layout.addWidget(self.pause)
        horizontal_layout.addWidget(self.stop)
        horizontal_layout.addWidget(self.add_video)
        horizontal_layout.addWidget(self.slider)
        vertical_layout.addLayout(horizontal_layout)


        # Show and play video
        self.video_player.show()
        self.player.play()
        # Container to add Widget to Mainwindow through layout
        container = QWidget()
        container.setLayout(vertical_layout)
        self.setCentralWidget(container)


    def triggerPause(self):
        self.player.pause()
    def triggerPlay(self):
        self.player.play()
    def triggerStop(self):
        self.player.stop()

    def sliderChanged(self,position):
        self.slider.setMaximum(self.player.duration()) # Link Slider to video duration
        self.player.setPosition(position)

    def resetSlider(self, status): # reset Slider when video is over
        if status == QMediaPlayer.MediaStatus.EndOfMedia: # If status == end of the video.
            self.slider.setValue(0) # Put Slider at 0 at the end of the video
            self.player.setPosition(0) # Video goes back to 0


    def openFileDir(self):
        file_directory, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier vidéo", "", "Videos (*.mp4 *.avi *.mkv)")

        if file_directory:  # Vérifie si un fichier a été sélectionné
            self.player.setSource(QUrl.fromLocalFile(file_directory))
            self.slider.setValue(0)
            self.player.setPosition(0)
            self.player.play()


    def updateSliderRange(self,duration):
        self.slider.setMaximum(duration)

class CustomPlayer(QVideoWidget):
    def __init__(self):
        super().__init__()

    def mouseDoubleClickEvent(self, event):
        if not self.isFullScreen():
            self.setFullScreen(True)
        elif self.isFullScreen() == True:
            self.setFullScreen(False)



app = QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec())
