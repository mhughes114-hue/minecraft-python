from mc.net.minecraft.game.entity.monster.EntityGiantZombie import EntityGiantZombie
from mc.net.minecraft.game.entity.monster.EntityMob import EntityMob
from mc.net.minecraft.game.level.block.Blocks import blocks
from nbtlib.tag import Short

import math

class EntityWitherStorm(EntityGiantZombie):

    def __init__(self, world):
        super().__init__(world)
        self._texture = 'mob/witherstorm.png'
        self.health = 600
        self.absorbedCount = 0
        self._moveSpeed = 0.45
        self._updateGrowth()

    @property
    def evolutionStage(self):
        return min(self.absorbedCount // 20, 3)

    def onLivingUpdate(self):
        super().onLivingUpdate()
        if self.isDead or self.health <= 0:
            return

        if self.ticksExisted % 40 == 0:
            self._absorbNearbyEntities()
            self._absorbNearbyBlocks()

        attackInterval = 120 - self.evolutionStage * 20
        if self.ticksExisted % attackInterval:
            return

        player = self._worldObj.getPlayerEntity()
        if not player or not player.isEntityAlive():
            return

        x = player.posX - self.posX
        y = player.posY - self.posY
        z = player.posZ - self.posZ
        attackRange = 24.0 + self.evolutionStage * 8.0
        if x * x + y * y + z * z <= attackRange * attackRange:
            self._worldObj.createExplosion(
                self, player.posX, player.posY + 1.0, player.posZ,
                3.0 + self.evolutionStage
            )

    def _updatePlayerActionState(self):
        super()._updatePlayerActionState()
        player = self._playerToAttack
        if not player or not player.isEntityAlive():
            return

        x = player.posX - self.posX
        z = player.posZ - self.posZ
        if x * x + z * z > 256.0 and self.ticksExisted % 100 < 25:
            self.rotationYaw = math.degrees(math.atan2(z, x)) - 90.0
            self._moveForward = self._moveSpeed * 1.5
            self._isJumping = player.posY > self.posY + 1.0

    def _findPlayerToAttack(self):
        player = self._worldObj.getPlayerEntity()
        return player if player and player.isEntityAlive() else None

    def _absorbNearbyEntities(self):
        for entity in self._worldObj.getEntitiesWithinAABBExcludingEntity(
                self, self.boundingBox.expand(6.0, 4.0, 6.0)):
            if entity is self._worldObj.getPlayerEntity() or \
               not isinstance(entity, EntityMob):
                continue

            entity.setEntityDead()
            self._recordAbsorption()
            self.health = min(600, self.health + 20)
            break

    def _absorbNearbyBlocks(self):
        protectedBlocks = (
            blocks.bedrock.blockID, blocks.oreGold.blockID,
            blocks.oreIron.blockID, blocks.tnt.blockID,
            blocks.blockGold.blockID, blocks.blockSteel.blockID,
            blocks.obsidian.blockID, blocks.chest.blockID,
            blocks.oreDiamond.blockID, blocks.blockDiamond.blockID,
            blocks.stoneOvenIdle.blockID, blocks.stoneOvenActive.blockID,
            blocks.luckyBlock.blockID
        )
        absorbed = 0
        for _ in range(12):
            x = int(self.posX) + self._rand.nextInt(11) - 5
            y = int(self.posY) + self._rand.nextInt(9) - 4
            z = int(self.posZ) + self._rand.nextInt(11) - 5
            if x < 0 or y < 0 or z < 0 or x >= self._worldObj.width or \
               y >= self._worldObj.height or z >= self._worldObj.length:
                continue

            blockId = self._worldObj.getBlockId(x, y, z)
            block = blocks.blocksList[blockId] if blockId else None
            if not block or blockId in protectedBlocks or not block.isOpaqueCube():
                continue

            if self._worldObj.setBlockWithNotify(x, y, z, 0):
                self._recordAbsorption()
                absorbed += 1
                if absorbed == 2:
                    break

    def _recordAbsorption(self):
        self.absorbedCount = min(self.absorbedCount + 1, 60)
        self._updateGrowth()

    def _updateGrowth(self):
        stage = self.evolutionStage
        self._attackStrength = 12 + stage * 3
        self.setSize(4.0 + stage * 0.7, 6.0 + stage * 0.8)

    def _writeEntityToNBT(self, compound):
        super()._writeEntityToNBT(compound)
        compound['Absorbed'] = Short(self.absorbedCount)

    def _readEntityFromNBT(self, compound):
        super()._readEntityFromNBT(compound)
        self.absorbedCount = min(max(0, compound.get('Absorbed', Short(0)).real), 60)
        self._updateGrowth()

    def _getEntityString(self):
        return 'WitherStorm'
