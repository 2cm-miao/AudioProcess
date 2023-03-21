import math
import pyaudio as pa
import soundcard as sc
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

    def startReadData(self):
        self.audioProcess = audioDataProcess.AudioDataProcess()
        self.pyAudio = pa.PyAudio()
        self.ifReading = True

        self.info = self.pyAudio.get_default_input_device_info()
        # self.info = self.pyAudio.get_default_output_device_info()
        self.rate = int(self.info['defaultSampleRate'])
        self.deviceIndex = self.info['index']
        self.channels = self.info['maxInputChannels']
        # self.channels = self.info['maxOutputChannels']
        # self.frameBuffer = self.roundUpToEven(self.rate / 1000)
        self.frameBuffer = 2400
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

        return self.stream, self.frameBuffer, self.format, self.rate, self.pyAudio

    @staticmethod
    def stopReadData(stream, pyAudio):
        # self.ReadingThread.join()
        stream.stop_stream()
        stream.close()
        pyAudio.terminate()

    @staticmethod
    def roundUpToEven(num):
        return int(math.ceil(num / 2.) * 2)
