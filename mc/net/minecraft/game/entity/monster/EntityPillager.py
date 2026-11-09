from mc.net.minecraft.game.entity.FactionAI import (
    breakObstructingBlock,
    findFactionTarget,
)
from mc.net.minecraft.game.entity.monster.EntityMob import EntityMob
from mc.net.minecraft.game.entity.projectile.EntityLaserBolt import EntityLaserBolt
import math


class EntityPillager(EntityMob):
    canDamageInCreative = True
    canSpawnInDaylight = True

    def __init__(self, world):
        super().__init__(world)
        self._texture = 'mob/pillager.png'
        self._moveSpeed = 0.7
        self._attackStrength = 3

    def onLivingUpdate(self):
        super().onLivingUpdate()
        if self.ticksExisted % 40 == 0:
            breakObstructingBlock(self, self._playerToAttack)

    def _updatePlayerActionState(self):
        super()._updatePlayerActionState()
        target = self._playerToAttack
        if not target or not target.isEntityAlive():
            return

        xd = target.posX - self.posX
        zd = target.posZ - self.posZ
        distanceSquared = xd * xd + zd * zd
        if 9.0 < distanceSquared < 196.0:
            self.rotationYaw = math.degrees(math.atan2(zd, xd)) - 90.0
            strafeDirection = 1.0 if (self.ticksExisted // 20) % 2 else -1.0
            self._moveStrafing = self._moveSpeed * strafeDirection
            self._moveForward = -self._moveSpeed * 0.35

    def _findPlayerToAttack(self):
        from mc.net.minecraft.game.entity.animal.EntityVillager import EntityVillager
        from mc.net.minecraft.game.entity.monster.EntityVillagerAircraft import EntityVillagerAircraft
        from mc.net.minecraft.game.entity.monster.EntityVillagerTank import EntityVillagerTank

        for targetType in (EntityVillager, EntityVillagerTank, EntityVillagerAircraft):
            target = findFactionTarget(self, targetType, 48.0)
            if target:
                return target

        return None

    def _attackEntity(self, entity, distance):
        if distance < 2.5:
            if self.attackTime == 0:
                super()._attackEntity(entity, distance)
            return

        if distance >= 14.0 or self.attackTime != 0:
            return

        xd = entity.posX - self.posX
        zd = entity.posZ - self.posZ
        from mc.net.minecraft.game.entity.animal.EntityVillager import EntityVillager
        from mc.net.minecraft.game.entity.monster.EntityVillagerAircraft import EntityVillagerAircraft
        from mc.net.minecraft.game.entity.monster.EntityVillagerTank import EntityVillagerTank

        targetType = next((kind for kind in (
            EntityVillager, EntityVillagerTank, EntityVillagerAircraft
        ) if isinstance(entity, kind)), None)
        if targetType is None:
            return

        bolt = EntityLaserBolt(self._worldObj, self, targetType, (1.0, 0.3, 0.2))
        bolt.posY += self._getEyeHeight() - 0.1
        yd = entity.posY + entity.height * 0.5 - bolt.posY
        travelTime = math.sqrt(xd * xd + zd * zd) * 0.2
        self._worldObj.spawnEntityInWorld(bolt)
        bolt.fireAt(xd, yd + travelTime, zd)
        self.attackTime = 35
        self.rotationYaw = math.degrees(math.atan2(zd, xd)) - 90.0
        self._hasAttacked = True

    def _getEntityString(self):
        return 'Pillager'
