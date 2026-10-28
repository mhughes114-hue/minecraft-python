from mc.net.minecraft.client.Session import Session
from mc.net.minecraft.client.controller.PlayerController import PlayerController
from mc.net.minecraft.game.level.MobSpawner import MobSpawner
from mc.net.minecraft.game.level.block.Blocks import blocks
from mc.net.minecraft.game.item.ItemStack import ItemStack

class PlayerControllerCreative(PlayerController):

    def __init__(self, mc):
        super().__init__(mc)
        self.isInTestMode = True

    def onRespawn(self, player):
        for i, block in enumerate(Session.registeredBlocksList):
            if i >= len(player.inventory.mainInventory):
                break

            player.inventory.mainInventory[i] = ItemStack(
                blocks.blocksList[block.blockID], 64
            )

    def shouldDrawHUD(self):
        return False

    def onWorldChange(self, world):
        super().onWorldChange(world)
        world.survivalWorld = False
        self.__mobSpawner = MobSpawner(world)

    def onUpdate(self):
        self.__mobSpawner.performSpawning()
