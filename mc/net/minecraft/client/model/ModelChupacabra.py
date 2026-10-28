from mc.net.minecraft.client.model.ModelBase import ModelBase
from mc.net.minecraft.client.model.ModelRenderer import ModelRenderer

import math

class ModelChupacabra(ModelBase):

    def __init__(self):
        self.head = ModelRenderer(0, 0)
        self.head.addBox(-3.0, -3.0, -6.0, 6, 6, 7, 0.0)
        self.head.setRotationPoint(0.0, 12.0, -6.0)
        self.muzzle = ModelRenderer(28, 0)
        self.muzzle.addBox(-2.0, -1.5, -4.0, 4, 3, 4, 0.0)
        self.muzzle.setRotationPoint(0.0, 13.0, -8.0)
        self.body = ModelRenderer(0, 14)
        self.body.addBox(-4.0, -3.5, -7.0, 8, 7, 14, 0.0)
        self.body.setRotationPoint(0.0, 14.0, 1.0)
        self.leftEar = ModelRenderer(32, 8)
        self.leftEar.addBox(0.0, -5.0, -1.0, 2, 5, 2, 0.0)
        self.leftEar.setRotationPoint(2.0, 10.0, -7.0)
        self.rightEar = ModelRenderer(32, 8)
        self.rightEar.mirror = True
        self.rightEar.addBox(-2.0, -5.0, -1.0, 2, 5, 2, 0.0)
        self.rightEar.setRotationPoint(-2.0, 10.0, -7.0)
        self.frontLeftLeg = ModelRenderer(40, 0)
        self.frontLeftLeg.addBox(-1.5, 0.0, -1.5, 3, 6, 3, 0.0)
        self.frontLeftLeg.setRotationPoint(2.5, 17.0, -3.0)
        self.frontRightLeg = ModelRenderer(40, 0)
        self.frontRightLeg.mirror = True
        self.frontRightLeg.addBox(-1.5, 0.0, -1.5, 3, 6, 3, 0.0)
        self.frontRightLeg.setRotationPoint(-2.5, 17.0, -3.0)
        self.backLeftLeg = ModelRenderer(40, 0)
        self.backLeftLeg.addBox(-1.5, 0.0, -1.5, 3, 6, 3, 0.0)
        self.backLeftLeg.setRotationPoint(2.5, 17.0, 6.0)
        self.backRightLeg = ModelRenderer(40, 0)
        self.backRightLeg.mirror = True
        self.backRightLeg.addBox(-1.5, 0.0, -1.5, 3, 6, 3, 0.0)
        self.backRightLeg.setRotationPoint(-2.5, 17.0, 6.0)
        self.parts = (self.head, self.muzzle, self.body, self.leftEar,
                      self.rightEar, self.frontLeftLeg, self.frontRightLeg,
                      self.backLeftLeg, self.backRightLeg)

    def render(self, x, y, z, xRot, yRot, zRot):
        self.setRotationAngles(x, y, z, xRot, yRot, zRot)
        for part in self.parts:
            part.render(1.0)

    def setRotationAngles(self, x, y, z, xRot, yRot, zRot):
        headYaw = xRot / (180.0 / math.pi)
        headPitch = yRot / (180.0 / math.pi)
        self.head.rotateAngleY = headYaw
        self.head.rotateAngleX = headPitch
        self.muzzle.rotateAngleY = headYaw
        self.muzzle.rotateAngleX = headPitch
        self.frontLeftLeg.rotateAngleX = math.cos(x * 0.6662) * 1.2 * y
        self.backRightLeg.rotateAngleX = self.frontLeftLeg.rotateAngleX
        self.frontRightLeg.rotateAngleX = math.cos(x * 0.6662 + math.pi) * 1.2 * y
        self.backLeftLeg.rotateAngleX = self.frontRightLeg.rotateAngleX
