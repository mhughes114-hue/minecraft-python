from mc.net.minecraft.game.level.block.BlockContainer import BlockContainer
from mc.net.minecraft.game.level.material.Material import Material


class BlockTsarBomba(BlockContainer):

    def __init__(self, blocks, blockId):
        super().__init__(blocks, blockId, Material.rock)
        self.blockIndexInTexture = 8

    def getBlockTextureFromSide(self, face):
        if face == 1:
            return self.blockIndexInTexture + 1
        if face == 0:
            return self.blockIndexInTexture + 2
        return self.blockIndexInTexture

    def blockActivated(self, world, x, y, z, player):
        player.displayGUITsarBomba(world.getBlockTileEntity(x, y, z))
        return True

    def _getBlockEntity(self):
        from mc.net.minecraft.game.level.block.tileentity.TileEntityTsarBomba import TileEntityTsarBomba
        return TileEntityTsarBomba()
