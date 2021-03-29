
import numpy as np
import moderngl
import imgui
import math
from pyrr import Matrix44, Quaternion, Vector3, vector
from UI.window import Window
from util.camera import Camera
from moderngl_window.integrations.imgui import ModernglWindowRenderer

class Heatmap(Window):
    title = "Title"
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

                void main() {
                    gl_PointSize = 3;
                    gradient = (vert.z+1)*0.5;
                    gl_Position = Mvp * vec4(vert, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330

                in float gradient;

                out vec4 outColor;

                void main() {

                    vec3 colorA = vec3(1.0,0.1,0.1);
                    vec3 colorB = vec3(0.0,0.0,1.0);

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
            return np.sin(np.sqrt(x ** 2 + y ** 2))
        if func == 4:
            return np.sin(np.sqrt(x ** 2 + y ** 2))



    def render(self, time: float, frame_time: float):

        # Camera animation
        self.camera.move_forward()
        self.camera.rotate_left()
        self.camera.move_backwards()

        self.mvp.write((self.camera.mat_projection * self.camera.mat_lookat).astype('f4'))

        self.ctx.enable(moderngl.DEPTH_TEST)

        self.ctx.enable_only(moderngl.PROGRAM_POINT_SIZE)
        back = (0.2, 0.2, 0.2)
        self.ctx.clear(back[0],back[1],back[2])
        self.vao.render(mode=moderngl.POINTS)

        self.render_ui()

    def render_ui(self):
        imgui.new_frame()


        imgui.begin("Description - aaa", False)
        imgui.text("Lorem ipsum")
        imgui.end()


        imgui.begin("Controls - aaa", False)
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



if __name__ == '__main__':
    Heatmap.run()


