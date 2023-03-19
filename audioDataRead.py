import os

import pyaudio as pa


class AudioDataRead:
    def __init__(self):
        self.pyAudio = pa.PyAudio()
        # self.info = self.pyAudio.get_default_output_device_info()
        self.info = self.pyAudio.get_default_input_device_info()
        self.rate = int(self.info['defaultSampleRate'])
        self.deviceIndex = self.info['index']
        self.channels = self.info['maxInputChannels']
        self.update_window_n_frames = 1024
        print(self.info)
        self.stream = self.pyAudio.open(input_device_index=self.deviceIndex,
                                        format=pa.paInt32,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.update_window_n_frames)

