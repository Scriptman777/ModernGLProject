import numpy as np
import moderngl
import imgui
from UI.window import Window
from moderngl_window.integrations.imgui import ModernglWindowRenderer

def grid(size, vert, steps, lines, vertStep):
    u = np.linspace(-size, size, steps)
    v = np.repeat(vert,steps)

    for x in range(lines-1):
        u = np.append(u,u)
        v = np.append(v,np.repeat(vert-vertStep,steps))
        vert = vert - vertStep
       
    out = np.array(list(zip(u,v))).flatten()
    return out

def calculateCumulative(seats):
    cumulativeSeats = [seats[0]]
    temp = seats[0]
    for x in range(1,len(seats)):
        temp = temp + seats[x]
        cumulativeSeats.append(temp)
    return cumulativeSeats

class Politics(Window):
    title = "Mandates graph"
    gl_version = (3, 3)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        imgui.create_context()
        self.imgui = ModernglWindowRenderer(self.wnd)

        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330

                in vec2 in_vert;

                uniform int inSeats[10];
                uniform int size;

                flat out int colIndex;

                int compare = inSeats[0];
                int selector = 0;


                void main() {
                    gl_Position = vec4(in_vert,0.0,1.0);
                    gl_PointSize = size;
                    
                    if (gl_VertexID < inSeats[0]) {
                        colIndex = 0;
                    }
                    else if (gl_VertexID < inSeats[1]) {
                        colIndex = 1;
                    }
                    else if (gl_VertexID < inSeats[2]) {
                        colIndex = 2;
                    }
                    else if (gl_VertexID < inSeats[3]) {
                        colIndex = 3;
                    }
                    else if (gl_VertexID < inSeats[4]) {
                        colIndex = 4;
                    }
                    else if (gl_VertexID < inSeats[5]) {
                        colIndex = 5;
                    }
                    else if (gl_VertexID < inSeats[6]) {
                        colIndex = 6;
                    }
                    else if (gl_VertexID < inSeats[7]) {
                        colIndex = 7;
                    }
                    else if (gl_VertexID < inSeats[8]) {
                        colIndex = 8;
                    }
                    else if (gl_VertexID < inSeats[9]) {
                        colIndex = 9;
                    }
                }
            ''',
            fragment_shader='''
                #version 330

                flat in int colIndex;

                uniform vec3 back;
                uniform bool round;

                out vec4 outColor;

                vec3 ano = vec3(0,255,251);
                vec3 ods = vec3(0,0,255);
                vec3 pir = vec3(0,0,0);
                vec3 spd = vec3(97,75,3);
                vec3 ksc = vec3(255,0,0);
                vec3 csd = vec3(255,123,0);
                vec3 kdu = vec3(255,255,0);
                vec3 top = vec3(136,0,255);
                vec3 stn = vec3(0,158,18);
                vec3 nan = vec3(255,255,255);

                vec3 colors[10] = vec3[](ano,ods,pir,spd,ksc,csd,kdu,top,stn,nan);
                vec3 color;

                

                void main() {
                    
                    color = colors[colIndex];
                    float r = color.x / 255;
                    float g = color.y / 255;
                    float b = color.z / 255;


                    vec3 normColor = vec3(r,g,b);

                    if (round)
                    {
                        float dist = step(length(gl_PointCoord.xy - vec2(0.5)), 0.5);
                        if (dist == 0.0) 
                        {
                            outColor = vec4(back ,1.0);
                        }
                        else 
                        {
                            outColor = vec4(dist * normColor, dist);
                        }
                    }
                    else 
                    {
                        outColor = vec4(normColor,1.0);
                    }

                    
                }

                
            '''
        )

        self.seats = self.prog['inSeats']
        self.back = self.prog['back']
        self.size = self.prog['size']
        self.round = self.prog['round']



        self.round.value = True
        self.size.value = 20

        self.gridx = 0.5
        self.gridy = 0.1


        self.seats.value = calculateCumulative([78,23,22,19,15,14,10,7,6,6])

        self.states = {
            self.wnd.keys.UP: False,   
            self.wnd.keys.DOWN: False,  
            self.wnd.keys.W: False,   
            self.wnd.keys.S: False,  
            self.wnd.keys.A: False,   
            self.wnd.keys.D: False,  
        }

    def changeSize(self,bigger: bool):
        if (bigger):
            self.size.value = self.size.value + 1
        else:
            self.size.value = self.size.value - 1

    def changePointShape(self):
        self.round.value = not self.round.value



    def changeGrid(self,bigger: bool, horiz : bool):
        if (horiz):
            if (bigger):
                self.gridx = self.gridx + 0.01
            else:
                self.gridx = self.gridx - 0.01
        else:
            if (bigger):
                self.gridy = self.gridy + 0.001
            else:
                self.gridy = self.gridy - 0.001
            
    def control(self):
        if self.states.get(self.wnd.keys.UP):
            self.changeSize(True)
        if self.states.get(self.wnd.keys.DOWN):
            self.changeSize(False)
        if self.states.get(self.wnd.keys.W):
            self.changeGrid(bigger=True,horiz=False)
        if self.states.get(self.wnd.keys.S):
            self.changeGrid(bigger=False,horiz=False)
        if self.states.get(self.wnd.keys.A):
            self.changeGrid(bigger=True,horiz=True)
        if self.states.get(self.wnd.keys.D):
            self.changeGrid(bigger=False,horiz=True)

    def key_event(self, key, action, modifiers):
        if key not in self.states:
            if key == self.wnd.keys.P and action == self.wnd.keys.ACTION_PRESS:
                self.changePointShape()
            return

        if action == self.wnd.keys.ACTION_PRESS:
            self.states[key] = True
        else:
            self.states[key] = False



    def render(self, time: float, frame_time: float):

        self.fps = 1/frame_time

        self.control()

        self.vbo = self.ctx.buffer(grid(self.gridx, 0.8, 20, 10, self.gridy).astype('f4'))
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'in_vert')

        self.ctx.enable_only(moderngl.PROGRAM_POINT_SIZE)
        back = (0.2, 0.2, 0.2)
        self.back.value = back
        self.ctx.clear(back[0],back[1],back[2])
        self.vao.render(mode=moderngl.POINTS)

        self.render_ui()

    def render_ui(self):
        imgui.new_frame()


        imgui.begin("Description - Political parties", False)
        imgui.text("Visualisation of the number of mandates held by different political parties")
        imgui.text("FPS: %.2f" % self.fps)
        imgui.text("Parties:")
        imgui.text_colored("ANO", 0 ,1 ,251/ 255)
        imgui.text_colored("ODS", 0,0,1)
        imgui.text_colored("Pirate party", 0.5,0.5,0.5)
        imgui.text_colored("SPD", 97/ 255,75/ 255,3/ 255)
        imgui.text_colored("Communist party", 1,0,0)
        imgui.text_colored("CSSD", 1,123/ 255,0)
        imgui.text_colored("KDU-CLS", 1,1,0)
        imgui.text_colored("TOP 09", 136/ 255,0,1)
        imgui.text_colored("STAN", 0,158/ 255,18/ 255)
        imgui.text_colored("Other", 1,1,1)
        imgui.end()


        imgui.begin("Controls - Political parties", False)
        imgui.text("Press A/D to change size horizontaly")
        imgui.text("Press W/S to change size vertically")
        imgui.text("Press UP/DOWN to change size of the points")
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
    Politics.run()


