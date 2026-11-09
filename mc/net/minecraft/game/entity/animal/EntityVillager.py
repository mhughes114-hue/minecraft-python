from mc.net.minecraft.game.entity.FactionAI import (
    breakObstructingBlock,
    findFactionTarget,
)
from mc.net.minecraft.game.entity.animal.EntityAnimal import EntityAnimal
from mc.net.minecraft.game.entity.projectile.EntityLaserBolt import EntityLaserBolt
import math


class EntityVillager(EntityAnimal):

    def __init__(self, world):
        super().__init__(world)
        self._texture = 'char.png'
        self._moveSpeed = 0.65
        self._attackStrength = 3

    def onLivingUpdate(self):
        super().onLivingUpdate()
        if self.ticksExisted % 40 == 0:
            breakObstructingBlock(self, self._playerToAttack)

    def _findPlayerToAttack(self):
        from mc.net.minecraft.game.entity.monster.EntityPillager import EntityPillager
        from mc.net.minecraft.game.entity.monster.EntityPillagerAircraft import EntityPillagerAircraft
        from mc.net.minecraft.game.entity.monster.EntityPillagerTank import EntityPillagerTank

        for targetType in (EntityPillager, EntityPillagerTank, EntityPillagerAircraft):
            target = findFactionTarget(self, targetType)
            if target:
                return target

        return None

    def _attackEntity(self, entity, distance):
        if distance < 2.5:
            if self.attackTime == 0 and entity.boundingBox.maxY > self.boundingBox.minY and \
               entity.boundingBox.minY < self.boundingBox.maxY:
                self.attackTime = 20
                entity.attackEntityFrom(self, self._attackStrength)
                self._hasAttacked = True
            return

        if distance >= 18.0 or self.attackTime != 0:
            return

        from mc.net.minecraft.game.entity.monster.EntityPillager import EntityPillager
        from mc.net.minecraft.game.entity.monster.EntityPillagerAircraft import EntityPillagerAircraft
        from mc.net.minecraft.game.entity.monster.EntityPillagerTank import EntityPillagerTank

        targetType = next((kind for kind in (
            EntityPillager, EntityPillagerTank, EntityPillagerAircraft
        ) if isinstance(entity, kind)), None)
        if targetType is None:
            return

        dx = entity.posX - self.posX
        dz = entity.posZ - self.posZ
        bolt = EntityLaserBolt(self._worldObj, self, targetType, (0.25, 0.9, 1.0))
        bolt.posY += self._getEyeHeight() - 0.1
        dy = entity.posY + entity.height * 0.5 - bolt.posY
        lead = math.sqrt(dx * dx + dz * dz) * 0.12
        self._worldObj.spawnEntityInWorld(bolt)
        bolt.fireAt(dx, dy + lead, dz)
        self.attackTime = 30
        self._hasAttacked = True

    def _getEntityString(self):
        return 'Villager'
