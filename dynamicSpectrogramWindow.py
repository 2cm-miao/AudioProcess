import numpy as np
import pyaudio as pa
import soundcard as sc
import pygame

from audioDataRead import AudioDataRead


class DynamicSpectrogramWindow:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 1200, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('2D Dynamic Spectrogram')

        # audioRead = AudioDataRead()
        # self.stream, self.frameBuffer, self.format, self.rate, self.pyAudio = audioRead.startReadData()

        virtual_microphone = next(mic for mic in sc.all_microphones() if 'BlackHole' in mic.name)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # self.stopReadData()
                    running = False

            if not running:
                break

            with virtual_microphone.recorder(samplerate=44100) as mic:
                data = mic.record(numframes=2400)
                # print(data)
                self.dynamicSpectrogramProcessTest(data, 44100)

            # self.dynamicSpectrogramProcess(self.stream, self.frameBuffer, self.format, self.rate)

        pygame.display.quit()
        pygame.quit()

    # def stopReadData(self):
    #     audioRead = AudioDataRead()
    #     audioRead.stopReadData(self.stream, self.pyAudio)

    def drawDynamicSpectrogram(self, audioFrequency, audioSpectrum):
        # print(audioFrequency, audioSpectrum)
        # clean the screen
        self.screen.fill((0, 0, 0))

        # draw 2D dynamic spectrogram
        num_bars = len(audioFrequency // 2)
        # bar_width = self.screen_width // num_bars
        maxValue = np.max(audioFrequency)
        minValue = np.min(audioFrequency)
        for i in range(num_bars - 1):
            x = i
            if audioSpectrum[i] > 0:
                y = self.screen_height - audioSpectrum[i] * 10
            else:
                y = self.screen_height - np.abs(audioSpectrum[i])
            height = self.screen_height - y
            rect = pygame.Rect(x, y, 1, height)
            color = self.drawColor(audioFrequency[i], minValue, maxValue)
            pygame.draw.rect(self.screen, color, rect)

        # update the screen
        pygame.display.flip()

    def fftFunction(self, data, rate):
        # if format == pa.paInt16:
        #     format = np.int16
        # elif format == pa.paInt32:
        #     format = np.int32
        # elif format == pa.paInt24:
        #     format = np.int24
        # else:
        #     format = np.int8
        #
        # audioData = np.frombuffer(data, dtype=format)
        # audioData = data[:, 0]
        # audioSpectrum = np.fft.rfft(audioData)
        # audioFrequency = np.fft.rfftfreq(len(audioData), 1 / rate)
        #
        # audioSpectrum = self.calculateDBValue(audioSpectrum)

        # test part
        # window_length = len(data)
        # hamming_window = np.hamming(window_length)
        # windowed_data = np.zeros_like(data)
        # windowed_data[:, 0] = data[:, 0] * hamming_window
        # windowed_data[:, 1] = data[:, 1] * hamming_window

        audioData = data[:, 0]
        windowed_data = audioData * np.hamming(len(audioData))
        audioFrequency = np.fft.rfftfreq(len(windowed_data), 1 / rate)
        audioSpectrum = np.fft.fft(windowed_data)

        # calculate the dBValue
        left, right = np.split(np.abs(audioSpectrum), 2)
        audioSpectrum = np.add(left, right[::-1])
        audioSpectrum = np.multiply(20, np.log10(audioSpectrum))

        return audioFrequency, audioSpectrum
        # return audioFrequency, FFT

    def dynamicSpectrogramProcess(self, stream, frameBuffer, format, rate):
        data = stream.read(frameBuffer, exception_on_overflow=False)
        audioFrequency, audioSpectrum = self.fftFunction(data, rate)

        self.drawDynamicSpectrogram(audioFrequency, audioSpectrum)

    def dynamicSpectrogramProcessTest(self, data, rate):
        audioFrequency, audioSpectrum = self.fftFunction(data, rate)

        self.drawDynamicSpectrogram(audioFrequency, audioSpectrum)

    @staticmethod
    def calculateDBValue(spectrum):
        magnitudes = np.abs(spectrum)
        dBValue = 20 * np.log10(magnitudes + 1e-8)

        return dBValue

    @staticmethod
    def drawColor(dBValue, minValue, maxValue):
        ratio = (dBValue - minValue) / (maxValue - minValue)
        r, g, b = int(255 * ratio), int(255 * (1 - ratio)), 0
        return r, g, b
