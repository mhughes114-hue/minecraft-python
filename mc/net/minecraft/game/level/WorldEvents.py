import math
import random

from mc.net.minecraft.game.level.block.Blocks import blocks


class NoahsFlood:
    WARNING_TICKS = 600
    BLOCKS_PER_TICK = 1024

    def __init__(self, world, postMessage):
        self.world = world
        self.postMessage = postMessage
        self.state = 'idle'
        self.ticksUntilFlood = 0
        self.floodY = 0
        self.floodCursor = 0

    def start(self):
        if self.state in ('warning', 'flooding'):
            return "Noah's Flood is already underway."
        if self.state == 'complete':
            return 'This world has already been flooded.'

        self.state = 'warning'
        self.ticksUntilFlood = self.WARNING_TICKS
        self.postMessage(
            'God: Build an ark. The entire earth will be flooded in 30 seconds.'
        )
        return "Noah's Flood warning started. Build an ark!"

    def stop(self):
        if self.state not in ('warning', 'flooding'):
            return 'No flood is underway.'

        self.state = 'stopped'
        return "Noah's Flood has been stopped; existing water remains."

    def status(self):
        if self.state == 'warning':
            return "Noah's Flood begins in " + \
                   str(math.ceil(self.ticksUntilFlood / 20.0)) + ' seconds.'
        return "Noah's Flood status: " + self.state + '.'

    def update(self):
        if self.state == 'warning':
            self.ticksUntilFlood -= 1
            if self.ticksUntilFlood in (400, 200):
                seconds = self.ticksUntilFlood // 20
                self.postMessage(
                    'God: The flood begins in ' + str(seconds) +
                    ' seconds. Finish your ark!'
                )
            elif self.ticksUntilFlood <= 0:
                self.state = 'flooding'
                self.floodY = max(1, self.world.waterLevel)
                self.postMessage(
                    'God: The rain begins. The waters are rising over all the earth!'
                )

        if self.state == 'flooding':
            self.__raiseWater()

    def __raiseWater(self):
        width = self.world.width - 2
        length = self.world.length - 2
        if width <= 0 or length <= 0:
            self.state = 'complete'
            self.postMessage('The flood has covered the world.')
            return

        layerSize = width * length
        end = min(self.floodCursor + self.BLOCKS_PER_TICK, layerSize)
        waterId = blocks.waterStill.blockID
        for index in range(self.floodCursor, end):
            x = 1 + index % width
            z = 1 + index // width
            if self.world.getBlockId(x, self.floodY, z) == 0:
                self.world.setBlock(x, self.floodY, z, waterId)

        self.floodCursor = end
        if self.floodCursor < layerSize:
            return

        self.floodCursor = 0
        self.floodY += 1
        if self.floodY < self.world.height - 1:
            if self.floodY % 8 == 0:
                self.postMessage('God: The floodwaters are rising...')
            return

        self.state = 'complete'
        self.postMessage('The entire world is beneath the floodwaters.')


class Sinkhole:
    DURATION_TICKS = 40

    def __init__(self, world, target, postMessage):
        self.world = world
        self.target = target
        self.postMessage = postMessage
        self.ticksRemaining = self.DURATION_TICKS
        self.__open()

    def __open(self):
        x = int(self.target.posX)
        z = int(self.target.posZ)
        top = int(self.target.boundingBox.minY) - 1
        protected = {
            blocks.bedrock.blockID,
            blocks.oreGold.blockID,
            blocks.oreIron.blockID,
            blocks.oreDiamond.blockID,
            blocks.blockGold.blockID,
            blocks.blockSteel.blockID,
            blocks.blockDiamond.blockID,
            blocks.obsidian.blockID,
            blocks.chest.blockID,
            blocks.stoneOvenIdle.blockID,
            blocks.stoneOvenActive.blockID,
            blocks.luckyBlock.blockID,
            blocks.tsarBomba.blockID,
        }

        for y in range(max(1, top - 7), top + 1):
            for offsetX in range(-2, 3):
                for offsetZ in range(-2, 3):
                    blockX = x + offsetX
                    blockZ = z + offsetZ
                    if blockX <= 0 or blockZ <= 0 or \
                       blockX >= self.world.width - 1 or \
                       blockZ >= self.world.length - 1:
                        continue
                    blockId = self.world.getBlockId(blockX, y, blockZ)
                    if blockId and blockId not in protected:
                        self.world.setBlock(blockX, y, blockZ, 0)

        self.postMessage('A sinkhole opens beneath someone nearby!')
        self.world.spawnParticle(
            'largesmoke', self.target.posX, self.target.boundingBox.minY,
            self.target.posZ, 0.0, 0.0, 0.0
        )

    def update(self):
        if not self.target.isEntityAlive():
            return True

        self.target.motionY = -0.5
        self.ticksRemaining -= 1
        if self.ticksRemaining > 0:
            return False

        if self.target is self.world.playerEntity:
            self.target.health = 0
            self.target.deathTime = 0
        else:
            self.target.setEntityDead()
        self.postMessage('The earth consumes its victim in the sinkhole!')
        return True


class WorldEvents:
    def __init__(self, world, postMessage):
        self.world = world
        self.postMessage = postMessage
        self.flood = NoahsFlood(world, postMessage)
        self.sinkholes = []
        self.nextSinkholeIn = random.randint(1200, 3600)

    def update(self):
        self.flood.update()
        self.sinkholes = [
            sinkhole for sinkhole in self.sinkholes if not sinkhole.update()
        ]

        self.nextSinkholeIn -= 1
        if self.nextSinkholeIn <= 0:
            targets = self.__livingTargets()
            if targets:
                self.startSinkhole(random.choice(targets))
            self.nextSinkholeIn = random.randint(1200, 3600)

    def selectSinkholeTarget(self, selector):
        targets = self.__livingTargets()
        if selector == 'player':
            targets = [target for target in targets
                       if target is self.world.playerEntity]
        elif selector == 'mob':
            targets = [target for target in targets
                       if target is not self.world.playerEntity]
        elif selector != 'random':
            return None

        return random.choice(targets) if targets else None

    def startSinkhole(self, target):
        if not target:
            return False

        self.sinkholes.append(Sinkhole(self.world, target, self.postMessage))
        return True

    def __livingTargets(self):
        from mc.net.minecraft.game.entity.EntityLiving import EntityLiving

        return [
            entity for entity in self.world.entityMap.all
            if isinstance(entity, EntityLiving) and entity.isEntityAlive()
        ]
