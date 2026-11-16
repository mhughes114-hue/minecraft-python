from mc.net.minecraft.game.entity.monster.EntityMob import EntityMob
import math


class EntityFPVDrone(EntityMob):
    canDamageInCreative = True
    canSpawnInDaylight = True
    TARGET_RANGE = 48.0
    ATTACK_COOLDOWN = 12

    def __init__(self, world):
        super().__init__(world)
        self._texture = 'mob/pillager_plane.png'
        self.health = 24
        self._attackStrength = 5
        self._moveSpeed = 0.9
        self._isCreativeFlying = True
        self._creativeFlightMultiplier = 3.5
        self.setSize(0.9, 0.45)

    def onLivingUpdate(self):
        verticalCorrection = 0.0
        target = self._playerToAttack
        if target and target.isEntityAlive():
            verticalCorrection = max(
                -0.08, min(0.08, (target.posY - self.posY) * 0.02)
            )

        self.motionY += 0.08 + verticalCorrection
        super().onLivingUpdate()

    def _findPlayerToAttack(self):
        from mc.net.minecraft.game.entity.player.EntityPlayer import EntityPlayer
        from mc.net.minecraft.game.entity.animal.EntityVillager import EntityVillager
        from mc.net.minecraft.game.entity.monster.EntityPillager import EntityPillager
        from mc.net.minecraft.game.entity.monster.EntityPillagerAircraft import EntityPillagerAircraft
        from mc.net.minecraft.game.entity.monster.EntityPillagerMLRS import EntityPillagerMLRS
        from mc.net.minecraft.game.entity.monster.EntityPillagerTank import EntityPillagerTank
        from mc.net.minecraft.game.entity.monster.EntityVillagerAircraft import EntityVillagerAircraft
        from mc.net.minecraft.game.entity.monster.EntityVillagerMLRS import EntityVillagerMLRS
        from mc.net.minecraft.game.entity.monster.EntityVillagerTank import EntityVillagerTank

        targetTypes = (
            EntityPlayer, EntityVillager, EntityPillager,
            EntityVillagerTank, EntityVillagerAircraft, EntityVillagerMLRS,
            EntityPillagerTank, EntityPillagerAircraft, EntityPillagerMLRS,
        )
        area = self.boundingBox.expand(self.TARGET_RANGE, 24.0, self.TARGET_RANGE)
        closest = None
        closestDistance = self.TARGET_RANGE * self.TARGET_RANGE
        for candidate in self._worldObj.getEntitiesWithinAABBExcludingEntity(self, area):
            if not isinstance(candidate, targetTypes) or not candidate.isEntityAlive():
                continue

            distance = self.getDistanceSqToEntity(candidate)
            if distance < closestDistance:
                closest = candidate
                closestDistance = distance

        return closest

    def _updatePlayerActionState(self):
        self._hasAttacked = False
        target = self._findPlayerToAttack()
        self._playerToAttack = target
        self._moveStrafing = 0.0
        self._isJumping = False
        if not target:
            self._moveForward = 0.0
            return

        dx = target.posX - self.posX
        dy = target.posY + target.height * 0.5 - (self.posY + self.height * 0.5)
        dz = target.posZ - self.posZ
        distance = math.sqrt(dx * dx + dy * dy + dz * dz)
        self.rotationYaw = math.degrees(math.atan2(dz, dx)) - 90.0
        self._moveForward = self._moveSpeed
        if distance <= 2.5 and self.attackTime == 0:
            target.attackEntityFrom(self, self._attackStrength)
            self.attackTime = self.ATTACK_COOLDOWN
            self._hasAttacked = True

    def _getEntityString(self):
        return 'FPVDrone'
