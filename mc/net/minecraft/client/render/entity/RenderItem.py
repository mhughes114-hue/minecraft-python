from mc.net.minecraft.client.render.Tessellator import tessellator
from mc.net.minecraft.client.render.entity.Render import Render
from mc.net.minecraft.client.render.RenderBlocks import RenderBlocks
from mc.net.minecraft.client.gui.Gui import Gui
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.JavaUtils import Random
from pyglet import gl

import math

class RenderItem(Render):

    def __init__(self):
        super().__init__()
        self.__renderBlocks = RenderBlocks()
        self.__random = Random()
        self._shadowSize = 0.15
        self._shadowOpaque = 12.0 / 16.0

    def renderItemIntoGUI(self, renderEngine, stack, width, height):
        if not stack:
            return

        if getattr(stack.getItem(), 'isSpawnEgg', False):
            self.__renderSpawnEggIcon(stack, width, height)
        elif stack.itemID < 256 and blocks.blocksList[stack.itemID].getRenderType() == 0:
            renderEngine.bindTexture(renderEngine.getTexture('terrain.png'))
            block = blocks.blocksList[stack.itemID]
            gl.glPushMatrix()
            gl.glTranslatef(width - 2, height + 3, 0.0)
            gl.glScalef(10.0, 10.0, 10.0)
            gl.glTranslatef(1.0, 0.5, 8.0)
            gl.glRotatef(210.0, 1.0, 0.0, 0.0)
            gl.glRotatef(45.0, 0.0, 1.0, 0.0)
            gl.glColor4f(1.0, 1.0, 1.0, 1.0)
            self.__renderBlocks.renderBlockOnInventory(block)
            gl.glPopMatrix()
        elif stack.getItem().getIconIndex() >= 0:
            gl.glDisable(gl.GL_LIGHTING)
            if stack.itemID < 256:
                renderEngine.bindTexture(renderEngine.getTexture('terrain.png'))
            else:
                renderEngine.bindTexture(renderEngine.getTexture('gui/items.png'))

            u = stack.getItem().getIconIndex() % 16 << 4
            v = stack.getItem().getIconIndex() // 16 << 4
            t = tessellator
            t.startDrawingQuads()
            t.addVertexWithUV(width, height + 16, 0.0, u * 0.00390625, (v + 16) * 0.00390625)
            t.addVertexWithUV(width + 16, height + 16, 0.0, (u + 16) * 0.00390625, (v + 16) * 0.00390625)
            t.addVertexWithUV(width + 16, height, 0.0, (u + 16) * 0.00390625, v * 0.00390625)
            t.addVertexWithUV(width, height, 0.0, u * 0.00390625, v * 0.00390625)
            t.draw()
            gl.glEnable(gl.GL_LIGHTING)

    def renderItemOverlayIntoGUI(self, fontRenderer, stack, width, height):
        if not stack:
            return

        if stack.stackSize > 1:
            size = str(stack.stackSize)
            gl.glDisable(gl.GL_LIGHTING)
            gl.glDisable(gl.GL_DEPTH_TEST)
            fontRenderer.drawStringWithShadow(
                size, width + 19 - 2 - fontRenderer.getStringWidth(size),
                height + 6 + 3, 16777215)
            gl.glEnable(gl.GL_LIGHTING)
            gl.glEnable(gl.GL_DEPTH_TEST)
        if stack.itemDamage > 0 and not getattr(stack.getItem(), 'isSpawnEgg', False):
            x = 13 - stack.itemDamage * 13 // stack.isItemStackDamageable()
            z1 = 255 - stack.itemDamage * 255 // stack.isItemStackDamageable()
            gl.glDisable(gl.GL_LIGHTING)
            gl.glDisable(gl.GL_DEPTH_TEST)
            gl.glDisable(gl.GL_TEXTURE_2D)
            t = tessellator
            z0 = 255 - z1 << 16 | z1 << 8
            z1 = (255 - z1) // 4 << 16 | 16128
            self.__renderQuad(t, width + 2, height + 13, 13, 2, 0)
            self.__renderQuad(t, width + 2, height + 13, 12, 1, z1)
            self.__renderQuad(t, width + 2, height + 13, x, 1, z0)
            gl.glEnable(gl.GL_LIGHTING)
            gl.glEnable(gl.GL_DEPTH_TEST)
            gl.glEnable(gl.GL_TEXTURE_2D)
            gl.glColor4f(1.0, 1.0, 1.0, 1.0)

    @staticmethod
    def __renderSpawnEggIcon(stack, x, y):
        base, spots = RenderItem.__getSpawnEggColors(stack)
        gl.glDisable(gl.GL_LIGHTING)
        Gui._drawRect(x + 6, y + 2, x + 10, y + 4, 0xFF171715)
        Gui._drawRect(x + 4, y + 4, x + 12, y + 6, 0xFF171715)
        Gui._drawRect(x + 3, y + 6, x + 13, y + 11, 0xFF171715)
        Gui._drawRect(x + 4, y + 11, x + 12, y + 14, 0xFF171715)
        Gui._drawRect(x + 6, y + 14, x + 10, y + 15, 0xFF171715)
        Gui._drawRect(x + 6, y + 3, x + 10, y + 5, base)
        Gui._drawRect(x + 5, y + 5, x + 11, y + 7, base)
        Gui._drawRect(x + 4, y + 7, x + 12, y + 11, base)
        Gui._drawRect(x + 5, y + 11, x + 11, y + 13, base)
        Gui._drawRect(x + 7, y + 13, x + 9, y + 14, base)
        Gui._drawRect(x + 6, y + 6, x + 8, y + 8, spots)
        Gui._drawRect(x + 9, y + 9, x + 11, y + 10, spots)
        Gui._drawRect(x + 6, y + 11, x + 8, y + 12, spots)
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        gl.glEnable(gl.GL_LIGHTING)

    @staticmethod
    def __getSpawnEggColors(stack):
        colors = (
            (0xFFEEE5CE, 0xFF8F5735),
            (0xFFF4F0E8, 0xFF817C72),
            (0xFFC9DFE5, 0xFF46728A),
            (0xFF6D9E38, 0xFF2E4C1D),
            (0xFFF2F0E8, 0xFF55534F),
            (0xFF4F4F4F, 0xFF91B53B),
            (0xFF554A3B, 0xFFB89965),
            (0xFFFFB348, 0xFF8C382B),
            (0xFF8E6346, 0xFFD8C19A),
            (0xFF78916B, 0xFF3B4D32),
        )
        return colors[stack.itemDamage % len(colors)]

    @staticmethod
    def __renderSpawnEggWorld(stack, t):
        base, spots = RenderItem.__getSpawnEggColors(stack)
        regions = (
            (6, 2, 10, 4, 0x171715),
            (4, 4, 12, 6, 0x171715),
            (3, 6, 13, 11, 0x171715),
            (4, 11, 12, 14, 0x171715),
            (6, 14, 10, 15, 0x171715),
            (6, 3, 10, 5, base),
            (5, 5, 11, 7, base),
            (4, 7, 12, 11, base),
            (5, 11, 11, 13, base),
            (7, 13, 9, 14, base),
            (6, 6, 8, 8, spots),
            (9, 9, 11, 10, spots),
            (6, 11, 8, 12, spots),
        )
        for left, top, right, bottom, color in regions:
            x0 = (left - 8.0) / 16.0
            x1 = (right - 8.0) / 16.0
            y0 = 0.75 - bottom / 16.0
            y1 = 0.75 - top / 16.0
            t.startDrawingQuads()
            t.setColorOpaque_I(color & 0xFFFFFF)
            t.addVertex(x0, y0, 0.0)
            t.addVertex(x1, y0, 0.0)
            t.addVertex(x1, y1, 0.0)
            t.addVertex(x0, y1, 0.0)
            t.draw()

    @staticmethod
    def __renderQuad(t, width, height, x, y, z):
        t.startDrawingQuads()
        t.setColorOpaque_I(z)
        t.addVertex(width, height, 0.0)
        t.addVertex(width, height + y, 0.0)
        t.addVertex(width + x, height + y, 0.0)
        t.addVertex(width + x, height, 0.0)
        t.draw()

    def doRender(self, entity, xd, yd, zd, yaw, a):
        self.__random.setSeed(187)
        item = entity.item
        gl.glPushMatrix()
        hoverY = math.sin((entity.age + a) / 10.0 + entity.hoverStart) * 0.1 + 0.1
        rot = ((entity.age + a) / 20.0 + entity.hoverStart) * (180.0 / math.pi)
        renders = 1
        if item.stackSize > 1:
            renders = 2
        if item.stackSize > 5:
            renders = 3
        if item.stackSize > 20:
            renders = 4

        gl.glTranslatef(xd, yd + hoverY, zd)
        gl.glEnable(gl.GL_NORMALIZE)
        if item.itemID < 256 and blocks.blocksList[item.itemID].getRenderType() == 0:
            gl.glRotatef(rot, 0.0, 1.0, 0.0)
            self._loadTexture('terrain.png')
            scale = 0.25
            if not blocks.blocksList[item.itemID].renderAsNormalBlock() and \
               item.itemID != blocks.stairSingle.blockID:
                scale = 0.5

            gl.glScalef(scale, scale, scale)

            for i in range(renders):
                gl.glPushMatrix()
                if i > 0:
                    x = (self.__random.nextFloat() * 2.0 - 1.0) * 0.2 / scale
                    y = (self.__random.nextFloat() * 2.0 - 1.0) * 0.2 / scale
                    z = (self.__random.nextFloat() * 2.0 - 1.0) * 0.2 / scale
                    gl.glTranslatef(x, y, z)

                self.__renderBlocks.renderBlockOnInventory(blocks.blocksList[item.itemID])
                gl.glPopMatrix()
        else:
            gl.glScalef(0.5, 0.5, 0.5)
            if getattr(item.getItem(), 'isSpawnEgg', False):
                gl.glDisable(gl.GL_TEXTURE_2D)
                gl.glDisable(gl.GL_LIGHTING)
                for i in range(renders):
                    gl.glPushMatrix()
                    if i > 0:
                        gl.glTranslatef(
                            (self.__random.nextFloat() * 2.0 - 1.0) * 0.3,
                            (self.__random.nextFloat() * 2.0 - 1.0) * 0.3,
                            (self.__random.nextFloat() * 2.0 - 1.0) * 0.3
                        )
                    gl.glRotatef(180.0 - self._renderManager.playerViewY,
                                 0.0, 1.0, 0.0)
                    self.__renderSpawnEggWorld(item, tessellator)
                    gl.glPopMatrix()
                gl.glEnable(gl.GL_LIGHTING)
                gl.glEnable(gl.GL_TEXTURE_2D)
                gl.glColor4f(1.0, 1.0, 1.0, 1.0)
            else:
                iconIndex = item.getItem().getIconIndex()
                if item.itemID < 256:
                    self._loadTexture('terrain.png')
                else:
                    self._loadTexture('gui/items.png')
                t = tessellator
                u0 = (iconIndex % 16 << 4) / 256.0
                u1 = ((iconIndex % 16 << 4) + 16) / 256.0
                v0 = (iconIndex // 16 << 4) / 256.0
                v1 = ((iconIndex // 16 << 4) + 16) / 256.0

                for i in range(renders):
                    gl.glPushMatrix()
                    if i > 0:
                        x = (self.__random.nextFloat() * 2.0 - 1.0) * 0.3
                        y = (self.__random.nextFloat() * 2.0 - 1.0) * 0.3
                        z = (self.__random.nextFloat() * 2.0 - 1.0) * 0.3
                        gl.glTranslatef(x, y, z)

                    gl.glRotatef(180.0 - self._renderManager.playerViewY, 0.0, 1.0, 0.0)
                    t.startDrawingQuads()
                    t.setNormal(0.0, 1.0, 0.0)
                    t.addVertexWithUV(-0.5, -0.25, 0.0, u0, v1)
                    t.addVertexWithUV(0.5, -0.25, 0.0, u1, v1)
                    t.addVertexWithUV(0.5, 12.0 / 16.0, 0.0, u1, v0)
                    t.addVertexWithUV(-0.5, 12.0 / 16.0, 0.0, u0, v0)
                    t.draw()
                    gl.glPopMatrix()

        gl.glDisable(gl.GL_NORMALIZE)
        gl.glPopMatrix()
