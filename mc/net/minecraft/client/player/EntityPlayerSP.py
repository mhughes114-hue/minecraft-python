from mc.net.minecraft.client.effect.EntityPickupFX import EntityPickupFX
from mc.net.minecraft.client.gui.container.GuiCrafting import GuiCrafting
from mc.net.minecraft.client.gui.container.GuiFurnace import GuiFurnace
from mc.net.minecraft.client.gui.container.GuiChest import GuiChest
from mc.net.minecraft.game.entity.player.EntityPlayer import EntityPlayer
from mc.net.minecraft.game.item.ItemStack import ItemStack
from nbtlib.tag import Compound, List, Byte, Int

class EntityPlayerSP(EntityPlayer):

    def __init__(self, mc, world, session):
        super().__init__(world)
        self.__mc = mc
        self.movementInput = None
        if session:
            self.skinUrl = f'https://api.mojang.com/users/profiles/minecraft/{session.username}'

    def _updatePlayerActionState(self):
        self._moveStrafing = self.movementInput.moveStrafe
        self._moveForward = self.movementInput.moveForward
        flying = self.__mc.playerController.isInTestMode
        self._isCreativeFlying = flying and not self.onGround
        self._isSprinting = self.movementInput.sprint and self._moveForward > 0.0 and \
                            not self.movementInput.sneak and not flying
        if self._isCreativeFlying:
            self._creativeFlightMultiplier = self.__mc.options.creativeFlightMultiplier

        self._isJumping = self.movementInput.jump and not flying

    def onLivingUpdate(self):
        self.movementInput.updatePlayerMoveState()
        flying = self.__mc.playerController.isInTestMode
        if flying:
            if self.movementInput.jump:
                self.motionY = 0.42
            elif self.movementInput.sneak:
                self.motionY = -0.42
            else:
                self.motionY = 0.0

        super().onLivingUpdate()
        if flying:
            self.motionY = 0.0

    def _writeEntityToNBT(self, compound):
        super()._writeEntityToNBT(compound)
        compound['Score'] = Int(self._getScore)
        invList = List[Compound]()
        for slot in range(len(self.inventory.mainInventory)):
            if self.inventory.mainInventory[slot]:
                comp = Compound({'Slot': Byte(slot)})
                self.inventory.mainInventory[slot].writeToNBT(comp)
                invList.append(comp)
        for slot in range(len(self.inventory.armorInventory)):
            if self.inventory.armorInventory[slot]:
                comp = Compound({'Slot': Byte(slot + 100)})
                self.inventory.armorInventory[slot].writeToNBT(comp)
                invList.append(comp)

        compound['Inventory'] = invList

    def _readEntityFromNBT(self, compound):
        super()._readEntityFromNBT(compound)
        self._getScore = compound.get('Score', Int(0)).real
        invList = compound.get('Inventory', List[Compound]())
        self.inventory.mainInventory = [None] * 36
        self.inventory.armorInventory = [None] * 4
        for comp in invList:
            slot = comp.get('Slot', Byte(0)).real & 255
            if slot >= 0 and slot < len(self.inventory.mainInventory):
                self.inventory.mainInventory[slot] = ItemStack(comp)
            if slot >= 100 and slot < len(self.inventory.armorInventory) + 100:
                self.inventory.armorInventory[slot - 100] = ItemStack(comp)

    def _getEntityString(self):
        return 'LocalPlayer'

    def displayGUIChest(self, inventory):
        self.__mc.displayGuiScreen(GuiChest(self.inventory, inventory))

    def displayWorkbenchGUI(self):
        self.__mc.displayGuiScreen(GuiCrafting(self.inventory))

    def displayGUIFurnace(self, furnaceInventory):
        self.__mc.displayGuiScreen(GuiFurnace(self.inventory, furnaceInventory))

    def destroyCurrentEquippedItem(self):
        self.inventory.setInventorySlotContents(self.inventory.currentItem, None)

    def onItemPickup(self, item):
        self.__mc.effectRenderer.addEffect(EntityPickupFX(self.__mc.theWorld, item,
                                                          self, -0.5))
