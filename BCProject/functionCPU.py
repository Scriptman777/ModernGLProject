import numpy as np
import moderngl
import imgui
import math
from pyrr import Matrix44, Quaternion, Vector3, vector
from UI.window import Window
from util.camera import Camera
from moderngl_window.integrations.imgui import ModernglWindowRenderer

class Heatmap(Window):
    title = "Functions/Heatmaps"
    gl_version = (3, 3)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        imgui.create_context()
        self.imgui = ModernglWindowRenderer(self.wnd)

        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330
                in vec3 vert;

                out float gradient;

                uniform mat4 Mvp;
                uniform int size;

                void main() {
                    gl_PointSize = size;
                    gradient = (vert.z+1)*0.5;
                    gl_Position = Mvp * vec4(vert, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330

                in float gradient;

                uniform vec3 colorA;
                uniform vec3 colorB;

                out vec4 outColor;

                void main() {

                    vec3 color = mix(colorA,colorB,gradient);
                    outColor = vec4(color, 1.0);
                }
            ''',
        )

        # Camera setup
        self.camera = Camera(self.aspect_ratio)
        self.camera._camera_position = Vector3([0.0, 0.0, -20.0])
        self.camera._move_horizontally = 20
        self.camera.build_look_at()

        self.mvp = self.prog['Mvp']
        self.colorA = self.prog['colorA']
        self.colorB = self.prog['colorB']
        self.size = self.prog['size']

        self.colorA.value = (0.1,1.0,0.0)
        self.colorB.value = (0.0,0.0,1.0)
        self.colorSelector = 0
        self.size.value = 5

        self.vbo = self.ctx.buffer(self.initData(1).astype('f4'))
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'vert')

        
        
    def initData(self,function):
        x = np.linspace(-8, 8, 200)
        y = np.linspace(-8, 8, 200)
        out = []

        for i in range(len(x)):
            for j in range(len(y)):
                out = np.append(out,[x[i],y[j],self.calcFunc(x[i],y[j],function)])

        return out


    def calcFunc(self,x,y,func):
        if func == 1:
            return math.sin(math.sqrt(x ** 2 + y ** 2))
        if func == 2:
            return math.cos(x)*math.sin(y)
        if func == 3:
            return math.cos(40*math.sqrt(x**2+y**2))
        if func == 4:
            return math.cos(math.fabs(x) + math.fabs(y))
        if func == 5:
            return 8*math.exp(-x**2-y**2)*(0.1+x*(y-0.5))
        if func == 6:
            return math.exp(math.sin(x*2)*math.sin(y*0.2))*0.9 * math.exp(math.sin(y*2) * math.sin(x*0.2))*0.9-0.7



    def render(self, time: float, frame_time: float):

        self.fps = 1/frame_time

        # Camera animation
        self.camera.move_forward()
        self.camera.rotate_left()
        self.camera.move_backwards()

        self.mvp.write((self.camera.mat_projection * self.camera.mat_lookat).astype('f4'))

        self.ctx.enable_only(moderngl.PROGRAM_POINT_SIZE | moderngl.DEPTH_TEST)
        back = (0.2, 0.2, 0.2)
        self.ctx.clear(back[0],back[1],back[2])
        self.vao.render(mode=moderngl.POINTS)

        self.render_ui()

    def render_ui(self):
        imgui.new_frame()


        imgui.begin("Description - Functions", False)
        imgui.text("This is a visualisation of two variable functions")
        imgui.text("Points are colored based on their Z coordinate")
        imgui.text("Same visualisation could be used for heatmaps or simillar data")
        imgui.text("FPS: %.2f" % self.fps)
        imgui.end()


        imgui.begin("Controls - Functions", False)
        imgui.text("UP and DOWN to change colors")
        imgui.text("Press 1,2,3,4,5,6 to change function")
        imgui.text("LEFT and RIGHT to change point size")
        imgui.text_colored("Warning:", 1,0,0)
        imgui.text("Depending on your machine, this may take a while")
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
        if key == 49 and action == self.wnd.keys.ACTION_PRESS:
            self.vbo = self.ctx.buffer(self.initData(1).astype('f4'))
            self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'vert')
        if key == 50 and action == self.wnd.keys.ACTION_PRESS:
            self.vbo = self.ctx.buffer(self.initData(2).astype('f4'))
            self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'vert')
        if key == 51 and action == self.wnd.keys.ACTION_PRESS:
            self.vbo = self.ctx.buffer(self.initData(3).astype('f4'))
            self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'vert')
        if key == 52 and action == self.wnd.keys.ACTION_PRESS:
            self.vbo = self.ctx.buffer(self.initData(4).astype('f4'))
            self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'vert')
        if key == 53 and action == self.wnd.keys.ACTION_PRESS:
            self.vbo = self.ctx.buffer(self.initData(5).astype('f4'))
            self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'vert')
        if key == 54 and action == self.wnd.keys.ACTION_PRESS:
            self.vbo = self.ctx.buffer(self.initData(6).astype('f4'))
            self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'vert')
        if key == self.wnd.keys.UP and action == self.wnd.keys.ACTION_PRESS:
            self.colorSelect(True)
        if key == self.wnd.keys.DOWN and action == self.wnd.keys.ACTION_PRESS:
            self.colorSelect(False)
        if key == self.wnd.keys.LEFT and action == self.wnd.keys.ACTION_PRESS:
            self.sizeSelect(True)
        if key == self.wnd.keys.RIGHT and action == self.wnd.keys.ACTION_PRESS:
            self.sizeSelect(False)

    def sizeSelect(self,up):
        if up:
            self.size.value = self.size.value + 1
        else:
            self.size.value = self.size.value - 1



    def colorSelect(self,up):
        if up:
            self.colorSelector = self.colorSelector + 1
        else:
            self.colorSelector = self.colorSelector - 1

        if self.colorSelector % 4 == 0:
            self.colorA.value = (0.1,1.0,0.0)
            self.colorB.value = (0.0,0.0,1.0)
        elif self.colorSelector % 4 == 1:
            self.colorA.value = (1.0,0.5,0.0)
            self.colorB.value = (0.25,0.0,0.4)
        elif self.colorSelector % 4 == 2:
            self.colorA.value = (1.0,1.0,1.0)
            self.colorB.value = (0.0,0.0,0.0)
        elif self.colorSelector % 4 == 3:
            self.colorA.value = (1.0,0.0,0.0)
            self.colorB.value = (1.0,1.0,0.0)
        


if __name__ == '__main__':
    Heatmap.run()


