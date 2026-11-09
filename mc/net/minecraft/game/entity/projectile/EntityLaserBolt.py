from mc.net.minecraft.game.entity.projectile.EntityArrow import EntityArrow


class EntityLaserBolt(EntityArrow):

    def __init__(self, world, owner, targetType, color):
        super().__init__(world, owner)
        self.targetType = targetType
        self.damage = 6
        self.isLaser = True
        self.laserColor = color

    def fireAt(self, x, y, z):
        self.setArrowHeading(x, y, z, 1.8, 0.5)
