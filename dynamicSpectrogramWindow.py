from functools import partial

import numpy as np
import pyaudio as pa
import pygame
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout, QPushButton, QStyle
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from pygame import time

from audioDataRead import AudioDataRead
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


# import audioDataRead

# audioRead = audioDataRead.AudioDataRead()


# class DynamicSpectrogramWindow(QMainWindow):
#     def __init__(self):
#         super(DynamicSpectrogramWindow, self).__init__()
#         self.setWindowTitle("Dynamic Spectrogram")
#
#         wid = QWidget(self)
#         self.setCentralWidget(wid)
#         self.setGeometry(300, 300, 1200, 600)
#
#         self.startButton = QPushButton()
#         self.startButton.setEnabled(True)
#         self.startButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
#         self.startButton.clicked.connect(self.startReadData)
#
#         self.stopButton = QPushButton()
#         self.stopButton.setEnabled(True)
#         self.stopButton.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
#         self.stopButton.clicked.connect(self.stopReadData)
#
#         plt.ion()
#         self.spectrumLabel = QLabel()
#         self.fig, self.axs = plt.subplots()
#         self.canvas = FigureCanvas(self.fig)
#         self.canvas.setParent(self)
#         # self.toolbar = NavigationToolbar(self.canvas, self)
#
#         self.xData = np.array([])
#         self.yData = np.array([])
#         self.line, = self.axs.plot(self.xData, self.yData)
#
#         self.spectrogramLayout = QVBoxLayout()
#         self.spectrogramLayout.addWidget(self.startButton)
#         self.spectrogramLayout.addWidget(self.stopButton)
#         self.spectrogramLayout.addWidget(self.canvas)
#         # self.spectrogramLayout.addWidget(self.toolbar)
#         self.spectrumLabel.setLayout(self.spectrogramLayout)
#
#         self.mainLayout = QVBoxLayout()
#         self.mainLayout.addWidget(self.spectrumLabel)
#         wid.setLayout(self.mainLayout)
#
#     @staticmethod
#     def startReadData():
#         audioRead = AudioDataRead()
#         audioRead.startReadData()
#
#     @staticmethod
#     def stopReadData():
#         audioRead = AudioDataRead()
#         audioRead.stopReadData()
#
#     def updateCanvas(self, xAxis, yAxis, frame):
#         self.xData = xAxis
#         self.yData = np.abs(yAxis)
#
#         self.line.set_data(self.xData, self.yData)
#         self.axs.relim()
#         self.axs.autoscale_view()
#
#         return self.line,
#
#     def drawDynamicSpectrogram(self, xAxis, yAxis):
#         FuncAnimation(self.fig, partial(self.updateCanvas, xAxis, yAxis), frames=None, interval=50, blit=True)
#         plt.show()


class DynamicSpectrogramWindow:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 1200, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('2D Dynamic Spectrogram')

        audioRead = AudioDataRead()
        self.stream, self.frameBuffer, self.format, self.rate = audioRead.startReadData()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stopReadData()
                    running = False

            self.dynamicSpectrogramProcess(self.stream, self.frameBuffer, self.format, self.rate)

    # @staticmethod
    # def startReadData():
    #     audioRead = AudioDataRead()
    #     audioRead.startReadData()

    @staticmethod
    def stopReadData():
        audioRead = AudioDataRead()
        audioRead.stopReadData()

    def drawDynamicSpectrogram(self, audioFrequency, audioSpectrum):
        # print(audioFrequency, audioSpectrum)
        # clean the screen
        self.screen.fill((0, 0, 0))

        # draw 2D dynamic spectrogram
        num_bars = len(audioFrequency // 2)
        bar_width = self.screen_width // num_bars
        for i in range(num_bars):
            x = i
            y = self.screen_height - audioSpectrum[i]
            rect = pygame.Rect(x, y, 3, y)
            pygame.draw.rect(self.screen, (255, 255, 255), rect)

        # update the screen
        pygame.display.flip()

    def fftFunction(self, data, rate, format):
        if format == pa.paInt16:
            format = np.int16
        elif format == pa.paInt32:
            format = np.int32
        elif format == pa.paInt24:
            format = np.int24
        else:
            format = np.int8

        audioData = np.frombuffer(data, dtype=format)
        audioSpectrum = np.fft.rfft(audioData)
        audioFrequency = np.fft.rfftfreq(len(audioData), 1 / rate)

        audioSpectrum = self.calculateDBValue(audioSpectrum)

        return audioFrequency, audioSpectrum

    def dynamicSpectrogramProcess(self, stream, frameBuffer, format, rate):
        data = stream.read(frameBuffer, exception_on_overflow=False)
        audioFrequency, audioSpectrum = self.fftFunction(data, rate, format)

        self.drawDynamicSpectrogram(audioFrequency, audioSpectrum)

    @staticmethod
    def calculateDBValue(spectrum):
        magnitudes = np.abs(spectrum)
        dBValue = 20 * np.log10(magnitudes + 1e-8)

        return dBValue
