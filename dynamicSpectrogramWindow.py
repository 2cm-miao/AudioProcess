import numpy as np
import soundcard as sc
import pygame


class DynamicSpectrogramWindow:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 1200, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('2D Dynamic Spectrogram')

        virtual_microphone = next(mic for mic in sc.all_microphones() if 'BlackHole' in mic.name)

        running = True
        self.ifFlag = True
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
                self.dynamicSpectrogramProcess(data, 44100)

        pygame.display.quit()
        pygame.quit()

    # update dynamic spectrogram
    def drawDynamicSpectrogram(self, audioFrequency, audioSpectrum):
        self.screen.fill((0, 0, 0))

        # draw 2D dynamic spectrogram
        numBars = len(audioFrequency // 2)
        maxValue = np.max(audioFrequency)
        minValue = np.min(audioFrequency)
        for i in range(numBars - 1):
            x = i
            if audioSpectrum[i] > 0:
                y = self.screen_height - audioSpectrum[i] * 10
            else:
                y = self.screen_height - np.abs(audioSpectrum[i])
            height = self.screen_height - y
            rect = pygame.Rect(x, y, 1, height)
            color = self.drawColor(audioFrequency[i], minValue, maxValue)
            pygame.draw.rect(self.screen, color, rect)

        # draw frequency
        self.drawFrequencyRect(audioFrequency)

        # update the screen
        pygame.display.flip()

    # draw frequency information
    def drawFrequencyRect(self, fre):
        numRect = self.screen_width // 10
        freLen = len(fre)
        rectText = []
        i = 0
        while i < freLen:
            if i + 1 < freLen:
                freNum = fre[i + 1]
                i += numRect
                rectText.append(str(round(freNum)))
            else:
                break

        k = 0
        font = pygame.font.Font(None, 25)
        for i in range(len(rectText)):
            text = font.render(rectText[i] + ' Hz', True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.topleft = (k, self.screen_height - 18)
            k += numRect
            self.screen.blit(text, text_rect)

    # FFT calculate function
    @staticmethod
    def fftFunction(data, rate):
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

    def dynamicSpectrogramProcess(self, data, rate):
        audioFrequency, audioSpectrum = self.fftFunction(data, rate)

        self.drawDynamicSpectrogram(audioFrequency, audioSpectrum)

    # calculate DB value function
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
