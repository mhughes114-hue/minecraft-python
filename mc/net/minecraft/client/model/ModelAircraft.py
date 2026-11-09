from mc.net.minecraft.client.model.ModelBase import ModelBase
from mc.net.minecraft.client.model.ModelRenderer import ModelRenderer


class ModelAircraft(ModelBase):

    def __init__(self):
        self.fuselage = ModelRenderer(0, 0, 128, 128)
        self.fuselage.addBox(-2.0, -3.0, -11.0, 4, 5, 22, 0.0)
        self.wings = ModelRenderer(0, 32, 128, 128)
        self.wings.addBox(-13.0, -2.0, -4.0, 26, 2, 8, 0.0)
        self.tailplane = ModelRenderer(70, 32, 128, 128)
        self.tailplane.addBox(-6.0, -2.0, 7.0, 12, 2, 5, 0.0)
        self.tailfin = ModelRenderer(106, 32, 128, 128)
        self.tailfin.addBox(-1.0, -7.0, 7.0, 2, 6, 5, 0.0)
        self.propeller = ModelRenderer(0, 45, 128, 128)
        self.propeller.addBox(-7.0, -1.0, -13.0, 14, 2, 1, 0.0)

    def render(self, x, y, z, xRot, yRot, zRot):
        self.fuselage.render(1.0)
        self.wings.render(1.0)
        self.tailplane.render(1.0)
        self.tailfin.render(1.0)
        self.propeller.render(1.0)
