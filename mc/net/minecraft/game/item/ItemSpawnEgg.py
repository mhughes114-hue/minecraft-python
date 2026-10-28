from mc.net.minecraft.game.item.Item import Item

import math


class ItemSpawnEgg(Item):
    isSpawnEgg = True

    def __init__(self, items, itemId):
        super().__init__(items, itemId)
        self.setIconIndex(37)

    def onItemRightClick(self, stack, world, player):
        if not world or not player:
            return stack

        from mc.net.minecraft.game.level.MobSpawner import SPAWN_EGG_ENTITIES

        damage = stack.itemDamage
        if damage < 0 or damage >= len(SPAWN_EGG_ENTITIES):
            return stack

        _, entityClass = SPAWN_EGG_ENTITIES[damage]
        entity = entityClass(world)
        yaw = player.rotationYaw
        radians = math.radians(yaw)
        x = player.posX - math.sin(radians) * 2.0
        y = player.posY - player.yOffset
        z = player.posZ + math.cos(radians) * 2.0
        entity.setPositionAndRotation(x, y, z, yaw, 0.0)
        world.spawnEntityInWorld(entity)
        stack.stackSize -= 1
        return stack
