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

        self.mvp = self.prog['Mvp']

        self.obj = self.load_scene('car.obj')

        self.vao = self.obj.root_nodes[0].mesh.vao.instance(self.prog)

    def render(self, time, frame_time):
        self.ctx.clear(1.0, 1.0, 1.0)
        self.ctx.enable(moderngl.DEPTH_TEST)

        proj = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 1000.0)
        lookat = Matrix44.look_at(
            (-85, -180, 140),
            (0.0, 0.0, 65.0),
            (0.0, 0.0, 1.0),
        )

        self.mvp.write((proj * lookat).astype('f4'))
        self.vao.render()

        model = Matrix44.from_translation(np.array([10,0,0]))

        self.mvp.write((proj * lookat * model).astype('f4'))
        self.vao.render()


if __name__ == '__main__':
    Cars.run()
