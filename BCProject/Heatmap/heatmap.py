
import numpy as np
import moderngl
import imgui
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

                out float origZ;

                uniform mat4 Mvp;

                void main() {
                    gl_PointSize = 5;
                    origZ = vert.z;
                    gl_Position = Mvp * vec4(vert, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330

                in float origZ;

                out vec4 color;
                void main() {

                    color = vec4(origZ, origZ, 1.0, 0.5);
                }
            ''',
        )

        # Camera setup
        self.camera = Camera(self.aspect_ratio)
        self.camera._camera_position = Vector3([0.0, 0.0, -20.0])
        self.camera._move_horizontally = 20
        self.camera.build_look_at()



        self.mvp = self.prog['Mvp']

        self.vbo = self.ctx.buffer(self.initData().astype('f4'))
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'vert')

        
        
    def initData(self):
        x = np.linspace(-8, 8, 200)
        y = np.linspace(-8, 8, 200)
        out = []

        for i in range(len(x)):
            for j in range(len(y)):
                out = np.append(out,[x[i],y[j],np.sin(np.sqrt(x[i] ** 2 + y[j] ** 2))])

        return out



    def render(self, time: float, frame_time: float):

        self.camera.move_forward()
        self.camera.rotate_left()
        self.camera.move_backwards()

        self.mvp.write((self.camera.mat_projection * self.camera.mat_lookat).astype('f4'))

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
        print(key)




if __name__ == '__main__':
    Heatmap.run()


