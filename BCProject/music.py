import numpy as np
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
                uniform float dataPlot[1024];
                

                void main() {

                gl_PointSize = 3;

                if (true) {  //DONT FORGET THIS
                    gl_Position = vec4(vert.x, dataPlot[gl_VertexID], 0.0, 1.0);
                }
                else {
                    gl_Position = vec4(vert.x, dataPlot[gl_VertexID], 0.0, 1.0);
                }
                
                    
                }
            ''',
            fragment_shader='''
                #version 330

                uniform vec2 resolution;

                out vec4 outColor;
                void main() {

                    outColor = vec4(1.0,1.0,1.0,1.0); 
                }
            ''',
        )

        self.dataPlot = self.prog['dataPlot']
        #self.up = self.prog['up']


        self.rate, self.audio = scipyio.read('data/sweet_dreams.wav')


        self.vbo = self.ctx.buffer(self.initLines().astype('f4'))
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'vert')

        filename = 'data/sweet_dreams.wav'
        winsound.PlaySound(filename, winsound.SND_ASYNC | winsound.SND_ALIAS)


    def render(self, time: float, frame_time: float):
        self.ctx.enable_only(moderngl.PROGRAM_POINT_SIZE)

        onechannel = self.audio[:,0]

        bigTime = int(time * 44100)
        value = (onechannel[0+bigTime:1024+bigTime]/(32767*2)).tolist()
        self.dataPlot.value = value

        self.fps = 1/frame_time

        #self.up.value = true
        self.ctx.clear(0.2, 0.2, 0.2)
        self.vao.render(mode=moderngl.POINTS)

        self.render_ui()



    def initLines(self):
        u = np.linspace(-0.8, 0.8, 1024)
        v = np.repeat(0.0,1024)

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


