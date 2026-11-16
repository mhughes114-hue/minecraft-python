from mc.net.minecraft.client.model.ModelTank import ModelTank
from mc.net.minecraft.client.model.ModelRenderer import ModelRenderer


class ModelMLRS(ModelTank):

    def __init__(self):
        super().__init__()
        self.turret = ModelRenderer(0, 32, 128, 128)
        self.turret.addBox(-5.0, -8.0, -5.0, 10, 7, 11, 0.0)
        self.leftPod = ModelRenderer(64, 32, 128, 128)
        self.leftPod.addBox(-8.0, -10.0, -4.0, 4, 5, 9, 0.0)
        self.rightPod = ModelRenderer(88, 32, 128, 128)
        self.rightPod.addBox(4.0, -10.0, -4.0, 4, 5, 9, 0.0)

    def render(self, x, y, z, xRot, yRot, zRot):
        self.hull.render(1.0)
        self.turret.render(1.0)
        self.leftPod.render(1.0)
        self.rightPod.render(1.0)
        self.leftTrack.render(1.0)
        self.rightTrack.render(1.0)
