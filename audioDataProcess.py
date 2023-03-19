import os

import librosa
import numpy as np
from PyQt5.QtMultimedia import QAudioBuffer
from moviepy.video.io.VideoFileClip import VideoFileClip


class AudioDataProcess:
    def __init__(self):
        pass

    def threeDSpectrogramProcess(self, buffer: QAudioBuffer):
        # get the filename of the file
        # file_extension = os.path.splitext(self.fileName)[1]
        # if file_extension == '.mp4':
        #     video = VideoFileClip(self.fileName)
        #     audio = video.audio
        #     fileBasename = os.path.splitext(self.fileName)[0]
        #     audio.write_audiofile(fileBasename + '.mp3')
        # print(f'Buffer received: {buffer.frameCount()} frames')
        print(buffer.startTime())

    def twoDSpectrogramProcess(self, fileName, canvas, axs):
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

        # self.axs.cla()
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
