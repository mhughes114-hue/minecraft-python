from mc.net.minecraft.game.entity.Entity import Entity
from mc.net.minecraft.game.entity.FactionAI import _PROTECTED_BLOCKS
from mc.net.minecraft.game.level.block.Blocks import blocks
from nbtlib.tag import Float, Short

import math


class EntityClusterShell(Entity):
    SUBMUNITION_COUNT = 7

    def __init__(self, world, owner=None, targetX=0.0, targetZ=0.0):
        super().__init__(world)
        self.setSize(0.24, 0.24)
        self._canTriggerWalking = False
        self.arrowShake = 0
        self.owner = owner
        self.targetX = targetX
        self.targetZ = targetZ
        self.targetY = self._findImpactHeight(targetX, targetZ)
        self.flightTicks = 0
        self.totalFlightTicks = 20
        self.arcHeight = 8.0

    def _findImpactHeight(self, x, z):
        blockX = max(0, min(self._worldObj.width - 1, int(x)))
        blockZ = max(0, min(self._worldObj.length - 1, int(z)))
        for y in range(self._worldObj.height - 1, 0, -1):
            blockId = self._worldObj.getBlockId(blockX, y, blockZ)
            if blockId and blocks.opaqueCubeLookup[blockId]:
                return y + 1.0
        return 1.0

    def onEntityUpdate(self):
        super().onEntityUpdate()
        self.flightTicks += 1
        progress = min(1.0, self.flightTicks / float(self.totalFlightTicks))
        self.posX = self.startX + (self.targetX - self.startX) * progress
        self.posZ = self.startZ + (self.targetZ - self.startZ) * progress
        self.posY = (
            self.startY + (self.targetY - self.startY) * progress +
            4.0 * self.arcHeight * progress * (1.0 - progress)
        )
        self.setPosition(self.posX, self.posY, self.posZ)
        self.rotationYaw = math.degrees(math.atan2(
            self.targetX - self.startX, self.targetZ - self.startZ
        ))
        self.rotationPitch = -45.0
        if progress >= 1.0:
            self._detonate()

    def setLaunchPosition(self, x, y, z):
        self.startX = x
        self.startY = y
        self.startZ = z
        distance = math.sqrt(
            (self.targetX - x) ** 2 + (self.targetZ - z) ** 2
        )
        self.totalFlightTicks = max(20, min(80, int(distance * 0.75)))
        self.arcHeight = max(8.0, distance * 0.16)
        self.setPosition(x, y, z)

    def _detonate(self):
        self.setEntityDead()
        for index in range(self.SUBMUNITION_COUNT):
            angle = math.tau * index / self.SUBMUNITION_COUNT
            distance = 1.5 + self._rand.nextFloat() * 2.5
            x = self.targetX + math.cos(angle) * distance
            z = self.targetZ + math.sin(angle) * distance
            y = self._findImpactHeight(x, z)
            self._worldObj.createExplosion(
                self.owner, x, y, z, 1.5,
                protectedBlockIds=_PROTECTED_BLOCKS
            )

    def _writeEntityToNBT(self, compound):
        compound['TargetX'] = Float(self.targetX)
        compound['TargetY'] = Float(self.targetY)
        compound['TargetZ'] = Float(self.targetZ)
        compound['StartX'] = Float(self.startX)
        compound['StartY'] = Float(self.startY)
        compound['StartZ'] = Float(self.startZ)
        compound['FlightTicks'] = Short(self.flightTicks)
        compound['TotalFlightTicks'] = Short(self.totalFlightTicks)
        compound['ArcHeight'] = Float(self.arcHeight)

    def _readEntityFromNBT(self, compound):
        self.targetX = compound.get('TargetX', Float(self.posX)).real
        self.targetY = compound.get('TargetY', Float(self.posY)).real
        self.targetZ = compound.get('TargetZ', Float(self.posZ)).real
        self.startX = compound.get('StartX', Float(self.posX)).real
        self.startY = compound.get('StartY', Float(self.posY)).real
        self.startZ = compound.get('StartZ', Float(self.posZ)).real
        self.flightTicks = compound.get('FlightTicks', Short(0)).real
        self.totalFlightTicks = max(
            1, compound.get('TotalFlightTicks', Short(20)).real
        )
        self.arcHeight = compound.get('ArcHeight', Float(8.0)).real

    def _getEntityString(self):
        return 'ClusterShell'

    def getShadowSize(self):
        return 0.0
