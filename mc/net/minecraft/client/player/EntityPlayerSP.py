from mc.net.minecraft.client.effect.EntityPickupFX import EntityPickupFX
from mc.net.minecraft.client.gui.container.GuiCrafting import GuiCrafting
from mc.net.minecraft.client.gui.container.GuiFurnace import GuiFurnace
from mc.net.minecraft.client.gui.container.GuiChest import GuiChest
from mc.net.minecraft.client.gui.container.GuiTsarBomba import GuiTsarBomba
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

    def _hasSneakSupport(self, x, z):
        box = self.boundingBox.cloneMove(x, -1.0, z)
        return bool(self._worldObj.getCollidingBoundingBoxes(box))

    def _getSneakSafeMovement(self, x, z):
        while x != 0.0 and not self._hasSneakSupport(x, 0.0):
            x = 0.0 if abs(x) < 0.05 else x - (0.05 if x > 0.0 else -0.05)

        while z != 0.0 and not self._hasSneakSupport(0.0, z):
            z = 0.0 if abs(z) < 0.05 else z - (0.05 if z > 0.0 else -0.05)

        while x != 0.0 and z != 0.0 and not self._hasSneakSupport(x, z):
            x = 0.0 if abs(x) < 0.05 else x - (0.05 if x > 0.0 else -0.05)
            z = 0.0 if abs(z) < 0.05 else z - (0.05 if z > 0.0 else -0.05)

        return x, z

    def moveEntity(self, x, y, z):
        if self.onGround and self.movementInput and self.movementInput.sneak and \
           not self.__mc.playerController.isInTestMode:
            x, z = self._getSneakSafeMovement(x, z)

        super().moveEntity(x, y, z)

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

    def displayGUITsarBomba(self, inventory):
        self.__mc.displayGuiScreen(GuiTsarBomba(self.inventory, inventory))

    def destroyCurrentEquippedItem(self):
        self.inventory.setInventorySlotContents(self.inventory.currentItem, None)

    def onItemPickup(self, item):
        self.__mc.effectRenderer.addEffect(EntityPickupFX(self.__mc.theWorld, item,
                                                          self, -0.5))
