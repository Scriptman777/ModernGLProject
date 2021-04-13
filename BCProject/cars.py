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
                in vec3 in_normal;

                out vec3 v_vert;
                out vec3 v_norm;

                void main() {
                    gl_Position = Mvp * vec4(in_position, 1.0);
                    v_vert = in_position;
                    v_norm = in_normal;
                }
            ''',
            fragment_shader='''
                #version 330

                uniform vec3 Light;
                uniform float gradient;

                in vec3 v_vert;
                in vec3 v_norm;

                out vec4 f_color;

                void main() {
                    float lum = clamp(dot(normalize(Light - v_vert), normalize(v_norm)), 0.0, 1.0) * 0.8 + 0.2;
                    vec3 color = mix(vec3(1.0,0.0,0.0),vec3(0.0,1.0,0.0),gradient);
                    f_color = vec4(color.xyz * lum, 1.0);
                }
            ''',
        )

        self.prog_map = self.ctx.program(
            vertex_shader='''
                #version 330

                uniform mat4 Mvp;

                in vec3 vert;
                out vec2 v_text;

                void main() {
                    gl_Position = Mvp * vec4(vert, 1.0);
                    v_text = vec2(vert.x/400,vert.y/400);
                }
            ''',
            fragment_shader='''
                #version 330

                out vec4 outColor;

                in vec2 v_text;

                uniform sampler2D Texture;

                void main() {
                    outColor = texture(Texture, v_text, 0.0);
                }
            ''',
        )



        vertices = np.array([
            0.0, 0.0, 0.0,
            400.0, 0.0, 0.0,
            400.0, 400.0, 0.0,
            0.0, 400.0, 0.0,
        ], dtype='f4')

        self.prog_map['Texture'] = 0
        self.texture = self.load_texture_2d('EU.jpg')

        self.mvp = self.prog['Mvp']
        self.mvp_map = self.prog_map['Mvp']

        self.light = self.prog['Light']
        self.gradient = self.prog['gradient']

        self.gradient.value = 0

        self.vbo_map = self.ctx.buffer(vertices.astype('f4'))
        self.vao_map = self.ctx.simple_vertex_array(self.prog_map, self.vbo_map, 'vert')

        self.obj = self.load_scene('car2.obj')

        self.vao = self.obj.root_nodes[0].mesh.vao.instance(self.prog)

        self.movX = 200
        self.movY = -200
        self.movZ = 300

        self.positions = np.array([
            [195,105,0],
            [160,135,0],
            [250,260,0],
            [150,100,0],
            [185,135,0],
            [200,60,0],
            [165,150,0],
            [105,45,0],
            [130,50,0],
            [205,260,0],
            [135,155,0],
            [205,125,0],
            [225,100,0],
            [225,150,0],
            [250,90,0],
            [220,118,0],
            [202,92,0],
            [220,80,0],
            [280,120,0],
            [300,190,0],])


    def render(self, time, frame_time):
        self.ctx.clear(0.2, 0.2, 0.2)
        self.ctx.enable(moderngl.DEPTH_TEST)

        proj = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 1000.0)
        lookat = Matrix44.look_at(
            (self.movX, self.movY, self.movZ),
            (200.0, 200.0, 0.0),
            (0.0, 0.0, 1.0),
        )

        self.light.value = (self.movX, self.movY, self.movZ)

        self.texture.use(0)
        self.mvp_map.write((proj * lookat).astype('f4'))
        self.vao_map.render(moderngl.TRIANGLE_FAN)

        model_rot = Matrix44.from_z_rotation(3.14/4) 

        for x in range(int(self.positions.size/3)):
            #model_size = Matrix44.from_scale(np.array([2,2,2]))
            model = Matrix44.from_translation(np.array(self.positions[x])) *  model_rot
            self.mvp.write((proj * lookat * model).astype('f4'))
            self.vao.render()
      

    def key_event(self, key, action, modifiers):
        if key == self.wnd.keys.RIGHT and action == self.wnd.keys.ACTION_PRESS:
            self.movX += 10
        if key == self.wnd.keys.LEFT and action == self.wnd.keys.ACTION_PRESS:
            self.movX -= 10
        if key == self.wnd.keys.UP and action == self.wnd.keys.ACTION_PRESS:
            self.movY += 10
        if key == self.wnd.keys.DOWN and action == self.wnd.keys.ACTION_PRESS:
            self.movY -= 10
        if key == self.wnd.keys.W and action == self.wnd.keys.ACTION_PRESS:
            self.movZ += 10
        if key == self.wnd.keys.S and action == self.wnd.keys.ACTION_PRESS:
            self.movZ -= 10
        if key == self.wnd.keys.A and action == self.wnd.keys.ACTION_PRESS:
            self.gradient.value += 0.1
        if key == self.wnd.keys.D and action == self.wnd.keys.ACTION_PRESS:
            self.gradient.value -= 0.1

        


if __name__ == '__main__':
    Cars.run()
