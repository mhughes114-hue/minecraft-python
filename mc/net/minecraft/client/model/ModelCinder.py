from mc.net.minecraft.client.model.ModelBase import ModelBase
from mc.net.minecraft.client.model.ModelRenderer import ModelRenderer

import math

class ModelCinder(ModelBase):

    def __init__(self):
        self.head = ModelRenderer(0, 0)
        self.head.addBox(-3.0, -3.0, -5.0, 6, 6, 6, 0.0)
        self.head.setRotationPoint(0.0, 10.0, -5.0)
        self.body = ModelRenderer(0, 14)
        self.body.addBox(-4.0, -4.0, -6.0, 8, 8, 12, 0.0)
        self.body.setRotationPoint(0.0, 13.0, 2.0)
        self.crest = ModelRenderer(28, 0)
        self.crest.addBox(-1.0, -5.0, -1.0, 2, 5, 2, 0.0)
        self.crest.setRotationPoint(0.0, 7.0, -4.0)
        self.frontLeftLeg = ModelRenderer(32, 14)
        self.frontLeftLeg.addBox(-1.5, 0.0, -1.5, 3, 6, 3, 0.0)
        self.frontLeftLeg.setRotationPoint(2.5, 17.0, -2.0)
        self.frontRightLeg = ModelRenderer(32, 14)
        self.frontRightLeg.mirror = True
        self.frontRightLeg.addBox(-1.5, 0.0, -1.5, 3, 6, 3, 0.0)
        self.frontRightLeg.setRotationPoint(-2.5, 17.0, -2.0)
        self.backLeftLeg = ModelRenderer(32, 14)
        self.backLeftLeg.addBox(-1.5, 0.0, -1.5, 3, 6, 3, 0.0)
        self.backLeftLeg.setRotationPoint(2.5, 17.0, 6.0)
        self.backRightLeg = ModelRenderer(32, 14)
        self.backRightLeg.mirror = True
        self.backRightLeg.addBox(-1.5, 0.0, -1.5, 3, 6, 3, 0.0)
        self.backRightLeg.setRotationPoint(-2.5, 17.0, 6.0)
        self.tail = ModelRenderer(44, 0)
        self.tail.addBox(-1.0, -1.0, 0.0, 2, 2, 7, 0.0)
        self.tail.setRotationPoint(0.0, 12.0, 7.0)
        self.parts = (self.head, self.body, self.crest, self.frontLeftLeg,
                      self.frontRightLeg, self.backLeftLeg, self.backRightLeg,
                      self.tail)

    def render(self, x, y, z, xRot, yRot, zRot):
        self.setRotationAngles(x, y, z, xRot, yRot, zRot)
        for part in self.parts:
            part.render(1.0)

    def setRotationAngles(self, x, y, z, xRot, yRot, zRot):
        self.head.rotateAngleY = xRot / (180.0 / math.pi)
        self.head.rotateAngleX = yRot / (180.0 / math.pi)
        self.crest.rotateAngleZ = math.sin(z * 0.2) * 0.18
        self.frontLeftLeg.rotateAngleX = math.cos(x * 0.6662) * 1.1 * y
        self.backRightLeg.rotateAngleX = self.frontLeftLeg.rotateAngleX
        self.frontRightLeg.rotateAngleX = math.cos(x * 0.6662 + math.pi) * 1.1 * y
        self.backLeftLeg.rotateAngleX = self.frontRightLeg.rotateAngleX
        self.tail.rotateAngleX = 0.2 + math.sin(z * 0.08) * 0.08
