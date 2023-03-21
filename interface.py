from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QFileDialog, QHBoxLayout, QLabel,
                             QSizePolicy, QSlider, QStyle, QVBoxLayout)
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QAction
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from audioDataProcess import AudioDataProcess as audioProcess
from dynamicSpectrogramWindow import DynamicSpectrogramWindow
from threeDDynamicSpectrogramWindow import ThreeDDynamicSpectrogramWindow
import audioDataRead

audioRead = audioDataRead.AudioDataRead()


class WindowFunction(QMainWindow):

    def __init__(self, parent=None):
        self.spectrogramWin = None
        self.dynamicSpectrogramWin = None
        self.toolbar = None
        self.canvas = None
        self.axs = None
        self.fig = None
        self.fileName = ''

        super(WindowFunction, self).__init__(parent)
        self.setWindowTitle("Video Player")

        # widgets
        # video player
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()

        # play button
        self.playButton = QPushButton()
        self.playButton.setEnabled(True)
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
        self.fig, self.axs = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
        self.toolbar = NavigationToolbar(self.canvas, self)

        # actions
        # Create open file action
        openAction = QAction('&Open File', self)
        openAction.triggered.connect(self.openFile)

        # Create spectrogram showing action
        soundTrackSpectrogramAction = QAction('Spectrogram', self)
        soundTrackSpectrogramAction.triggered.connect(self.openStaticSpectrogramWin)

        # create an action to open dynamic spectrogram window
        audio2DDynamicSpectrogramAction = QAction('2D Dynamic Spectrogram', self)
        audio2DDynamicSpectrogramAction.triggered.connect(self.open2DDynamicSpectrogramWin)

        audio3DDynamicSpectrogramAction = QAction('3D Dynamic Spectrogram', self)
        audio3DDynamicSpectrogramAction.triggered.connect(self.open3DDynamicSpectrogramWin)

        # Create a menu bar
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openAction)

        spectrogramMenu = menuBar.addMenu('Spectrogram')
        spectrogramMenu.addAction(soundTrackSpectrogramAction)
        spectrogramMenu.addAction(audio2DDynamicSpectrogramAction)
        spectrogramMenu.addAction(audio3DDynamicSpectrogramAction)

        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        self.controlLayout = QHBoxLayout()
        self.controlLayout.setContentsMargins(0, 0, 0, 0)
        self.controlLayout.addWidget(self.playButton)
        self.controlLayout.addWidget(self.positionSlider)

        # Create layouts to place spectrogram
        self.spectrogramLayout = QVBoxLayout()
        self.spectrogramLayout.addWidget(self.canvas)
        self.spectrogramLayout.addWidget(self.toolbar)
        self.spectrumLabel.setLayout(self.spectrogramLayout)

        # Create the main layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.videoWidget)
        self.mainLayout.addLayout(self.controlLayout)
        # mainLayout.addWidget(self.errorLabel)
        self.mainLayout.addWidget(self.spectrumLabel)

        # Set widget to contain window contents
        wid.setLayout(self.mainLayout)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        self.setGeometry(100, 100, 1500, 1000)

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

    def open2DDynamicSpectrogramWin(self):
        self.dynamicSpectrogramWin = DynamicSpectrogramWindow()

    def open3DDynamicSpectrogramWin(self):
        self.dynamicSpectrogramWin = ThreeDDynamicSpectrogramWindow()

    def openStaticSpectrogramWin(self):
        self.spectrogramWin = audioProcess.twoDSpectrogramProcess(self.fileName, self.canvas, self.axs)
