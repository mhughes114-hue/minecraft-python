from mc.net.minecraft.client.model.ModelBase import ModelBase
from mc.net.minecraft.client.model.ModelRenderer import ModelRenderer

import math


class ModelWitherStorm(ModelBase):

    def __init__(self):
        self.core = ModelRenderer(0, 0)
        self.core.addBox(-8.0, -5.0, -6.0, 16, 10, 12, 0.0)
        self.core.setRotationPoint(0.0, 13.0, 0.0)

        self.frontHead = ModelRenderer(0, 0)
        self.frontHead.addBox(-4.0, -4.0, -4.0, 8, 8, 8, 0.0)
        self.frontHead.setRotationPoint(0.0, 5.0, -8.0)

        self.leftHead = ModelRenderer(32, 0)
        self.leftHead.addBox(-3.5, -3.5, -3.5, 7, 7, 7, 0.0)
        self.leftHead.setRotationPoint(-10.0, 8.0, -2.0)

        self.rightHead = ModelRenderer(32, 0)
        self.rightHead.addBox(-3.5, -3.5, -3.5, 7, 7, 7, 0.0)
        self.rightHead.setRotationPoint(10.0, 8.0, -2.0)

        self.heart = ModelRenderer(32, 8)
        self.heart.addBox(-3.0, -3.0, -1.0, 6, 6, 2, 0.0)
        self.heart.setRotationPoint(0.0, 13.0, -6.5)

        self.tendrils = []
        for index, (x, z) in enumerate((
            (-7.0, -4.0), (7.0, -4.0), (-8.0, 4.0),
            (8.0, 4.0), (-3.0, 6.0), (3.0, 6.0)
        )):
            tendril = ModelRenderer(48, 0)
            tendril.addBox(-1.5, 0.0, -1.5, 3, 14, 3, 0.0)
            tendril.setRotationPoint(x, 15.0, z)
            self.tendrils.append(tendril)

        self.parts = (self.core, self.frontHead, self.leftHead,
                      self.rightHead, self.heart, *self.tendrils)

    def render(self, x, y, z, xRot, yRot, zRot):
        self.setRotationAngles(x, y, z, xRot, yRot, zRot)
        for part in self.parts:
            part.render(1.0)

    def setRotationAngles(self, x, y, z, xRot, yRot, zRot):
        yaw = xRot / (180.0 / math.pi)
        pitch = yRot / (180.0 / math.pi)

        self.core.rotateAngleY = math.sin(z * 0.025) * 0.04
        self.frontHead.rotateAngleY = yaw
        self.frontHead.rotateAngleX = pitch
        self.leftHead.rotateAngleY = yaw + math.sin(z * 0.035) * 0.16
        self.rightHead.rotateAngleY = yaw - math.sin(z * 0.035) * 0.16
        self.leftHead.rotateAngleX = pitch + math.sin(z * 0.04) * 0.08
        self.rightHead.rotateAngleX = pitch - math.sin(z * 0.04) * 0.08
        self.heart.rotateAngleZ = math.sin(z * 0.08) * 0.08

        for index, tendril in enumerate(self.tendrils):
            phase = z * 0.07 + index * 1.1
            tendril.rotateAngleX = math.sin(phase) * 0.18
            tendril.rotateAngleZ = math.cos(phase) * 0.24
