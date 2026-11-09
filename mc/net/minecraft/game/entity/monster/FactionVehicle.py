from mc.net.minecraft.game.entity.FactionAI import (
    breakObstructingBlock,
    findFactionTarget,
)
from mc.net.minecraft.game.entity.monster.EntityMob import EntityMob
from mc.net.minecraft.game.entity.projectile.EntityLaserBolt import EntityLaserBolt
import math


class FactionVehicle(EntityMob):
    canDamageInCreative = True
    canSpawnInDaylight = True

    def __init__(self, world, faction, vehicle):
        super().__init__(world)
        self.faction = faction
        self.vehicle = vehicle
        self._texture = f'mob/{faction}_{vehicle if vehicle == "tank" else "plane"}.png'
        if vehicle == 'tank':
            self.health = 80
            self._attackStrength = 8
            self._moveSpeed = 0.45
            self.setSize(3.2, 1.8)
        else:
            self.health = 50
            self._attackStrength = 5
            self._moveSpeed = 0.7
            self.setSize(4.5, 1.8)
            self._isCreativeFlying = True
            self._creativeFlightMultiplier = 8.0

    def onLivingUpdate(self):
        if self.vehicle == 'aircraft' and self.health > 0:
            target = self._playerToAttack
            verticalCorrection = 0.0
            if target and target.isEntityAlive():
                verticalCorrection = max(-0.04, min(0.04, (target.posY - self.posY) * 0.02))
            self.motionY += 0.08 + verticalCorrection

        super().onLivingUpdate()
        if self.ticksExisted % 40 == 0:
            breakObstructingBlock(self, self._playerToAttack)

    def _findPlayerToAttack(self):
        if self.faction == 'villager':
            from mc.net.minecraft.game.entity.monster.EntityPillager import EntityPillager
            from mc.net.minecraft.game.entity.monster.EntityPillagerAircraft import EntityPillagerAircraft
            from mc.net.minecraft.game.entity.monster.EntityPillagerTank import EntityPillagerTank

            for targetType in (EntityPillager, EntityPillagerTank, EntityPillagerAircraft):
                target = findFactionTarget(self, targetType, 48.0)
                if target:
                    return target

            return None

        from mc.net.minecraft.game.entity.animal.EntityVillager import EntityVillager
        from mc.net.minecraft.game.entity.monster.EntityVillagerAircraft import EntityVillagerAircraft
        from mc.net.minecraft.game.entity.monster.EntityVillagerTank import EntityVillagerTank

        target = findFactionTarget(self, EntityVillager, 48.0)
        if target:
            return target

        target = findFactionTarget(self, EntityVillagerTank, 48.0)
        return target or findFactionTarget(self, EntityVillagerAircraft, 48.0)

    def _attackEntity(self, entity, distance):
        if distance >= 30.0 or self.attackTime > 0:
            return

        if self.faction == 'villager':
            from mc.net.minecraft.game.entity.monster.EntityPillager import EntityPillager
            from mc.net.minecraft.game.entity.monster.EntityPillagerAircraft import EntityPillagerAircraft
            from mc.net.minecraft.game.entity.monster.EntityPillagerTank import EntityPillagerTank

            targetTypes = (EntityPillager, EntityPillagerTank, EntityPillagerAircraft)
            color = (0.25, 0.9, 1.0)
        else:
            from mc.net.minecraft.game.entity.animal.EntityVillager import EntityVillager
            from mc.net.minecraft.game.entity.monster.EntityVillagerAircraft import EntityVillagerAircraft
            from mc.net.minecraft.game.entity.monster.EntityVillagerTank import EntityVillagerTank

            targetTypes = (EntityVillager, EntityVillagerTank, EntityVillagerAircraft)
            color = (1.0, 0.3, 0.2)

        targetType = next((kind for kind in targetTypes if isinstance(entity, kind)), None)
        if targetType is None:
            return

        dx = entity.posX - self.posX
        dz = entity.posZ - self.posZ
        bolt = EntityLaserBolt(
            self._worldObj, self, targetType, color,
            explosive=self.vehicle == 'tank'
        )
        bolt.posY += self._getEyeHeight() - 0.1
        dy = entity.posY + entity.height * 0.5 - bolt.posY
        lead = math.sqrt(dx * dx + dz * dz) * 0.12
        self._worldObj.spawnEntityInWorld(bolt)
        bolt.fireAt(dx, dy + lead, dz)
        self.attackTime = 24 if self.vehicle == 'tank' else 30
        self.rotationYaw = math.degrees(math.atan2(dz, dx)) - 90.0
        self._hasAttacked = True

    def _writeEntityToNBT(self, compound):
        super()._writeEntityToNBT(compound)

    def _readEntityFromNBT(self, compound):
        super()._readEntityFromNBT(compound)
