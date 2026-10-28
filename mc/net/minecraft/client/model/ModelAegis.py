from mc.net.minecraft.client.model.ModelBase import ModelBase
from mc.net.minecraft.client.model.ModelRenderer import ModelRenderer

import math

class ModelAegis(ModelBase):

    def __init__(self):
        self.head = ModelRenderer(0, 0)
        self.head.addBox(-3.5, -4.0, -3.0, 7, 7, 6, 0.0)
        self.head.setRotationPoint(0.0, 5.0, 0.0)
        self.crown = ModelRenderer(28, 0)
        self.crown.addBox(-2.0, -7.0, -2.0, 4, 3, 4, 0.0)
        self.crown.setRotationPoint(0.0, 5.0, 0.0)
        self.body = ModelRenderer(0, 14)
        self.body.addBox(-4.0, -5.0, -2.5, 8, 10, 5, 0.0)
        self.body.setRotationPoint(0.0, 12.0, 0.0)
        self.leftWing = ModelRenderer(28, 12)
        self.leftWing.addBox(0.0, -4.0, -1.0, 3, 9, 2, 0.0)
        self.leftWing.setRotationPoint(4.0, 10.0, 0.0)
        self.rightWing = ModelRenderer(28, 12)
        self.rightWing.mirror = True
        self.rightWing.addBox(-3.0, -4.0, -1.0, 3, 9, 2, 0.0)
        self.rightWing.setRotationPoint(-4.0, 10.0, 0.0)
        self.leftLeg = ModelRenderer(0, 0)
        self.leftLeg.addBox(-1.5, 0.0, -1.5, 3, 6, 3, 0.0)
        self.leftLeg.setRotationPoint(2.0, 18.0, 0.0)
        self.rightLeg = ModelRenderer(0, 0)
        self.rightLeg.mirror = True
        self.rightLeg.addBox(-1.5, 0.0, -1.5, 3, 6, 3, 0.0)
        self.rightLeg.setRotationPoint(-2.0, 18.0, 0.0)
        self.parts = (self.head, self.crown, self.body, self.leftWing,
                      self.rightWing, self.leftLeg, self.rightLeg)

    def render(self, x, y, z, xRot, yRot, zRot):
        self.setRotationAngles(x, y, z, xRot, yRot, zRot)
        for part in self.parts:
            part.render(1.0)

    def setRotationAngles(self, x, y, z, xRot, yRot, zRot):
        self.head.rotateAngleY = xRot / (180.0 / math.pi)
        self.head.rotateAngleX = yRot / (180.0 / math.pi)
        self.crown.rotateAngleY = self.head.rotateAngleY
        self.crown.rotateAngleX = self.head.rotateAngleX
        self.leftLeg.rotateAngleX = math.cos(x * 0.6662) * 1.2 * y
        self.rightLeg.rotateAngleX = math.cos(x * 0.6662 + math.pi) * 1.2 * y
        flap = math.sin(z * 0.12) * 0.12
        self.leftWing.rotateAngleZ = flap
        self.rightWing.rotateAngleZ = flap
