from mc.net.minecraft.client.model.ModelBase import ModelBase
from mc.net.minecraft.client.model.ModelRenderer import ModelRenderer

import math

class ModelVentoraptor(ModelBase):

    def __init__(self):
        self.head = ModelRenderer(0, 0)
        self.head.addBox(-3.0, -3.0, -3.0, 6, 6, 6, 0.0)
        self.head.setRotationPoint(0.0, 5.0, -1.0)
        self.beak = ModelRenderer(24, 0)
        self.beak.addBox(-2.0, -1.5, -6.0, 4, 3, 5, 0.0)
        self.beak.setRotationPoint(0.0, 6.0, -1.0)
        self.body = ModelRenderer(0, 14)
        self.body.addBox(-4.0, -5.0, -3.0, 8, 11, 6, 0.0)
        self.body.setRotationPoint(0.0, 12.0, 1.0)
        self.leftWing = ModelRenderer(32, 12)
        self.leftWing.addBox(0.0, -1.0, -1.0, 7, 2, 3, 0.0)
        self.leftWing.setRotationPoint(3.0, 9.0, 0.0)
        self.rightWing = ModelRenderer(32, 12)
        self.rightWing.mirror = True
        self.rightWing.addBox(-7.0, -1.0, -1.0, 7, 2, 3, 0.0)
        self.rightWing.setRotationPoint(-3.0, 9.0, 0.0)
        self.leftLeg = ModelRenderer(40, 0)
        self.leftLeg.addBox(-1.5, 0.0, -2.0, 3, 7, 4, 0.0)
        self.leftLeg.setRotationPoint(2.0, 17.0, 0.0)
        self.rightLeg = ModelRenderer(40, 0)
        self.rightLeg.mirror = True
        self.rightLeg.addBox(-1.5, 0.0, -2.0, 3, 7, 4, 0.0)
        self.rightLeg.setRotationPoint(-2.0, 17.0, 0.0)
        self.tail = ModelRenderer(32, 0)
        self.tail.addBox(-1.0, -1.0, 0.0, 2, 2, 10, 0.0)
        self.tail.setRotationPoint(0.0, 12.0, 3.0)
        self.parts = (self.head, self.beak, self.body, self.leftWing,
                      self.rightWing, self.leftLeg, self.rightLeg, self.tail)

    def render(self, x, y, z, xRot, yRot, zRot):
        self.setRotationAngles(x, y, z, xRot, yRot, zRot)
        for part in self.parts:
            part.render(1.0)

    def setRotationAngles(self, x, y, z, xRot, yRot, zRot):
        headYaw = xRot / (180.0 / math.pi)
        headPitch = yRot / (180.0 / math.pi)
        self.head.rotateAngleY = headYaw
        self.head.rotateAngleX = headPitch
        self.beak.rotateAngleY = headYaw
        self.beak.rotateAngleX = headPitch
        self.leftLeg.rotateAngleX = math.cos(x * 0.6662) * 1.3 * y
        self.rightLeg.rotateAngleX = math.cos(x * 0.6662 + math.pi) * 1.3 * y
        flap = math.sin(z * 0.35) * 0.2
        self.leftWing.rotateAngleZ = flap
        self.rightWing.rotateAngleZ = flap
        self.tail.rotateAngleX = 0.25 + math.sin(z * 0.08) * 0.08
