
import numpy as np
import moderngl
import imgui
from UI.window import Window
from moderngl_window.integrations.imgui import ModernglWindowRenderer

# PGRF2 - David Továrek 2021

class Logmap(Window):
    title = "Logistic map"
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
                    color = vec4(1.0, 0.0, 0.0, 1.0);
                }
            ''',
        )

        self.picProg = self.ctx.program(
            vertex_shader='''
                #version 330
                in vec2 vert;
                out vec2 v_text;


                void main() {

                    gl_Position = vec4(vert, 0.0, 1.0);
                    v_text = vec2(vert.x+0.5,vert.y-0.1);
                }
            ''',
            fragment_shader='''
                #version 330

                uniform sampler2D Texture;

                in vec2 v_text;

                out vec4 outColor;
                void main() {
                    outColor = texture(Texture, v_text, 0.0);
                }
            ''',
        )

        self.picProg['Texture'] = 0
        self.texture = self.load_texture_2d('logmap.png')

        self.r = 3

        vertices = np.array([
            0.5, 1.0,
            -0.5, 1.0,
            -0.5, 0.1,
            0.5, 0.1,
        ], dtype='f4')

        self.line = np.array([
            -0.0845, 0.25,
            -0.0845, 0.925,
        ], dtype='f4')

        self.pic_vbo = self.ctx.buffer(vertices)
        self.pic_vao = self.ctx.simple_vertex_array(self.picProg, self.pic_vbo, 'vert')

        self.line_vbo = self.ctx.buffer(self.line)
        self.line_vao = self.ctx.simple_vertex_array(self.prog, self.line_vbo, 'vert')

        self.vbo = self.ctx.buffer(self.generateFunc().astype('f4'))
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'vert')


    def render(self, time: float, frame_time: float):

        self.fps = 1/frame_time

        back = (0.2, 0.2, 0.2)
        self.ctx.clear(back[0],back[1],back[2])
        self.vao.render(mode=moderngl.LINE_STRIP)

        self.texture.use(0)
        self.pic_vao.render(moderngl.TRIANGLE_FAN)

        self.line_vao.render(mode=moderngl.LINES)

        self.render_ui()

    def generateFunc(self):

        positions = np.linspace(-0.9,0.9,100)
        out = []
        x = 0.5
        for pos in range(100):
            out.append(positions[pos])
            out.append(x-1)
            x = self.r*x*(1-x)

        return np.array(out)
            

    def render_ui(self):
        imgui.new_frame()


        imgui.begin("Description - Logistic map ", False)
        imgui.text("R: %.2f" % self.r)
        imgui.text("FPS: %.2f" % self.fps)
        imgui.text("==========================")
        imgui.text("The top picture shows the ")
        imgui.text("Bifurcation diagram of the Logistic map.")
        imgui.text("The bottom graph shows the first")
        imgui.text("64 values with x starting at 0,5.")
        imgui.text("For R > 3, the values in the population")
        imgui.text("will approach oscilation between two values")
        imgui.text("this later changes to 4, 8 etc. values.")
        imgui.text("At roughly R > 3.57 there are no longer")
        imgui.text("oscilations with a finite period,")
        imgui.text("with the exceptions of small islands")
        imgui.text("where values oscilate, before becoming")
        imgui.text("chaotic once again.")
        imgui.end()

        imgui.begin("Controls - Logistic map", False)
        imgui.text("Press LEFT and RIGHT to")
        imgui.text("change the value of R")
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
        if key == self.wnd.keys.RIGHT and action == self.wnd.keys.ACTION_PRESS:
            self.changeR(True)
        if key == self.wnd.keys.LEFT and action == self.wnd.keys.ACTION_PRESS:
            self.changeR(False)


    def changeR(self, up):
        if (up and self.r < 3.99):
            self.r = self.r + 0.01
            self.line[0] = self.line[0] + 0.00485
            self.line[2] = self.line[2] + 0.00485
            self.updateVao()
        if ((not up) and self.r > 2.4):
            self.r = self.r - 0.01
            self.line[0] = self.line[0] - 0.00485
            self.line[2] = self.line[2] - 0.00485
            self.updateVao()

    def updateVao(self):
        self.vbo = self.ctx.buffer(self.generateFunc().astype('f4'))
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'vert')
        self.line_vbo = self.ctx.buffer(self.line)
        self.line_vao = self.ctx.simple_vertex_array(self.prog, self.line_vbo, 'vert')


if __name__ == '__main__':
    Logmap.run()



