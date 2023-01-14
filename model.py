import numpy as np
import glm

class Cube:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program('default')
        self.vao = self.get_vao()
        self.m_model = self.get_model_matrix()
        self.on_init()

    def on_init(self):
        self.shader_program['m_proj'].write(self.app.camera.m_proj)
        self.shader_program['m_view'].write(self.app.camera.m_view)
        self.shader_program['m_model'].write(self.m_model)

    def get_model_matrix(self):
        m_model = glm.mat4() 
        return m_model
    
    def update(self):
        m_model = glm.rotate(self.m_model, self.app.time, glm.vec3(0, 1, 0))
        self.shader_program['m_model'].write(m_model)

    def render(self):
        self.update()
        self.vao.render()
    
    def destroy(self):
        """
        There is no garbage colector in GL
        """
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vao(self):
        """
        Vertex array object = vbo + shader_program -> VAO
        '3f' - Buffer foramt = 3 float values 
        'in_position' - Attributes = 3f that are 'in_position' atributes
        """
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '3f', 'in_position')])
        return vao

    def get_vertex_data(self):
        """
        'vertices' - points of a cube
        'indices' - triangles/vertices that make a cube
        Note - OpenGL use counter clock vise selection to describe vertices
        """
        vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1), 
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)] 
                    
        indices = [(0, 2, 3), (0, 1, 2), (1, 7, 2), (1, 6, 7), (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0), (3, 7, 4), (3, 2, 7), (0, 6, 1), (0, 5, 6)] 
        vertex_data = self.get_data(vertices, indices)
        return vertex_data 
    
    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in  triangle]
        return np.array(data, dtype='f4')

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data) # vertex buffer object 
        return vbo

    def get_shader_program(self, shader_name):
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program


class Triangle:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program('default')
        self.vao = self.get_vao()

    def render(self):
        self.vao.render()
    
    def destroy(self):
        """
        There is no garbage colector in GL
        """
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vao(self):
        """
        Vertex array object = vbo + shader_program -> VAO
        '3f' - Buffer foramt = 3 float values 
        'in_position' - Attributes = 3f that are 'in_position' atributes
        """
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, '3f', 'in_position')])
        return vao

    def get_vertex_data(self):
        vertex_data = [(-0.6, -0.8, 0.0), (0.6, -0.8, 0.0), (0.0, 0.8, 0.0)]
        vertex_data = np.array(vertex_data, dtype='f4') # f4 = np.float32
        return vertex_data

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data) # vertex buffer object 
        return vbo

    def get_shader_program(self, shader_name):
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program

    
