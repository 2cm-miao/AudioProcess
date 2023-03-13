from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QAction
from moviepy.editor import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import os
import matplotlib.pyplot as plt
import librosa.display
import numpy as np
# import imageio_ffmpeg


class WindowFunction(QMainWindow):

    def __init__(self, parent=None):
        self.toolbar = None
        self.canvas = None
        self.ax = None
        self.fig = None
        self.fileName = ''

        super(WindowFunction, self).__init__(parent)
        self.setWindowTitle("Video Player")

        # widgets
        # video player
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()

        # play button
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        # video slider
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        # error label
        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # spectrum label
        self.spectrumLabel = QLabel()
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # actions
        # Create open file action
        openAction = QAction('&Open File', self)
        openAction.triggered.connect(self.openFile)

        # Create spectrogram showing action
        soundTrackSpectrogramAction = QAction('Spectrogram', self)
        soundTrackSpectrogramAction.triggered.connect(self.spectrogramProcess)

        # Create a menu bar
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(soundTrackSpectrogramAction)

        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)

        # Create layouts to place spcetrogram
        self.spectrogramLayout = QVBoxLayout()
        self.spectrogramLayout.addWidget(self.canvas)
        self.spectrogramLayout.addWidget(self.toolbar)
        self.spectrumLabel.setLayout(self.spectrogramLayout)

        # Create the main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(videoWidget)
        mainLayout.addLayout(controlLayout)
        # mainLayout.addWidget(self.errorLabel)
        mainLayout.addWidget(self.spectrumLabel)

        # Set widget to contain window contents
        wid.setLayout(mainLayout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        # self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        self.setGeometry(100, 100, 2000, 2000)

    # open file function
    def openFile(self):
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Open File",
                                                       QDir.homePath())

        if self.fileName != '':
            self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(self.fileName)))
            self.playButton.setEnabled(True)

    # play the video
    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())

    def spectrogramProcess(self):
        # get the filename of the file
        file_extension = os.path.splitext(self.fileName)[1]
        if file_extension == '.mp4':
            video = VideoFileClip(self.fileName)
            audio = video.audio
            fileBasename = os.path.splitext(self.fileName)[0]
            audio.write_audiofile(fileBasename + '.mp3')

        y, sr = librosa.load(self.fileName, sr=16000)
        spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
        log_spectrogram = librosa.power_to_db(spectrogram, ref=np.max)

        # self.fig, self.ax = plt.subplots()
        # self.canvas = FigureCanvas(self.fig)
        # self.canvas.setParent(self)
        # self.toolbar = NavigationToolbar(self.canvas, self)

        self.ax.cla()
        librosa.display.specshow(log_spectrogram, sr=sr, x_axis="time", y_axis="mel", ax=self.ax)
        self.canvas.draw()

        # spectrogramLayout.addWidget(self.canvas)
        # spectrogramLayout.addWidget(self.toolbar)

        # x, sr = librosa.load(self.fileName, sr=16000)
        # spectrogram = librosa.amplitude_to_db(librosa.stft(x))
        # librosa.display.specshow(spectrogram, y_axis='log')
        # plt.colorbar(format='%+2.0f dB')
        # plt.title('spectrogram')
        # plt.xlabel('time(second)')
        # plt.ylabel('Hertz(Hz)')
        # plt.show()




