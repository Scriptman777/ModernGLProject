import numpy as np
import moderngl
import imgui
import tkinter as tk
from tkinter import filedialog
from UI.window import Window
from PIL import Image
from moderngl_window.integrations.imgui import ModernglWindowRenderer


class Histogram(Window):
    title = "Histogram"
    gl_version = (3, 3)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        imgui.create_context()
        self.imgui = ModernglWindowRenderer(self.wnd)

        self.prog2 = self.ctx.program(
            vertex_shader='''
                #version 330
                in vec2 vert;
                out vec2 v_text;

                void main() {
                    gl_Position = vec4(vert, 0.0, 1.0);
                    v_text = vert.xy*2;
                }
            ''',
            fragment_shader='''
                #version 330

                in vec2 v_text;

                out vec4 outColor;
                uniform sampler2D Texture;

                void main() {

                    outColor = texture(Texture, v_text, 0.0);

                }
                
            '''
        )

        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330
                in vec2 vert;
                uniform float histogram[256];

                void main() {

                    if ((gl_VertexID % 2) == 0) {
                        gl_Position = vec4(vert.x, histogram[gl_VertexID/2]-0.7, 0.0, 1.0);
                        
                    }
                    else {
                        gl_Position = vec4(vert, 0.0, 1.0);
                    }

                    
                }
            ''',
            geometry_shader="""
            #version 330

            uniform vec2 resolution;
            uniform float width;

            layout(lines) in;
            layout(triangle_strip, max_vertices=4) out;

            void main() {
                vec2 p1 = gl_in[0].gl_Position.xy;
                vec2 p2 = gl_in[1].gl_Position.xy;
                vec2 dir = p2 - p1;
                vec2 normal = vec2(dir.y, -dir.x);
                vec2 step = normalize(normal) / resolution * width;

                gl_Position = vec4(p2 - step, 0, 1);
                EmitVertex();

                gl_Position = vec4(p1 - step, 0, 1);
                EmitVertex();

                gl_Position = vec4(p2 + step, 0, 1);
                EmitVertex();

                gl_Position = vec4(p1 + step, 0, 1);
                EmitVertex();

                EndPrimitive();
            }
            """,
            fragment_shader='''
                #version 330

                uniform vec2 resolution;

                out vec4 outColor;
                void main() {

                    vec2 coord = (gl_FragCoord.xy/resolution)-0.1;
                    outColor = vec4(coord.y,coord.y,1.0,1.0); 
                }
            ''',
        )

        self.histo = self.prog['histogram']
        self.prog2['Texture'] = 0

        self.histo.value = self.countPix('data/pic10.png')
        self.texture = self.load_texture_2d('pic10.png')

        vertices = np.array([
            1.0, 1.0,
            0.5, 1.0,
            0.5, 0.5,
            1.0, 0.5,
        ], dtype='f4')

        self.vbo2 = self.ctx.buffer(vertices)
        self.vao2 = self.ctx.simple_vertex_array(self.prog2, self.vbo2, 'vert')

        self.vbo = self.ctx.buffer(self.initLines().astype('f4'))
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'vert')


    def render(self, time: float, frame_time: float):
        self.texture.use(0)

        self.prog["resolution"] = self.wnd.buffer_size
        self.prog["width"] = 3.0
        back = (0.2, 0.2, 0.2)
        self.ctx.clear(back[0],back[1],back[2])
        self.vao.render(mode=moderngl.LINES)

        self.vao2.render(mode=moderngl.TRIANGLE_FAN)

        self.render_ui()

    def initLines(self):
        u = np.linspace(-0.8, 0.8, 256)
        u = np.array(list(zip(u,u))).flatten()
        v_down = np.repeat(-0.8,256)
        v_up = np.repeat(-0.7,256)

        v = np.array(list(zip(v_down,v_up))).flatten()

        return np.array(list(zip(u,v))).flatten()
       

    def countPix(self,path):
        hist = np.zeros(256)
        im = Image.open(path)
        pix = im.load()
        print(im.size)
        for x in range(im.size[0]):
            for y in range(im.size[1]):
                index = int((pix[x,y][0]+pix[x,y][1]+pix[x,y][2])/3)
                hist[index] += 1

        
        max = np.max(hist)
        hist = hist * (1/max)
        return hist.tolist()


    def render_ui(self):
        imgui.new_frame()

        imgui.begin("Description - Histogram", False)
        imgui.text("Shows the histogram of a selected photo")
        imgui.end()


        imgui.begin("Controls - Histogram", False)
        imgui.text("Press P to select a photo")
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
        if key == self.wnd.keys.P and action == self.wnd.keys.ACTION_PRESS:
            # Show file dialog
            root = tk.Tk()
            root.withdraw()
            path = filedialog.askopenfilename(filetypes=[("Picture files", ".png .jpg .jpeg .bmp")])
            self.histo.value = self.countPix(path)

            self.texture = self.load_texture_2d('warn.png')
                    

if __name__ == '__main__':
    Histogram.run()


