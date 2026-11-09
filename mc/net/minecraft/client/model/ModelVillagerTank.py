from mc.net.minecraft.client.model.ModelTank import ModelTank
from mc.net.minecraft.client.model.ModelRenderer import ModelRenderer


class ModelVillagerTank(ModelTank):

    def __init__(self):
        super().__init__()
        self.leftCargo = ModelRenderer(88, 32, 128, 128)
        self.leftCargo.addBox(-8.0, -5.0, 2.0, 4, 4, 5, 0.0)
        self.rightCargo = ModelRenderer(108, 32, 128, 128)
        self.rightCargo.addBox(4.0, -5.0, 2.0, 4, 4, 5, 0.0)

    def render(self, x, y, z, xRot, yRot, zRot):
        super().render(x, y, z, xRot, yRot, zRot)
        self.leftCargo.render(1.0)
        self.rightCargo.render(1.0)
