from mc.net.minecraft.game.entity.Entity import Entity
from mc.net.minecraft.game.entity.FactionAI import _PROTECTED_BLOCKS


class EntityLandmine(Entity):
    TRIGGER_RADIUS = 1.6

    def __init__(self, world):
        super().__init__(world)
        self.setSize(0.45, 0.12)
        self._canTriggerWalking = False

    def onEntityUpdate(self):
        super().onEntityUpdate()
        self._checkForDetonation()

    def _checkForDetonation(self):
        radius = self.TRIGGER_RADIUS
        nearbyEntities = self._worldObj.getEntitiesWithinAABBExcludingEntity(
            self, self.boundingBox.expand(radius, radius, radius)
        )
        for entity in nearbyEntities:
            if entity is self or not hasattr(entity, 'health') or \
               not entity.isEntityAlive():
                continue

            dx = entity.posX - self.posX
            dy = entity.posY - self.posY
            dz = entity.posZ - self.posZ
            if dx * dx + dy * dy + dz * dz <= radius * radius:
                self.setEntityDead()
                self._worldObj.createExplosion(
                    self, self.posX, self.posY, self.posZ, 2.2,
                    protectedBlockIds=_PROTECTED_BLOCKS
                )
                return

    def _getEntityString(self):
        return 'Landmine'
