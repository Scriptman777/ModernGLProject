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

        self.vbo_map = self.ctx.buffer(vertices.astype('f4'))
        self.vao_map = self.ctx.simple_vertex_array(self.prog_map, self.vbo_map, 'vert')

        self.obj = self.load_scene('car.obj')

        self.vao = self.obj.root_nodes[0].mesh.vao.instance(self.prog)

        self.movX = 0
        self.movY = 0


    def render(self, time, frame_time):
        self.ctx.clear(0.2, 0.2, 0.2)
        self.ctx.enable(moderngl.DEPTH_TEST)

        proj = Matrix44.perspective_projection(45.0, self.aspect_ratio, 0.1, 1000.0)
        lookat = Matrix44.look_at(
            (200, -200, 300),
            (200.0, 200.0, 0.0),
            (0.0, 0.0, 1.0),
        )


        self.texture.use(0)
        self.mvp_map.write((proj * lookat).astype('f4'))
        self.vao_map.render(moderngl.TRIANGLE_FAN)

        model_rot = Matrix44.from_z_rotation(3.14/4) 


        #Austria

        model = Matrix44.from_translation(np.array([195,105,0])) *  model_rot
        self.mvp.write((proj * lookat * model).astype('f4'))
        self.vao.render()

        #Belgium

        model = Matrix44.from_translation(np.array([160,135,0])) *  model_rot
        self.mvp.write((proj * lookat * model).astype('f4'))
        self.vao.render()

        #Finland

        model = Matrix44.from_translation(np.array([250,260,0])) *  model_rot
        self.mvp.write((proj * lookat * model).astype('f4'))
        self.vao.render()

        #France

        model = Matrix44.from_translation(np.array([150,100,0])) *  model_rot
        self.mvp.write((proj * lookat * model).astype('f4'))
        self.vao.render()

        #Germany

        model = Matrix44.from_translation(np.array([185,135,0])) *  model_rot
        self.mvp.write((proj * lookat * model).astype('f4'))
        self.vao.render()

        #Italy

        model = Matrix44.from_translation(np.array([200,60,0])) *  model_rot
        self.mvp.write((proj * lookat * model).astype('f4'))
        self.vao.render()

        #Netherlands

        model = Matrix44.from_translation(np.array([165,150,0])) *  model_rot
        self.mvp.write((proj * lookat * model).astype('f4'))
        self.vao.render()

        #Portugal

        model = Matrix44.from_translation(np.array([105,45,0])) *  model_rot
        self.mvp.write((proj * lookat * model).astype('f4'))
        self.vao.render()

        #Spain

        model = Matrix44.from_translation(np.array([130,50,0])) *  model_rot
        self.mvp.write((proj * lookat * model).astype('f4'))
        self.vao.render()

        #Sweden

        model = Matrix44.from_translation(np.array([205,260,0])) *  model_rot
        self.mvp.write((proj * lookat * model).astype('f4'))
        self.vao.render()

        #UK

        model = Matrix44.from_translation(np.array([135,155,0])) *  model_rot
        self.mvp.write((proj * lookat * model).astype('f4'))
        self.vao.render()

        #CZ

        model = Matrix44.from_translation(np.array([205,125,0])) *  model_rot
        self.mvp.write((proj * lookat * model).astype('f4'))
        self.vao.render()

        #Hungary

        model = Matrix44.from_translation(np.array([225,100,0])) *  model_rot
        self.mvp.write((proj * lookat * model).astype('f4'))
        self.vao.render()

        #Poland

        model = Matrix44.from_translation(np.array([225,150,0])) *  model_rot
        self.mvp.write((proj * lookat * model).astype('f4'))
        self.vao.render()

        #Romania

        model = Matrix44.from_translation(np.array([250,90,0])) *  model_rot
        self.mvp.write((proj * lookat * model).astype('f4'))
        self.vao.render()

        #Slovakia

        model = Matrix44.from_translation(np.array([220,118,0])) *  model_rot
        self.mvp.write((proj * lookat * model).astype('f4'))
        self.vao.render()

        #Slovenia

        model = Matrix44.from_translation(np.array([202,92,0])) *  model_rot
        self.mvp.write((proj * lookat * model).astype('f4'))
        self.vao.render()

        #Serbia

        model = Matrix44.from_translation(np.array([220,80,0])) *  model_rot
        self.mvp.write((proj * lookat * model).astype('f4'))
        self.vao.render()

        #Ukraine

        model = Matrix44.from_translation(np.array([280,120,0])) *  model_rot
        self.mvp.write((proj * lookat * model).astype('f4'))
        self.vao.render()

        #Russia

        model = Matrix44.from_translation(np.array([300,190,0])) *  model_rot
        self.mvp.write((proj * lookat * model).astype('f4'))
        self.vao.render()

        #AAA

        model = Matrix44.from_translation(np.array([self.movX,self.movY,0])) *  model_rot
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
        print("X: " + str(self.movX) + "Y: " + str(self.movY))

        


if __name__ == '__main__':
    Cars.run()
