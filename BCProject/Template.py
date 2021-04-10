
import numpy as np
import moderngl
import imgui
from UI.window import Window
from moderngl_window.integrations.imgui import ModernglWindowRenderer

class Name(Window):
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

                void main() {

                    gl_Position = vec4(vert, 0.0, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330

                out vec4 color;
                void main() {
                    color = vec4(0.3, 0.5, 1.0, 1.0);
                }
            ''',
        )



        vertices = np.array([
            1.0, 0.0,
            -0.5, 0.86,
            -0.5, -0.86,
        ], dtype='f4')

        self.vbo = self.ctx.buffer(vertices)
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'vert')



    def render(self, time: float, frame_time: float):

        self.fps = 1/frame_time

        back = (0.2, 0.2, 0.2)
        self.ctx.clear(back[0],back[1],back[2])
        self.vao.render(mode=moderngl.TRIANGLES)

        self.render_ui()

    def render_ui(self):
        imgui.new_frame()


        imgui.begin("Description - aaa", False)
        imgui.text("Lorem ipsum")
        imgui.text("FPS: %.2f" % self.fps)
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
    Name.run()


