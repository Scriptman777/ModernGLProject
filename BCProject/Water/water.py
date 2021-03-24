import numpy as np
import moderngl
import imgui
from UI.window import Window
from moderngl_window.integrations.imgui import ModernglWindowRenderer

def gridInit(size, steps):
    #Vertical Lines
    u = np.linspace(-size, size, steps)
    u = np.array(list(zip(u,u))).flatten()

    v = np.repeat(size,steps)
    neg_v = np.repeat(-size,steps)
    v = np.array(list(zip(v,neg_v))).flatten()
       
    out = np.array(list(zip(u,v))).flatten()

    #Horizontal lines

    out = np.append(out,np.array(list(zip(v,u))).flatten())

    return out

class Water(Window):
    title = "Water"
    gl_version = (3, 3)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        imgui.create_context()
        self.imgui = ModernglWindowRenderer(self.wnd)

        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330

                in vec2 in_vert;


                void main() {
                    gl_Position = vec4(in_vert,0.0,1.0);

                }
            ''',
            fragment_shader='''
                #version 330

                out vec4 outColor;

                uniform bool graph;
                
                void main() {
                    if (graph) 
                    {
                        outColor = vec4(0.0,0.0,1.0,1.0);   
                    }
                    else
                    {
                        outColor = vec4(0.0,0.0,0.0,1.0);
                    }

                    
                }

                
            '''
        )

        vertices = np.array([
            0.0, 0.8, 
            0.0, -0.8, 
            0.4, 0.8,
            0.4, -0.8, 
        ], dtype='f4')

        self.graph = self.prog['graph']

        
        

        self.vbo_grid = self.ctx.buffer(gridInit(0.8,20).astype('f4'))
        self.vao_grid = self.ctx.simple_vertex_array(self.prog, self.vbo_grid, 'in_vert')

        self.vbo_graph = self.ctx.buffer(vertices)   
        self.vao_graph = self.ctx.simple_vertex_array(self.prog, self.vbo_graph, 'in_vert')

    def render(self, time: float, frame_time: float):


        back = (1.0, 1.0, 1.0)
        self.ctx.clear(back[0],back[1],back[2])
        self.graph.value = False
        self.vao_grid.render(moderngl.LINES)
        self.graph.value = True
        self.vao_graph.render(moderngl.TRIANGLES)

        self.render_ui()

    def render_ui(self):
        imgui.new_frame()


        imgui.begin("Description - Water levels", False)
        imgui.text("Štítarský potok")
        imgui.end()

        imgui.render()
        self.imgui.render(imgui.get_draw_data())

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




if __name__ == '__main__':
    Water.run()


