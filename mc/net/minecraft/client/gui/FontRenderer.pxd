# cython: language_level=3

cimport cython

@cython.final
cdef class FontRenderer:

    cdef:
        int[256] __charWidth
        int[32] __colorCode
        int __fontTextureName
        int __textureWidth
        int __textureHeight
        int __glyphWidth
        int __glyphHeight

    cdef __renderString(self, str string, int x, int y, int color, bint darken=?)
