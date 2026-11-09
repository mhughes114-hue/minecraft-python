from mc.net.minecraft.client.gui.container.GuiContainer import GuiContainer
from mc.net.minecraft.client.gui.container.Slot import Slot
from mc.net.minecraft.client.render.RenderEngine import RenderEngine
from mc.net.minecraft.game.item.Items import items
from pyglet import gl


class TsarBombaSlot(Slot):

    def __init__(self, gui, inventory, slot, x, y, itemId):
        super().__init__(gui, inventory, slot, x, y)
        self.itemId = itemId

    def isItemValid(self, stack):
        return stack is not None and stack.itemID == self.itemId

    def getBackgroundIconIndex(self):
        return items.itemsList[self.itemId].getIconIndex()


class GuiTsarBomba(GuiContainer):

    def __init__(self, playerInventory, bombaInventory):
        super().__init__()
        self.__bombaInventory = bombaInventory
        for slot, (itemId, _) in enumerate(bombaInventory.REQUIREMENTS):
            x = 20 + slot * 54
            self._inventorySlots.append(
                TsarBombaSlot(self, bombaInventory, slot, x, 34, itemId)
            )
        for row in range(3):
            for col in range(9):
                self._inventorySlots.append(Slot(
                    self, playerInventory, col + (row + 1) * 9,
                    8 + col * 18, 84 + row * 18
                ))
        for col in range(9):
            self._inventorySlots.append(Slot(
                self, playerInventory, col, 8 + col * 18, 142
            ))

    def _drawGuiContainerForegroundLayer(self):
        self._fontRenderer.drawString('Tsar Bomba', 8, 6, 4210752)
        self._fontRenderer.drawString('1 TNT', 20, 54, 4210752)
        self._fontRenderer.drawString('8 Gunpowder', 66, 54, 4210752)
        self._fontRenderer.drawString('1 Diamond', 126, 54, 4210752)
        if self.__bombaInventory.hasRequiredItems():
            status = 'Ready for redstone' if not \
                     self.__bombaInventory.isPowered() else 'Detonating'
            color = 4210752
        else:
            status = 'Fill all required slots'
            color = 0xAA0000
        self._fontRenderer.drawString(status, 8, 70, color)
        self._fontRenderer.drawString('Inventory', 8, self.ySize - 96 + 2, 4210752)

    def _drawGuiContainerBackgroundLayer(self):
        texture = self.mc.renderEngine.getTexture('gui/container.png')
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        RenderEngine.bindTexture(texture)
        x = (self.width - self.xSize) // 2
        y = (self.height - self.ySize) // 2
        self.drawTexturedModalRect(x, y, 0, 0, self.xSize, self.ySize)
