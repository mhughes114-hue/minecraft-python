from mc.net.minecraft.client.model.ModelBiped import ModelBiped
from mc.net.minecraft.client.model.ModelRenderer import ModelRenderer


class ModelPillager(ModelBiped):

    def __init__(self):
        super().__init__(textureWidth=128, textureHeight=128)
        self.hood = ModelRenderer(64, 0, 128, 128)
        self.hood.addBox(-4.5, -8.5, -4.5, 9, 9, 9, 0.0)
        self.nose = ModelRenderer(104, 0, 128, 128)
        self.nose.addBox(-1.0, -1.0, -3.0, 2, 2, 4, 0.0)
        self.nose.setRotationPoint(0.0, -4.0, -4.0)
        self.coat = ModelRenderer(64, 32, 128, 128)
        self.coat.addBox(-4.5, -0.5, -2.5, 9, 13, 5, 0.0)

    def setRotationAngles(self, x, y, z, xRot, yRot, zRot):
        super().setRotationAngles(x, y, z, xRot, yRot, zRot)
        self.hood.rotateAngleX = self.bipedHead.rotateAngleX
        self.hood.rotateAngleY = self.bipedHead.rotateAngleY
        self.nose.rotateAngleX = self.bipedHead.rotateAngleX
        self.nose.rotateAngleY = self.bipedHead.rotateAngleY

    def render(self, x, y, z, xRot, yRot, zRot):
        super().render(x, y, z, xRot, yRot, zRot)
        self.hood.render(1.0)
        self.coat.render(1.0)
        self.nose.render(1.0)
