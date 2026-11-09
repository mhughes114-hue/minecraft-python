from mc.net.minecraft.client.model.ModelBiped import ModelBiped
from mc.net.minecraft.client.model.ModelRenderer import ModelRenderer


class ModelVillager(ModelBiped):

    def __init__(self):
        super().__init__(textureWidth=128, textureHeight=128)
        self.nose = ModelRenderer(104, 0, 128, 128)
        self.nose.addBox(-1.0, -1.0, -3.0, 2, 2, 4, 0.0)
        self.nose.setRotationPoint(0.0, -4.0, -4.0)
        self.robe = ModelRenderer(64, 32, 128, 128)
        self.robe.addBox(-4.5, -0.5, -2.5, 9, 13, 5, 0.0)
        self.sash = ModelRenderer(96, 52, 128, 128)
        self.sash.addBox(-4.5, 3.0, -2.5, 9, 2, 5, 0.0)

    def setRotationAngles(self, x, y, z, xRot, yRot, zRot):
        super().setRotationAngles(x, y, z, xRot, yRot, zRot)
        self.nose.rotateAngleX = self.bipedHead.rotateAngleX
        self.nose.rotateAngleY = self.bipedHead.rotateAngleY

    def render(self, x, y, z, xRot, yRot, zRot):
        super().render(x, y, z, xRot, yRot, zRot)
        self.robe.render(1.0)
        self.sash.render(1.0)
        self.nose.render(1.0)
