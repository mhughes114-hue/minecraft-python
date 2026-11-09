class TexturedQuad:

    def __init__(self, vertices, u0=None, v0=None, u1=None, v1=None,
                 textureWidth=64, textureHeight=32):
        self.vertexPositions = vertices
        if isinstance(u0, int):
            insetU = 0.1 / textureWidth
            insetV = 0.1 / textureHeight
            vertices[0] = vertices[0].setTexturePosition(u1 / textureWidth - insetU,
                                                         v0 / textureHeight + insetV)
            vertices[1] = vertices[1].setTexturePosition(u0 / textureWidth + insetU,
                                                         v0 / textureHeight + insetV)
            vertices[2] = vertices[2].setTexturePosition(u0 / textureWidth + insetU,
                                                         v1 / textureHeight - insetV)
            vertices[3] = vertices[3].setTexturePosition(u1 / textureWidth - insetU,
                                                         v1 / textureHeight - insetV)
