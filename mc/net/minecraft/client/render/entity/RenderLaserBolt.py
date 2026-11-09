from mc.net.minecraft.client.render.entity.Render import Render
from pyglet import gl


class RenderLaserBolt(Render):

    def doRender(self, entity, xd, yd, zd, yaw, a):
        gl.glPushMatrix()
        gl.glDisable(gl.GL_TEXTURE_2D)
        gl.glDisable(gl.GL_LIGHTING)
        gl.glLineWidth(3.0)
        gl.glColor3f(*entity.laserColor)
        gl.glBegin(gl.GL_LINES)
        gl.glVertex3f(xd, yd, zd)
        gl.glVertex3f(
            xd + entity.motionX * 2.5,
            yd + entity.motionY * 2.5,
            zd + entity.motionZ * 2.5
        )
        gl.glEnd()
        gl.glLineWidth(1.0)
        gl.glColor3f(1.0, 1.0, 1.0)
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glPopMatrix()
