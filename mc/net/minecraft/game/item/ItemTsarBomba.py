from mc.net.minecraft.game.item.Item import Item

import math


class ItemTsarBomba(Item):

    def __init__(self, items, itemId):
        super().__init__(items, itemId)
        self._maxStackSize = 1

    def onItemRightClick(self, stack, world, player):
        from mc.net.minecraft.game.entity.monster.EntityWitherStorm import EntityWitherStorm
        from mc.net.minecraft.game.level.TsarBomba import TsarBomba

        yaw = math.radians(player.rotationYaw)
        pitch = math.radians(player.rotationPitch)
        directionX = -math.sin(yaw) * math.cos(pitch)
        directionY = -math.sin(pitch)
        directionZ = math.cos(yaw) * math.cos(pitch)
        originX = player.posX
        originY = player.posY + player.height * 0.9
        originZ = player.posZ

        target = None
        targetDistance = float('inf')
        for entity in world.entityMap.all:
            if not isinstance(entity, EntityWitherStorm) or entity.isDead:
                continue

            offsetX = entity.posX - originX
            offsetY = entity.posY + entity.height * 0.5 - originY
            offsetZ = entity.posZ - originZ
            distance = offsetX * directionX + offsetY * directionY + \
                       offsetZ * directionZ
            if distance <= 0.0 or distance > 64.0 or distance >= targetDistance:
                continue

            nearestX = originX + directionX * distance
            nearestY = originY + directionY * distance
            nearestZ = originZ + directionZ * distance
            missX = entity.posX - nearestX
            missY = entity.posY + entity.height * 0.5 - nearestY
            missZ = entity.posZ - nearestZ
            hitRadius = entity.width * 0.5 + 6.0
            if missX * missX + missY * missY + missZ * missZ <= \
               hitRadius * hitRadius:
                target = entity
                targetDistance = distance

        if target:
            x, y, z = target.posX, target.posY, target.posZ
        else:
            x = originX + directionX * 24.0
            y = originY + directionY * 24.0
            z = originZ + directionZ * 24.0

        world.tsarBombs.append(TsarBomba(world, x, y, z))
        stack.stackSize -= 1
        return stack
