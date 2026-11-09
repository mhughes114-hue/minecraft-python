from mc.net.minecraft.game.Inventory import Inventory
from mc.net.minecraft.game.level.block.tileentity.TileEntity import TileEntity
from mc.net.minecraft.game.item.ItemStack import ItemStack
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.item.Items import items

from nbtlib.tag import Compound, String, Byte, List


class TileEntityTsarBomba(TileEntity, Inventory):
    REQUIREMENTS = (
        (blocks.tnt.blockID, 1),
        (items.gunpowder.shiftedIndex, 8),
        (items.diamond.shiftedIndex, 1),
    )

    def __init__(self):
        super().__init__()
        self.__itemStacks = [None] * len(self.REQUIREMENTS)
        self.detonated = False

    def getSizeInventory(self):
        return len(self.__itemStacks)

    def getStackInSlot(self, slot):
        return self.__itemStacks[slot]

    def decrStackSize(self, slot, size):
        stack = self.__itemStacks[slot]
        if not stack:
            return None
        if stack.stackSize <= size:
            self.__itemStacks[slot] = None
            return stack
        result = stack.splitStack(size)
        if stack.stackSize == 0:
            self.__itemStacks[slot] = None
        return result

    def setInventorySlotContents(self, slot, stack):
        self.__itemStacks[slot] = stack
        if stack:
            stack.stackSize = min(stack.stackSize, self.getInventoryStackLimit())

    def getInvName(self):
        return 'Tsar Bomba'

    def getInventoryStackLimit(self):
        return Inventory.STACK_LIMIT

    def readFromNBT(self, compound):
        super().readFromNBT(compound)
        self.__itemStacks = [None] * len(self.REQUIREMENTS)
        for tag in compound.get('Items', List[Compound]()):
            slot = tag.get('Slot', Byte(0)).real & 255
            if slot < len(self.__itemStacks):
                self.__itemStacks[slot] = ItemStack(tag)

    def writeToNBT(self, compound):
        super().writeToNBT(compound)
        compound['id'] = String('TsarBomba')
        tagList = List[Compound]()
        for slot, stack in enumerate(self.__itemStacks):
            if stack:
                tag = Compound({'Slot': Byte(slot)})
                stack.writeToNBT(tag)
                tagList.append(tag)
        compound['Items'] = tagList

    def hasRequiredItems(self):
        for slot, (itemId, amount) in enumerate(self.REQUIREMENTS):
            stack = self.__itemStacks[slot]
            if not stack or stack.itemID != itemId or stack.stackSize < amount:
                return False
        return True

    def isPowered(self):
        x, y, z = self.xCoord, self.yCoord, self.zCoord
        return any(
            self.worldObj.getBlockId(x + dx, y + dy, z + dz) ==
            blocks.redstoneTorch.blockID
            for dx, dy, dz in (
                (1, 0, 0), (-1, 0, 0), (0, 1, 0),
                (0, -1, 0), (0, 0, 1), (0, 0, -1),
            )
        )

    def updateEntity(self):
        if self.detonated or not self.hasRequiredItems() or not self.isPowered():
            return

        self.detonated = True
        for slot, (_, amount) in enumerate(self.REQUIREMENTS):
            self.decrStackSize(slot, amount)

        from mc.net.minecraft.game.level.TsarBomba import TsarBomba
        world = self.worldObj
        x, y, z = self.xCoord, self.yCoord, self.zCoord
        world.setBlockWithNotify(x, y, z, 0)
        world.tsarBombs.append(TsarBomba(world, x + 0.5, y + 0.5, z + 0.5))
