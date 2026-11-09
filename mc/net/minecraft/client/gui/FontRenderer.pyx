# cython: language_level=3

cimport cython

from mc.net.minecraft.client.render.Tessellator import tessellator
from mc import Resources
from pyglet import gl

@cython.final
cdef class FontRenderer:

    def __init__(self, settings, name, textures):
        cdef int i, glyph_x, glyph_y, x, y, pixel, alpha
        cdef int glyph_width, glyph_height
        cdef int color, col, r, g, b, ar

        texture = Resources.textures[name]
        self.__textureWidth = texture[0]
        self.__textureHeight = texture[1]
        glyph_width = self.__textureWidth // 16
        glyph_height = self.__textureHeight // 16
        if glyph_width <= 0 or glyph_height <= 0 or \
           self.__textureWidth % 16 or self.__textureHeight % 16:
            raise ValueError(f'Font texture {name} must contain a 16x16 glyph atlas')
        self.__glyphWidth = glyph_width
        self.__glyphHeight = glyph_height
        self.__fontTextureName = textures.getTexture(name)

        rawPixels = texture[2]

        for i in range(256):
            glyph_x = i % 16 * glyph_width
            glyph_y = i // 16 * glyph_height
            self.__charWidth[i] = 0
            for x in range(glyph_width):
                for y in range(glyph_height):
                    pixel = ((glyph_y + y) * self.__textureWidth + glyph_x + x) * 4
                    alpha = rawPixels[pixel + 3] & 255
                    if alpha > 128:
                        self.__charWidth[i] = x + 1

        self.__charWidth[32] = glyph_width // 2

        i = 0
        while i < 32:
            col = (i >> 3 & 1) * 85
            r = (i >> 2 & 1) * 170 + col
            g = (i >> 1 & 1) * 170 + col
            b = (i & 1) * 170 + col
            if i == 6:
                r += 85
            if settings.anaglyph:
                ar = (r * 30 + g * 59 + b * 11) // 100
                g = (r * 30 + g * 70) // 100
                b = (r * 30 + b * 70) // 100
                r = ar

            if i >= 16:
                r //= 4
                g //= 4
                b //= 4

            color = r << 16 | g << 8 | b
            self.__colorCode[i] = color
            i += 1

    def drawStringWithShadow(self, str string, int x, int y, int color):
        self.__renderString(string, x + 1, y + 1, color, True)
        self.drawString(string, x, y, color)

    def drawString(self, str string, int x, int y, int color):
        self.__renderString(string, x, y, color, False)

    cdef __renderString(self, str string, int x, int y, int color, bint darken=False):
        cdef int i, char_code, glyph_x, glyph_y, advance, draw_color
        cdef float u0, u1, v0, v1, left, top
        cdef int pen_x

        if string is None:
            return
        if not string:
            return

        if darken:
            color = (color & 0xFCFCFC) >> 2

        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__fontTextureName)
        draw_color = color
        pen_x = x
        t = tessellator
        t.startDrawingQuads()
        i = 0
        while i < len(string):
            if string[i] == '&' and i + 1 < len(string):
                code = string[i + 1].lower()
                if code in '0123456789abcdef':
                    color_index = '0123456789abcdef'.index(code)
                    draw_color = self.__colorCode[color_index]
                    if darken:
                        draw_color = (draw_color & 0xFCFCFC) >> 2
                    i += 2
                    continue

            char_code = ord(string[i])
            if char_code > 255:
                char_code = ord('?')
            advance = self.__charWidth[char_code]
            if advance > 0:
                glyph_x = char_code % 16 * self.__glyphWidth
                glyph_y = char_code // 16 * self.__glyphHeight
                u0 = glyph_x / self.__textureWidth
                u1 = (glyph_x + self.__glyphWidth - 0.01) / self.__textureWidth
                v0 = glyph_y / self.__textureHeight
                v1 = (glyph_y + self.__glyphHeight - 0.01) / self.__textureHeight
                left = pen_x
                top = y
                t.setColorOpaque_I(draw_color)
                t.addVertexWithUV(left, top + self.__glyphHeight - 0.01, 0.0, u0, v1)
                t.addVertexWithUV(left + self.__glyphWidth - 0.01,
                                  top + self.__glyphHeight - 0.01, 0.0, u1, v1)
                t.addVertexWithUV(left + self.__glyphWidth - 0.01, top, 0.0, u1, v0)
                t.addVertexWithUV(left, top, 0.0, u0, v0)

            pen_x += advance
            i += 1

        t.draw()

    def getStringWidth(self, str string):
        cdef int length, i, char_code

        if string is None:
            return 0
        else:
            length = 0
            i = 0
            while i < len(string):
                if string[i] == '&' and i + 1 < len(string) and \
                   string[i + 1].lower() in '0123456789abcdef':
                    i += 2
                    continue

                char_code = ord(string[i])
                if char_code > 255:
                    char_code = ord('?')
                length += self.__charWidth[char_code]
                i += 1

            return length
