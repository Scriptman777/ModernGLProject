from pyrr import Matrix44
from UI.window import Window
import numpy as np

import moderngl


class Cars(Window):
    title = "Car production"
    gl_version = (3, 3)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330

                uniform mat4 Mvp;

                in vec3 in_position;


                void main() {
                    gl_Position = Mvp * vec4(in_position, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330

                in vec3 v_norm;
                in vec2 v_text;

                out vec4 f_color;

                void main() {

                    f_color = vec4(0.0,0.0,1.0, 1.0);
                }
            ''',
        )

        self.prog_map = self.ctx.program(
            vertex_shader='''
                #version 330

                uniform mat4 Mvp;

                in vec3 vert;

                void main() {
                    gl_Position = Mvp * vec4(vert, 1.0);
                }
            ''',
            fragment_shader='''
                #version 330

                out vec4 outColor;

                void main() {
                    outColor = vec4(1.0,0.0,0.0,1.0);
                }
            ''',
        )



        vertices = np.array([
            0.0, 0.0, 0.0,
            10.0, 0.0, 0.0,
            0.0, 10.0, 0.0,
        ], dtype='f4')

        self.mvp = self.prog['Mvp']
        self.mvp_map = self.prog_map['Mvp']

        self.vbo_map = self.ctx.buffer(vertices.astype('f4'))
        self.vao_map = self.ctx.simple_vertex_array(self.prog_map, self.vbo_map, 'vert')

        self.obj = self.load_scene('car.obj')

        self.vao = self.obj.root_nodes[0].mesh.vao.instance(self.prog)

    def render(self, time, frame_time):
        self.ctx.clear(0.2, 0.2, 0.2)
        self.ctx.enable(moderngl.DEPTH_TEST)

        proj = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 1000.0)
        lookat = Matrix44.look_at(
            (-150, -150, 150),
            (0.0, 0.0, 0.0),
            (0.0, 0.0, 1.0),
        )

        
        

        self.mvp.write((proj * lookat).astype('f4'))
        self.vao.render()


        self.mvp_map.write((proj * lookat).astype('f4'))
        self.vao_map.render(moderngl.TRIANGLES)

        model = Matrix44.from_translation(np.array([10,0,0]))

        self.mvp.write((proj * lookat * model).astype('f4'))
        self.vao.render()


        


if __name__ == '__main__':
    Cars.run()
