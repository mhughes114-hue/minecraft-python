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
    TSAR_BOMBA_INITIAL_DELAY = 3 * 24000
    TSAR_BOMBA_COOLDOWN = 12000
    TSAR_BOMBA_COOLDOWN_VARIANCE = 12000
    NORMAL_BOMB_COOLDOWN = 200
    MLRS_COOLDOWN = 100
    MLRS_RANGE = 72.0

    def __init__(self, world, faction, vehicle):
        super().__init__(world)
        self.faction = faction
        self.vehicle = vehicle
        self._tsarBombCooldown = self.TSAR_BOMBA_INITIAL_DELAY
        self._normalBombCooldown = self.NORMAL_BOMB_COOLDOWN
        self._mlrsCooldown = 60
        self._texture = f'mob/{faction}_{"tank" if vehicle in ("tank", "mlrs") else "plane"}.png'
        if vehicle in ('tank', 'mlrs'):
            self.health = 80
            self._attackStrength = 8 if vehicle == 'tank' else 4
            self._moveSpeed = 0.45 if vehicle == 'tank' else 0.3
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
        self._updateTsarBomba()
        self._updateMLRS()

    def _updateTsarBomba(self):
        if self.vehicle != 'aircraft' or self.health <= 0 or \
           not self._playerToAttack or \
           not self._playerToAttack.isEntityAlive():
            return

        target = self._playerToAttack
        if self._tsarBombCooldown > 0:
            self._tsarBombCooldown -= 1
            self._dropNormalBombWhenReady(target)
            return

        world = self._worldObj
        if world.tsarBombaCooldown > 0:
            self._dropNormalBombWhenReady(target)
            return

        from mc.net.minecraft.game.level.TsarBomba import TsarBomba

        world.tsarBombs.append(
            TsarBomba(world, target.posX, target.posY, target.posZ)
        )
        world.tsarBombaCooldown = (
            self.TSAR_BOMBA_COOLDOWN +
            world.rand.nextInt(self.TSAR_BOMBA_COOLDOWN_VARIANCE + 1)
        )

    def _dropNormalBombWhenReady(self, target):
        if self._normalBombCooldown > 0:
            self._normalBombCooldown -= 1
            return

        self._dropNormalBomb(target)
        self._normalBombCooldown = self.NORMAL_BOMB_COOLDOWN

    def _dropNormalBomb(self, target):
        from mc.net.minecraft.game.entity.misc.EntityTNTPrimed import EntityTNTPrimed

        bomb = EntityTNTPrimed(
            self._worldObj, target.posX, target.posY + 10.0, target.posZ
        )
        bomb.fuse = 40
        bomb.motionX = 0.0
        bomb.motionY = -0.2
        bomb.motionZ = 0.0
        self._worldObj.spawnEntityInWorld(bomb)

    def _updateMLRS(self):
        if self.vehicle != 'mlrs' or self.health <= 0 or \
           not self._playerToAttack or \
           not self._playerToAttack.isEntityAlive():
            return

        if self._mlrsCooldown > 0:
            self._mlrsCooldown -= 1

    def _fireMLRS(self, target):
        from mc.net.minecraft.game.entity.projectile.EntityClusterShell import (
            EntityClusterShell,
        )

        shell = EntityClusterShell(
            self._worldObj, self, target.posX, target.posZ
        )
        shell.setLaunchPosition(
            self.posX, self.posY + self.height * 0.5, self.posZ
        )
        self._worldObj.spawnEntityInWorld(shell)
        self._mlrsCooldown = self.MLRS_COOLDOWN
        self._hasAttacked = True
        self.rotationYaw = math.degrees(math.atan2(
            target.posZ - self.posZ, target.posX - self.posX
        )) - 90.0

    def _findPlayerToAttack(self):
        searchRange = self.MLRS_RANGE if self.vehicle == 'mlrs' else 48.0
        if self.faction == 'villager':
            from mc.net.minecraft.game.entity.monster.EntityPillager import EntityPillager
            from mc.net.minecraft.game.entity.monster.EntityPillagerAircraft import EntityPillagerAircraft
            from mc.net.minecraft.game.entity.monster.EntityPillagerMLRS import EntityPillagerMLRS
            from mc.net.minecraft.game.entity.monster.EntityPillagerTank import EntityPillagerTank

            for targetType in (EntityPillager, EntityPillagerTank,
                               EntityPillagerAircraft, EntityPillagerMLRS):
                target = findFactionTarget(self, targetType, searchRange)
                if target:
                    return target

            return None

        from mc.net.minecraft.game.entity.animal.EntityVillager import EntityVillager
        from mc.net.minecraft.game.entity.monster.EntityVillagerAircraft import EntityVillagerAircraft
        from mc.net.minecraft.game.entity.monster.EntityVillagerMLRS import EntityVillagerMLRS
        from mc.net.minecraft.game.entity.monster.EntityVillagerTank import EntityVillagerTank

        target = findFactionTarget(self, EntityVillager, searchRange)
        if target:
            return target

        target = findFactionTarget(self, EntityVillagerTank, searchRange)
        return target or findFactionTarget(self, EntityVillagerAircraft, searchRange) or \
               findFactionTarget(self, EntityVillagerMLRS, searchRange)

    def _attackEntity(self, entity, distance):
        if self.vehicle == 'mlrs':
            if distance < 12.0 or distance > self.MLRS_RANGE or \
               self._mlrsCooldown > 0 or self.attackTime > 0:
                return

            from mc.net.minecraft.game.entity.animal.EntityVillager import EntityVillager
            from mc.net.minecraft.game.entity.monster.EntityPillager import EntityPillager
            from mc.net.minecraft.game.entity.monster.EntityPillagerAircraft import EntityPillagerAircraft
            from mc.net.minecraft.game.entity.monster.EntityPillagerMLRS import EntityPillagerMLRS
            from mc.net.minecraft.game.entity.monster.EntityPillagerTank import EntityPillagerTank
            from mc.net.minecraft.game.entity.monster.EntityVillagerAircraft import EntityVillagerAircraft
            from mc.net.minecraft.game.entity.monster.EntityVillagerMLRS import EntityVillagerMLRS
            from mc.net.minecraft.game.entity.monster.EntityVillagerTank import EntityVillagerTank

            enemyTypes = (
                (EntityPillager, EntityPillagerTank, EntityPillagerAircraft,
                 EntityPillagerMLRS)
                if self.faction == 'villager' else
                (EntityVillager, EntityVillagerTank, EntityVillagerAircraft,
                 EntityVillagerMLRS)
            )
            if isinstance(entity, enemyTypes):
                self._fireMLRS(entity)
                self.attackTime = 30
            return

        if distance >= 30.0 or self.attackTime > 0:
            return

        if self.faction == 'villager':
            from mc.net.minecraft.game.entity.monster.EntityPillager import EntityPillager
            from mc.net.minecraft.game.entity.monster.EntityPillagerAircraft import EntityPillagerAircraft
            from mc.net.minecraft.game.entity.monster.EntityPillagerTank import EntityPillagerTank

            from mc.net.minecraft.game.entity.monster.EntityPillagerMLRS import EntityPillagerMLRS
            targetTypes = (EntityPillager, EntityPillagerTank,
                           EntityPillagerAircraft, EntityPillagerMLRS)
            color = (0.25, 0.9, 1.0)
        else:
            from mc.net.minecraft.game.entity.animal.EntityVillager import EntityVillager
            from mc.net.minecraft.game.entity.monster.EntityVillagerAircraft import EntityVillagerAircraft
            from mc.net.minecraft.game.entity.monster.EntityVillagerMLRS import EntityVillagerMLRS
            from mc.net.minecraft.game.entity.monster.EntityVillagerTank import EntityVillagerTank

            targetTypes = (EntityVillager, EntityVillagerTank,
                           EntityVillagerAircraft, EntityVillagerMLRS)
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
