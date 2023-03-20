from functools import partial
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
import audioDataRead

audioRead = audioDataRead.AudioDataRead()


class WindowFunction(QMainWindow):

    def __init__(self, parent=None):
        self.dynamicSpectrogramWin = None
        self.toolbar = None
        self.canvas = None
        self.axs = None
        self.fig = None
        self.fileName = ''
        self.fileName = '/Users/cmzhang/Downloads/test3.mp4'

        super(WindowFunction, self).__init__(parent)
        self.setWindowTitle("Video Player")

        # widgets
        # video player
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.videoWidget = QVideoWidget()

        # self.audioBuffer = QAudioBuffer()
        # self.audioProbe = QAudioProbe()
        # self.audioProbe.audioBufferProbed.connect(partial(audioProcess.twoDSpectrogramProcess, None, self.fileName,
        #                                                   self.canvas, self.axs))
        # self.audioProbe.setSource(self.mediaPlayer)
        # print(self.audioProbe.isActive())

        # self.audioFormat = QAudioFormat()
        # self.audioFormat.setSampleRate(48000)
        # self.audioFormat.setChannelCount(2)
        # self.audioFormat.setSampleSize(16)
        #
        # self.devices = QAudioDeviceInfo.availableDevices(QAudio.AudioOutput)
        # if self.devices:
        #     print(self.devices[3].deviceName())

        # play button
        self.playButton = QPushButton()
        # self.playButton.setEnabled(False)
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
        soundTrackSpectrogramAction.triggered.connect(partial(audioProcess.twoDSpectrogramProcess, self.fileName,
                                                              self.canvas, self.axs))

        # create an action to open dynamic spectrogram window
        audioDynamicSpectrogramAction = QAction('2D Dynamic Spectrogram', self)
        audioDynamicSpectrogramAction.triggered.connect(self.openDynamicSpectrogramWin)

        # Create a menu bar
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu('&File')
        fileMenu.addAction(openAction)

        spectrogramMenu = menuBar.addMenu('Spectrogram')
        spectrogramMenu.addAction(soundTrackSpectrogramAction)
        spectrogramMenu.addAction(audioDynamicSpectrogramAction)

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
            # stop read output data
            # audioRead.stopReadData()
        else:
            self.mediaPlayer.play()
            # start read output data
            # audioRead.startReadData()

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

    def openDynamicSpectrogramWin(self):
        self.dynamicSpectrogramWin = DynamicSpectrogramWindow()
        # self.dynamicSpectrogramWin.show()
