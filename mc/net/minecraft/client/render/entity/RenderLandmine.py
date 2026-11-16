from mc.net.minecraft.client.render.RenderBlocks import RenderBlocks
from mc.net.minecraft.client.render.entity.Render import Render
from mc.net.minecraft.game.level.block.Blocks import blocks
from pyglet import gl


class RenderLandmine(Render):
    blockRenderer = RenderBlocks()

    def doRender(self, entity, xd, yd, zd, yaw, a):
        self._loadTexture('terrain.png')
        gl.glPushMatrix()
        gl.glTranslatef(xd, yd - 0.08, zd)
        gl.glScalef(0.28, 0.12, 0.28)
        self.blockRenderer.renderBlockOnInventory(blocks.gravel)
        gl.glPopMatrix()
