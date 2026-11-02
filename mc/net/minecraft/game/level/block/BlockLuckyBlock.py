from mc.net.minecraft.game.level.block.Block import Block
from mc.net.minecraft.game.level.material.Material import Material


class BlockLuckyBlock(Block):

    def __init__(self, blocks, blockId, tex):
        super().__init__(blocks, blockId, tex, Material.rock)

    def getBlockTextureFromSide(self, face):
        if face == 0:
            return self.blockIndexInTexture + 2
        if face == 1:
            return self.blockIndexInTexture + 1
        return self.blockIndexInTexture

    def idDropped(self, metadata, random):
        return 0

    def __spawnHostileMob(self, world, x, y, z):
        from mc.net.minecraft.game.entity.monster.EntityChupacabra import EntityChupacabra
        from mc.net.minecraft.game.entity.monster.EntityCinder import EntityCinder
        from mc.net.minecraft.game.entity.monster.EntityVentoraptor import EntityVentoraptor

        mobs = (EntityCinder, EntityChupacabra, EntityVentoraptor)
        mob = mobs[world.rand.nextInt(len(mobs))](world)
        mob.setPositionAndRotation(
            x + 0.5, y, z + 0.5, world.rand.nextFloat() * 360.0, 0.0
        )
        world.spawnEntityInWorld(mob)

    def onBlockDestroyedByPlayer(self, world, x, y, z, metadata):
        from mc.net.minecraft.game.entity.misc.EntityItem import EntityItem
        from mc.net.minecraft.game.item.ItemStack import ItemStack
        from mc.net.minecraft.game.item.Items import items

        outcome = world.rand.nextInt(10)
        if outcome < 6:
            rewards = (
                (items.coal.shiftedIndex, 4),
                (items.ingotIron.shiftedIndex, 2),
                (items.ingotGold.shiftedIndex, 2),
                (items.diamond.shiftedIndex, 1),
                (items.bread.shiftedIndex, 3),
                (items.porkCooked.shiftedIndex, 2),
                (items.arrow.shiftedIndex, 8),
                (items.swordSteel.shiftedIndex, 1),
                (self.blocks.blockGold.blockID, 2),
                (self.blocks.blockDiamond.blockID, 1),
            )
            itemId, amount = rewards[world.rand.nextInt(len(rewards))]
            entity = EntityItem(
                world, x + 0.5, y + 0.5, z + 0.5, ItemStack(itemId, amount)
            )
            entity.delayBeforeCanPickup = 10
            world.spawnEntityInWorld(entity)
        elif outcome < 8:
            self.__spawnHostileMob(world, x, y, z)
        else:
            world.createExplosion(None, x + 0.5, y + 0.5, z + 0.5, 3.0)
