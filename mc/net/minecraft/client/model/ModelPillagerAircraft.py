from mc.net.minecraft.client.model.ModelAircraft import ModelAircraft
from mc.net.minecraft.client.model.ModelRenderer import ModelRenderer


class ModelPillagerAircraft(ModelAircraft):

    def __init__(self):
        super().__init__()
        self.canopy = ModelRenderer(50, 56, 128, 128)
        self.canopy.addBox(-2.0, -5.0, -5.0, 4, 3, 6, 0.0)
        self.leftGun = ModelRenderer(32, 56, 128, 128)
        self.leftGun.addBox(-10.0, 0.0, -4.0, 2, 2, 6, 0.0)
        self.rightGun = ModelRenderer(32, 56, 128, 128)
        self.rightGun.addBox(8.0, 0.0, -4.0, 2, 2, 6, 0.0)
        self.bomb = ModelRenderer(70, 56, 128, 128)
        self.bomb.addBox(-1.5, 1.0, 1.0, 3, 4, 5, 0.0)

    def render(self, x, y, z, xRot, yRot, zRot):
        super().render(x, y, z, xRot, yRot, zRot)
        self.canopy.render(1.0)
        self.leftGun.render(1.0)
        self.rightGun.render(1.0)
        self.bomb.render(1.0)
