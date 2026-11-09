from mc.net.minecraft.client.model.ModelTank import ModelTank
from mc.net.minecraft.client.model.ModelRenderer import ModelRenderer


class ModelPillagerTank(ModelTank):

    def __init__(self):
        super().__init__()
        self.frontArmor = ModelRenderer(88, 48, 128, 128)
        self.frontArmor.addBox(-8.0, -3.0, -11.0, 16, 2, 4, 0.0)
        self.leftArmor = ModelRenderer(88, 60, 128, 128)
        self.leftArmor.addBox(-10.5, -2.0, -8.0, 3, 4, 8, 0.0)
        self.rightArmor = ModelRenderer(88, 60, 128, 128)
        self.rightArmor.addBox(7.5, -2.0, -8.0, 3, 4, 8, 0.0)

    def render(self, x, y, z, xRot, yRot, zRot):
        super().render(x, y, z, xRot, yRot, zRot)
        self.frontArmor.render(1.0)
        self.leftArmor.render(1.0)
        self.rightArmor.render(1.0)
