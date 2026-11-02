from mc.net.minecraft.client.model.ModelWitherStorm import ModelWitherStorm
from mc.net.minecraft.client.render.entity.RenderLiving import RenderLiving
from pyglet import gl


class RenderWitherStorm(RenderLiving):

    def __init__(self):
        super().__init__(ModelWitherStorm(), 4.0)

    def _preRenderCallback(self, entity, a):
        scale = 1.7 + entity.evolutionStage * 0.45
        gl.glScalef(scale, scale, scale)
