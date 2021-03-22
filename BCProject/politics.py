import numpy as np
import moderngl
from window import Window

def grid(size, vert, steps, lines):
    u = np.linspace(-size, size, steps)
    v = np.repeat(vert,steps)

    for x in range(lines-1):
        u = np.append(u,u)
        v = np.append(v,np.repeat(vert-0.1,steps))
        vert = vert - 0.1
        

    out = np.array(list(zip(u,v))).flatten()

    return out

class Politics(Window):
    title = "Poslanecká sněmovna ČR"
    gl_version = (3, 3)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330

                in vec2 in_vert;

                uniform int inSeats[10];

                flat out int colIndex;

                int compare = inSeats[0];
                int selector = 0;


                void main() {
                    gl_Position = vec4(in_vert,0.0,1.0);
                    gl_PointSize = 20;
                    
                    if (gl_VertexID < inSeats[0]) {
                        colIndex = 0;
                    }
                    else if (gl_VertexID < inSeats[0]+inSeats[1]) {
                        colIndex = 1;
                    }
                    else if (gl_VertexID < inSeats[0]+inSeats[1]+inSeats[2]) {
                        colIndex = 2;
                    }
                    else if (gl_VertexID < inSeats[0]+inSeats[1]+inSeats[2]+inSeats[3]) {
                        colIndex = 3;
                    }
                    else if (gl_VertexID < inSeats[0]+inSeats[1]+inSeats[2]+inSeats[3]+inSeats[4]) {
                        colIndex = 4;
                    }
                    else if (gl_VertexID < inSeats[0]+inSeats[1]+inSeats[2]+inSeats[3]+inSeats[4]+inSeats[5]) {
                        colIndex = 5;
                    }
                    else if (gl_VertexID < inSeats[0]+inSeats[1]+inSeats[2]+inSeats[3]+inSeats[4]+inSeats[5]+inSeats[6]) {
                        colIndex = 6;
                    }
                    else if (gl_VertexID < inSeats[0]+inSeats[1]+inSeats[2]+inSeats[3]+inSeats[4]+inSeats[5]+inSeats[6]+inSeats[7]) {
                        colIndex = 7;
                    }
                    else if (gl_VertexID < inSeats[0]+inSeats[1]+inSeats[2]+inSeats[3]+inSeats[4]+inSeats[5]+inSeats[6]+inSeats[7]+inSeats[8]) {
                        colIndex = 8;
                    }
                    else if (gl_VertexID < inSeats[0]+inSeats[1]+inSeats[2]+inSeats[3]+inSeats[4]+inSeats[5]+inSeats[6]+inSeats[7]+inSeats[8]+inSeats[9]) {
                        colIndex = 9;
                    }
                }
            ''',
            fragment_shader='''
                #version 330

                flat in int colIndex;

                uniform vec3 back;

                out vec4 outColor;

                vec3 ano = vec3(0,255,251);
                vec3 ods = vec3(0,0,255);
                vec3 pir = vec3(0,0,0);
                vec3 spd = vec3(97,75,3);
                vec3 ksc = vec3(255,0,0);
                vec3 csd = vec3(255,166,0);
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

                
            '''
        )

        self.seats = self.prog['inSeats']
        self.back = self.prog['back']

        self.vbo = self.ctx.buffer(grid(0.5, 0.8, 20, 10).astype('f4'))
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, 'in_vert')


    def render(self, time: float, frame_time: float):
        self.seats.value = [78,23,22,19,15,14,10,7,6,6]
        self.ctx.enable_only(moderngl.PROGRAM_POINT_SIZE)
        back = (0.5, 0.5, 0.5)
        self.back.value = back
        self.ctx.clear(back[0],back[1],back[2])
        self.vao.render(mode=moderngl.POINTS)


if __name__ == '__main__':
    Politics.run()


