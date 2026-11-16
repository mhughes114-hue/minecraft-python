from mc.net.minecraft.client.effect.EntitySmokeFX import EntitySmokeFX


class EntityTsarCloudFX(EntitySmokeFX):

    def __init__(self, world, x, y, z, xr, yr, zr):
        super().__init__(world, x, y, z, 7.0)
        self._motionX1 = xr
        self._motionY1 = yr
        self._motionZ1 = zr
        self._particleRed = 0.42
        self._particleGreen = 0.38
        self._particleBlue = 0.34
