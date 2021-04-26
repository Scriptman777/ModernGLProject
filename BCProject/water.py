import numpy as np
import moderngl
import imgui
import math
from UI.window import Window
from moderngl_window.integrations.imgui import ModernglWindowRenderer

# PGRF2 - David Továrek 2021

def gridInit(size, steps_x, steps_y):
    #Vertical Lines
    u = np.linspace(-size, size, steps_x)
    u = np.array(list(zip(u,u))).flatten()

    v = np.repeat(size,steps_x)
    neg_v = np.repeat(-size,steps_x)
    v = np.array(list(zip(v,neg_v))).flatten()
       
    out = np.array(list(zip(u,v))).flatten()

    #Horizontal lines

    u_y = np.linspace(-size, size, steps_y)
    u_y = np.array(list(zip(u_y,u_y))).flatten()

    v_y = np.repeat(size,steps_y)
    neg_v_y = np.repeat(-size,steps_y)
    v_y = np.array(list(zip(v_y,neg_v_y))).flatten()

    out = np.append(out,np.array(list(zip(v_y,u_y))).flatten())

    return out

def dataInit(data):

    # Read only flow 
    heights = []
    for x in data:
        num = float(x[2].replace(",","."))
        heights.append(num)

    # Order chronologically
    heights.reverse()

    # Find maximum flow 
    max_flow = math.ceil(max(heights))

    norm_heights = []
    for x in heights:
        norm = round(x/max_flow,2)
        norm_heights.append(norm)

    # Create points for the graph
    step = 1.6/(len(heights)-1)
    out = np.empty(0)



    for x in range(len(heights)):
        out = np.append(out,np.array([round(-0.8+x*step,2),-0.8+norm_heights[x]]))
        out = np.append(out,np.array([round(-0.8+x*step,2),-0.8]))

    return out

def readData(path):
    # Read data from file
    f = open(path, "r")
    line = 0
    data = []
    for x in f:
      data.append(x.split("\t"))

    return data



class Water(Window):
    title = "Water flow graph"
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
                uniform bool opac;

                void main() {

                    float op = 1;

                    if (opac) 
                    {
                    op = 0.5;
                    }


                    if (graph) 
                    {
                        vec2 res = vec2(1280,720);
                        vec2 coord = (gl_FragCoord.xy/res)-0.1;
                        
                        outColor = vec4(coord.y,coord.y,1.0,op);   
                    }
                    else
                    {
                        outColor = vec4(0.0,0.0,0.0,1.0);
                    }

                    
                }

                
            '''
        )


        self.graph = self.prog['graph']
        self.opac = self.prog['opac']

        self.setData(3)

        self.opac.value = False
        

    def render(self, time: float, frame_time: float):

        self.fps = 1/frame_time

        back = (1.0, 1.0, 1.0)
        self.ctx.clear(back[0],back[1],back[2])

        self.graph.value = False
        self.vao_grid.render(moderngl.LINES)
        self.graph.value = True
        self.vao_graph.render(moderngl.TRIANGLE_STRIP)

        self.render_ui()



    def render_ui(self):

        imgui.new_frame()


        imgui.begin("Description - Water levels", False)
        imgui.text("This graph displays the streamflow of a river")
        imgui.text("in cubic meters per second")
        imgui.text("Source of data:")
        imgui.text("http://www.pla.cz/portal/sap/")
        imgui.text("FPS: %.2f" % self.fps)
        imgui.end()

        imgui.begin("Controls - Water levels", False)
        imgui.text("Press P to toggle opacity")
        imgui.text("Press 1,2,3,4 to change dataset")
        imgui.text(self.data_name)
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

    def key_event(self, key, action, modifiers):
        if key == self.wnd.keys.P and action == self.wnd.keys.ACTION_PRESS:
            self.toggleOpacity()
        if key == 49 and action == self.wnd.keys.ACTION_PRESS:
            self.setData(1)
        if key == 50 and action == self.wnd.keys.ACTION_PRESS:
            self.setData(2)
        if key == 51 and action == self.wnd.keys.ACTION_PRESS:
            self.setData(3)
        if key == 52 and action == self.wnd.keys.ACTION_PRESS:
            self.setData(4)

    def toggleOpacity(self):
        self.opac.value = not self.opac.value

    def setData(self,data_index):
        if data_index == 1:
            data = readData("data/Water_data.txt")
            self.initVertBuffers(data)
            self.data_name = "Cidlina"
        if data_index == 2:
            data = readData("data/Water_data2.txt")
            self.initVertBuffers(data)
            self.data_name = "Doubrava"
        if data_index == 3:
            data = readData("data/Water_data3.txt")
            self.initVertBuffers(data)
            self.data_name = "Metuje"
        if data_index == 4:
            data = readData("data/Water_data4.txt")
            self.initVertBuffers(data)
            self.data_name = "Ostravice"


    def initVertBuffers(self,data):
        self.vbo_grid = self.ctx.buffer(gridInit(0.8,len(data),20).astype('f4'))
        self.vao_grid = self.ctx.simple_vertex_array(self.prog, self.vbo_grid, 'in_vert')

        self.vbo_graph = self.ctx.buffer(dataInit(data).astype('f4'))
        self.vao_graph = self.ctx.simple_vertex_array(self.prog, self.vbo_graph, 'in_vert')



if __name__ == '__main__':
    Water.run()


