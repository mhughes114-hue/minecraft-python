from mc.net.minecraft.game.entity.projectile.EntityArrow import EntityArrow
from mc.net.minecraft.game.entity.FactionAI import _PROTECTED_BLOCKS


class EntityLaserBolt(EntityArrow):

    def __init__(self, world, owner, targetType, color, explosive=False):
        super().__init__(world, owner)
        self.targetType = targetType
        self.damage = 6
        self.isLaser = True
        self.laserColor = color
        self.explosive = explosive

    def fireAt(self, x, y, z):
        self.setArrowHeading(x, y, z, 1.8, 0.5)

    def _onImpact(self, hit):
        if not self.explosive:
            return

        if hit.entityHit:
            x = hit.entityHit.posX
            y = hit.entityHit.posY + hit.entityHit.height * 0.5
            z = hit.entityHit.posZ
        else:
            x = hit.hitVec.xCoord
            y = hit.hitVec.yCoord
            z = hit.hitVec.zCoord

        self._worldObj.createExplosion(
            self.getOwner(), x, y, z, 2.5, _PROTECTED_BLOCKS
        )
