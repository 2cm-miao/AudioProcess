import numpy as np
import pyaudio as pa
import soundcard as sc
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from audioDataRead import AudioDataRead


class ThreeDDynamicSpectrogramWindow:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 1200, 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), DOUBLEBUF | OPENGL)
        pygame.display.set_caption('3D Dynamic Spectrogram')

        # glMatrixMode(GL_PROJECTION)
        # glLoadIdentity()
        # glOrtho(10, self.screen_width, 0, self.screen_height, -1, 1)
        # glOrtho(100, self.screen_width + 100, 50, self.screen_height + 50, -1, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        gluPerspective(45, (self.screen_width / self.screen_height), 0.1, 50.0)
        glTranslatef(-10.0, 0.0, -30)

        glEnable(GL_DEPTH_TEST)

        virtual_microphone = next(mic for mic in sc.all_microphones() if 'BlackHole' in mic.name)

        xRotation = 0
        yRotation = 0
        dragging = False
        self.scaleFlag = True

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        prev_mouse_x, prev_mouse_y = event.pos
                        dragging = True

                if event.type == MOUSEBUTTONUP:
                    if event.button == 1:
                        dragging = False

                if event.type == MOUSEMOTION:
                    if dragging:
                        dx, dy = event.rel
                        xRotation += dy * 0.5
                        yRotation += dx * 0.5

            if not running:
                break

            with virtual_microphone.recorder(samplerate=44100) as mic:
                data = mic.record(numframes=2400)
                # print(data)
                self.dynamicSpectrogramProcess(data, 44100)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glPushMatrix()
            glRotatef(xRotation, 1, 0, 0)
            glRotatef(yRotation, 0, 1, 0)
            # glScalef(0.5, 0.5, 0.5)
            # self.drawAxes()
            glPopMatrix()

            # pygame.display.flip()

        pygame.display.quit()
        pygame.quit()

    def dynamicSpectrogramProcess(self, data, param):
        audioFrequency, realPart, imagPart = self.fftFunction(data, param)
        self.draw3DDynamicSpectrogram(audioFrequency, realPart, imagPart)

    @staticmethod
    def fftFunction(data, param):
        audioData = data[:, 0]
        windowed_data = audioData * np.hamming(len(audioData))
        audioFrequency = np.fft.rfftfreq(len(windowed_data), 1 / param)
        audioSpectrum = np.fft.fft(windowed_data)

        # calculate the dBValue
        # left, right = np.split(np.abs(audioSpectrum), 2)
        # audioSpectrum = np.add(left, right[::-1])
        # audioSpectrum = np.multiply(20, np.log10(audioSpectrum))

        realPart = audioSpectrum.real
        imagPart = audioSpectrum.imag

        return audioFrequency, realPart, imagPart

    def draw3DDynamicSpectrogram(self, fre, realPart, imagPart):
        self.screen.fill((0, 0, 0))
        vertices = []
        edges = []
        colors = []

        for i in range(len(fre) - 1):
            vertices.append((fre[i], realPart[i] * 10, imagPart[i] * 10))

        for i in range(len(vertices)):
            if i != len(vertices) - 1:
                edges.append((i, i + 1))
                colors.append((0, 1, 1))

        if self.scaleFlag:
            glScalef(np.power(0.5, 6), np.power(0.5, 6), np.power(0.5, 6))
            glTranslatef(-1900, 0, 0)
            self.scaleFlag = False


        glBegin(GL_LINES)
        for edge, color in zip(edges, colors):
            for vertex in edge:
                glColor3fv(color)
                glVertex3fv(vertices[vertex])
        glEnd()

        pygame.display.flip()

    def drawAxes(self):
        glBegin(GL_LINES)

        # X axis (Red)
        glColor3f(1, 0, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(self.screen_width, 0, 0)

        # Y axis (Green)
        glColor3f(0, 1, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, self.screen_height, 0)

        # Z axis (Blue)
        glColor3f(0, 0, 1)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, self.screen_height)

        glEnd()



