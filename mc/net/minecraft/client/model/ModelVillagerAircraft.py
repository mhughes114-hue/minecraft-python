from mc.net.minecraft.client.model.ModelAircraft import ModelAircraft
from mc.net.minecraft.client.model.ModelRenderer import ModelRenderer


class ModelVillagerAircraft(ModelAircraft):

    def __init__(self):
        super().__init__()
        self.canopy = ModelRenderer(32, 45, 128, 128)
        self.canopy.addBox(-2.0, -5.0, -5.0, 4, 3, 6, 0.0)
        self.leftEngine = ModelRenderer(54, 45, 128, 128)
        self.leftEngine.addBox(-9.0, -1.0, -3.0, 3, 3, 8, 0.0)
        self.rightEngine = ModelRenderer(78, 45, 128, 128)
        self.rightEngine.addBox(6.0, -1.0, -3.0, 3, 3, 8, 0.0)
        self.landingGear = ModelRenderer(102, 45, 128, 128)
        self.landingGear.addBox(-1.0, 2.0, -3.0, 2, 4, 2, 0.0)

    def render(self, x, y, z, xRot, yRot, zRot):
        super().render(x, y, z, xRot, yRot, zRot)
        self.canopy.render(1.0)
        self.leftEngine.render(1.0)
        self.rightEngine.render(1.0)
        self.landingGear.render(1.0)
