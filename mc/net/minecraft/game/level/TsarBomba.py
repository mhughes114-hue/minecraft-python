from mc.net.minecraft.game.level.block.Blocks import blocks

import math


class TsarBomba:
    RADIUS = 24
    COLUMNS_PER_TICK = 32

    def __init__(self, world, x, y, z):
        self.world = world
        self.x = int(math.floor(x))
        self.y = int(math.floor(y))
        self.z = int(math.floor(z))
        self.radius = min(
            self.RADIUS, max(1, min(world.width, world.length) // 2)
        )
        self.outerRadius = self.radius * 1.3125
        self.columns = self.__makeSpiral(math.ceil(self.outerRadius))
        self.nextColumn = 0
        self.targetedStorms = []

        from mc.net.minecraft.game.entity.monster.EntityWitherStorm import EntityWitherStorm
        for entity in world.entityMap.all:
            if not isinstance(entity, EntityWitherStorm) or entity.isDead:
                continue

            dx = entity.posX - (self.x + 0.5)
            dy = entity.posY + entity.height * 0.5 - (self.y + 0.5)
            dz = entity.posZ - (self.z + 0.5)
            if dx * dx + dy * dy + dz * dz <= \
               (self.outerRadius + entity.width * 0.5) ** 2:
                self.targetedStorms.append(entity)

    @staticmethod
    def __makeSpiral(radius):
        columns = []
        x = z = 0
        stepX, stepZ = 0, -1
        sideLength = radius * 2 + 1
        for _ in range(sideLength * sideLength):
            if -radius <= x <= radius and -radius <= z <= radius:
                columns.append((x, z))

            if x == z or (x < 0 and x == -z) or \
               (x > 0 and x == 1 - z):
                stepX, stepZ = -stepZ, stepX
            x += stepX
            z += stepZ
        return columns

    def update(self):
        stop = min(
            self.nextColumn + self.COLUMNS_PER_TICK, len(self.columns)
        )
        while self.nextColumn < stop:
            offsetX, offsetZ = self.columns[self.nextColumn]
            self.nextColumn += 1
            distance = math.sqrt(offsetX * offsetX + offsetZ * offsetZ)
            if distance > self.outerRadius:
                continue

            x = self.x + offsetX
            z = self.z + offsetZ
            if x <= 0 or z <= 0 or \
               x >= self.world.width - 1 or z >= self.world.length - 1:
                continue

            self.__processColumn(x, z, distance)

        if self.nextColumn < len(self.columns):
            return False

        self.__finish()
        return True

    def __processColumn(self, x, z, distance):
        insideCrater = distance <= self.radius
        surface = 0
        fluids = (
            blocks.waterMoving.blockID, blocks.waterStill.blockID,
            blocks.waterSource.blockID, blocks.lavaMoving.blockID,
            blocks.lavaStill.blockID, blocks.lavaSource.blockID,
        )

        for y in range(self.world.height - 1, 0, -1):
            blockId = self.world.getBlockId(x, y, z)
            if blockId in fluids:
                if insideCrater:
                    self.world.setBlock(x, y, z, 0)
                continue

            block = blocks.blocksList[blockId] if blockId else None
            if not block:
                continue
            if not block.isOpaqueCube():
                if insideCrater:
                    self.world.setBlock(x, y, z, 0)
                continue
            if not surface:
                surface = y

        if not surface:
            return

        if insideCrater:
            depth = max(1, int((1.0 - distance / self.radius) *
                               self.radius * 0.45) + 1)
            floor = max(2, surface - depth)
            for y in range(surface, floor - 1, -1):
                if self.world.getBlockId(x, y, z) == blocks.bedrock.blockID:
                    break
                self.world.setBlock(x, y, z, 0)
            return

        wave = max(
            0.0,
            1.0 - abs(distance - self.radius * 1.08) /
            (self.radius * 0.32)
        )
        waveHeight = int(wave * 4.0)
        for y in range(surface + 1,
                       min(self.world.height - 1, surface + waveHeight) + 1):
            if self.world.getBlockId(x, y, z) == 0:
                self.world.setBlock(x, y, z, blocks.cobblestone.blockID)

    def __finish(self):
        from mc.net.minecraft.game.entity.monster.EntityWitherStorm import EntityWitherStorm

        for entity in self.targetedStorms:
            if not entity.isDead:
                entity.setEntityDead()

        blastRadius = self.outerRadius
        for entity in self.world.entityMap.all[:]:
            if not isinstance(entity, EntityWitherStorm) or entity.isDead:
                continue

            dx = entity.posX - (self.x + 0.5)
            dy = entity.posY + entity.height * 0.5 - (self.y + 0.5)
            dz = entity.posZ - (self.z + 0.5)
            if dx * dx + dy * dy + dz * dz <= \
               (blastRadius + entity.width * 0.5) ** 2:
                entity.setEntityDead()
