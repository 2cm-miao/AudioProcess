import math
import threading
from functools import partial

import pyaudio as pa
import numpy as np

import audioDataProcess


class AudioDataRead:
    def __init__(self):
        self.audioProcess = None
        self.pyAudio = None

        # audio data format
        self.info = None
        self.frameBuffer = None
        self.stream = None
        self.channels = None
        self.deviceIndex = None
        self.rate = None
        self.format = None

        # thread information
        self.ifReading = False
        self.ReadingThread = None

    # def calculate_rms(self, data, width):
    #     # 将音频数据转换为 NumPy 数组
    #     audio_data = np.frombuffer(data, dtype=np.int16)
    #
    #     # 计算 RMS 值
    #     rms = np.sqrt(np.mean(audio_data ** 2))
    #
    #     return rms

    def startReadData(self):
        self.audioProcess = audioDataProcess.AudioDataProcess()
        self.pyAudio = pa.PyAudio()
        self.ifReading = True

        self.info = self.pyAudio.get_default_input_device_info()
        self.rate = int(self.info['defaultSampleRate'])
        self.deviceIndex = self.info['index']
        self.channels = self.info['maxInputChannels']
        # self.frameBuffer = self.roundUpToEven(self.rate / 1000)
        self.frameBuffer = 4098
        self.format = pa.paInt32

        self.stream = self.pyAudio.open(input_device_index=self.deviceIndex,
                                        format=self.format,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frameBuffer,
                                        start=False)

        self.stream.start_stream()

        # self.ReadingThread = threading.Thread(target=self.audioProcess.dynamicSpectrogramProcess,
        #                                       args=(self.stream,
        #                                             self.ifReading,
        #                                             self.frameBuffer,
        #                                             self.format,
        #                                             self.rate))
        # self.ReadingThread.start()

        return self.stream, self.frameBuffer, self.format, self.rate

        # for _ in range(0, int(self.rate / self.frameBuffer * 5)):
        # data = self.stream.read(self.frameBuffer)
        # # frames.append(data)
        #
        # # 在这里处理音频数据
        # rms = self.calculate_rms(data, self.pyAudio.get_sample_size(self.format))
        # print("RMS:", rms)

    def stopReadData(self):
        self.ifReading = False
        # self.ReadingThread.join()
        self.stream.stop_stream()
        self.stream.close()
        self.pyAudio.terminate()

    @staticmethod
    def roundUpToEven(num):
        return int(math.ceil(num / 2.) * 2)

    # def readingData(self):
    #     while self.ifReading:
    #         data = self.stream.read(self.frameBuffer)
    #         rms = self.calculate_rms(data, self.pyAudio.get_sample_size(self.format))
    #         print("RMS:", rms)

    # 在这里处理音频数据
    # print("监控中...")
