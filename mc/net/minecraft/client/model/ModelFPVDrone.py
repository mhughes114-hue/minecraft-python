from mc.net.minecraft.client.model.ModelBase import ModelBase
from mc.net.minecraft.client.model.ModelRenderer import ModelRenderer


class ModelFPVDrone(ModelBase):

    def __init__(self):
        self.body = ModelRenderer(0, 0, 128, 128)
        self.body.addBox(-3.0, -2.0, -3.0, 6, 3, 6, 0.0)
        self.frontArm = ModelRenderer(0, 16, 128, 128)
        self.frontArm.addBox(-12.0, -1.0, -1.0, 24, 2, 2, 0.0)
        self.sideArm = ModelRenderer(0, 24, 128, 128)
        self.sideArm.addBox(-1.0, -1.0, -12.0, 2, 2, 24, 0.0)
        self.rotors = []
        for x, z in ((-10.0, -10.0), (-10.0, 10.0),
                     (10.0, -10.0), (10.0, 10.0)):
            rotor = ModelRenderer(0, 32, 128, 128)
            rotor.addBox(x - 2.0, -1.0, z - 2.0, 4, 1, 4, 0.0)
            self.rotors.append(rotor)

    def render(self, x, y, z, xRot, yRot, zRot):
        self.body.render(1.0)
        self.frontArm.render(1.0)
        self.sideArm.render(1.0)
        for rotor in self.rotors:
            rotor.render(1.0)
