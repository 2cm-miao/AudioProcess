import os
import librosa
import numpy as np
import pyaudio as pa
from moviepy.video.io.VideoFileClip import VideoFileClip
from dynamicSpectrogramWindow import DynamicSpectrogramWindow as dys


class AudioDataProcess:
    def __init__(self):
        self.update = None

    # @staticmethod
    # def fftFunction(data, rate, format):
    #     if format == pa.paInt16:
    #         format = np.int16
    #     elif format == pa.paInt32:
    #         format = np.int32
    #     elif format == pa.paInt24:
    #         format = np.int24
    #     else:
    #         format = np.int8
    #
    #     audioData = np.frombuffer(data, dtype=format)
    #     audioSpectrum = np.fft.rfft(audioData)
    #     audioFrequency = np.fft.rfftfreq(len(audioData), 1 / rate)
    #
    #     return audioFrequency, audioSpectrum
    #
    # def dynamicSpectrogramProcess(self, stream, ifReading, frameBuffer, format, rate):
    #     # while ifReading:
    #     data = stream.read(frameBuffer, exception_on_overflow=False)
    #     audioFrequency, audioSpectrum = self.fftFunction(data, rate, format)
    #
    #     self.updateSpectrogramData(audioFrequency, audioSpectrum)
    #     # print(audioFrequency, audioSpectrum)
    #
    # @staticmethod
    # def updateSpectrogramData(fre, spe):
    #     print(fre, spe)
    #     # self.update = DynamicSpectrogramWindow()
    #     dys.drawDynamicSpectrogram(fre, spe)

    @staticmethod
    def twoDSpectrogramProcess(fileName, canvas, axs):
        # get the filename of the file
        file_extension = os.path.splitext(fileName)[1]
        if file_extension == '.mp4':
            video = VideoFileClip(fileName)
            audio = video.audio
            fileBasename = os.path.splitext(fileName)[0]
            audio.write_audiofile(fileBasename + '.mp3')

        y, sr = librosa.load(fileName, sr=16000)
        spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
        log_spectrogram = librosa.power_to_db(spectrogram, ref=np.max)

        axs.cla()
        librosa.display.specshow(log_spectrogram, sr=sr, x_axis="time", y_axis="mel", ax=axs)
        canvas.draw()

        # x, sr = librosa.load(self.fileName, sr=16000)
        # spectrogram = librosa.amplitude_to_db(librosa.stft(x))
        # librosa.display.specshow(spectrogram, y_axis='log')
        # plt.colorbar(format='%+2.0f dB')
        # plt.title('spectrogram')
        # plt.xlabel('time(second)')
        # plt.ylabel('Hertz(Hz)')
        # plt.show()
