import numpy as np
import tkinter as tk
from tkinter import ttk
import moderngl
import imgui
import scipy.io.wavfile as scipyio
import winsound
from UI.window import Window
from moderngl_window.integrations.imgui import ModernglWindowRenderer

class Music(Window):
    title = "Title"
    gl_version = (3, 3)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        imgui.create_context()
        self.imgui = ModernglWindowRenderer(self.wnd)

        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330
                in vec2 vert;
                uniform float dataPlot[1000];
                uniform bool up;
                
                out float gradient;

                void main() {

                    gl_PointSize = 3;

                    if (up) {
                        gl_Position = vec4(vert.x, (dataPlot[gl_VertexID]+1)/2, 0.0, 1.0);
                    }
                    else {
                        gl_Position = vec4(vert.x, (dataPlot[gl_VertexID]-1)/2, 0.0, 1.0);
                    }
                    gradient = dataPlot[gl_VertexID]*4;
               
                }
            ''',
            fragment_shader='''
                #version 330

                uniform vec2 resolution;

                in float gradient;

                out vec4 outColor;
                void main() {

                    vec3 color = mix(vec3(1.0,1.0,1.0),vec3(1.0,0.0,0.0),abs(gradient));
                    outColor = vec4(color,1.0); 
                }
            ''',
        )

        self.dataPlot = self.prog['dataPlot']
        self.up = self.prog['up']
        self.up.value = True


        self.song = 1

        if (self.song == 1):
            path = 'data/sweet_dreams.wav'
        if (self.song == 2):
            path = 'data/omnissiah.wav'
        if (self.song == 3):
            path = 'data/never.wav'

        self.rate, self.audio = scipyio.read(path)


        self.vbo = self.ctx.buffer(self.initLines().astype('f4'))
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'vert')

        winsound.PlaySound(path, winsound.SND_ASYNC | winsound.SND_ALIAS)

    def render(self, time: float, frame_time: float):
        self.ctx.enable_only(moderngl.PROGRAM_POINT_SIZE)
        self.fps = 1/frame_time

        self.ctx.clear(0.2, 0.2, 0.2)

        self.up.value = True
        self.calculateSample(self.audio[:,0],time)
        self.vao.render(mode=moderngl.POINTS)

        self.up.value = False
        self.calculateSample(self.audio[:,1],time)
        self.vao.render(mode=moderngl.POINTS)

        self.render_ui()

    def calculateSample(self,channel,time):
        bigTime = int(time * self.rate)
        value = (channel[0+bigTime:1000+bigTime]/(32767*2)).tolist()
        self.dataPlot.value = value

    def initLines(self):
        u = np.linspace(-0.8, 0.8, 1000)
        v = np.repeat(0.0,1000)

        return np.array(list(zip(u,v))).flatten()

    def render_ui(self):
        imgui.new_frame()


        imgui.begin("Description - Music", False)
        imgui.text("Lorem ipsum")
        imgui.text("FPS: %.2f" % self.fps)
        imgui.end()


        imgui.begin("Controls - Music", False)
        imgui.text("Press A/D to dolor sit amet")
        imgui.end()



        imgui.render()
        self.imgui.render(imgui.get_draw_data())

    # Events for imgui
    def mouse_position_event(self, x, y, dx, dy):
        self.imgui.mouse_position_event(x, y, dx, dy)

    def mouse_drag_event(self, x, y, dx, dy):
        self.imgui.mouse_drag_event(x, y, dx, dy)

    def mouse_scroll_event(self, x_offset, y_offset):
        self.imgui.mouse_scroll_event(x_offset, y_offset)

    def mouse_press_event(self, x, y, button):
        self.imgui.mouse_press_event(x, y, button)

    def mouse_release_event(self, x: int, y: int, button: int):
        self.imgui.mouse_release_event(x, y, button)

    # Events to interact with the visualisation
    def key_event(self, key, action, modifiers):
        print(key)




if __name__ == '__main__':
    Music.run()


