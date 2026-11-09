from mc.net.minecraft.client.model.ModelBase import ModelBase
from mc.net.minecraft.client.model.ModelRenderer import ModelRenderer


class ModelTank(ModelBase):

    def __init__(self):
        self.hull = ModelRenderer(0, 0, 128, 128)
        self.hull.addBox(-8.0, -4.0, -10.0, 16, 7, 20, 0.0)
        self.turret = ModelRenderer(0, 32, 128, 128)
        self.turret.addBox(-5.0, -7.0, -5.0, 10, 4, 10, 0.0)
        self.cannon = ModelRenderer(48, 32, 128, 128)
        self.cannon.addBox(-1.0, -6.0, -15.0, 2, 2, 10, 0.0)
        self.leftTrack = ModelRenderer(0, 52, 128, 128)
        self.leftTrack.addBox(-10.0, -2.0, -9.0, 3, 6, 18, 0.0)
        self.rightTrack = ModelRenderer(44, 52, 128, 128)
        self.rightTrack.addBox(7.0, -2.0, -9.0, 3, 6, 18, 0.0)

    def render(self, x, y, z, xRot, yRot, zRot):
        self.hull.render(1.0)
        self.turret.render(1.0)
        self.cannon.render(1.0)
        self.leftTrack.render(1.0)
        self.rightTrack.render(1.0)
