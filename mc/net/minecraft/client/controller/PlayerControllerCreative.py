from mc.net.minecraft.client.controller.PlayerController import PlayerController
from mc.net.minecraft.game.level.MobSpawner import MobSpawner

class PlayerControllerCreative(PlayerController):

    def __init__(self, mc):
        super().__init__(mc)
        self.isInTestMode = True

    def onRespawn(self, player):
        player.inventory.mainInventory = [None] * len(player.inventory.mainInventory)
        player.inventory.armorInventory = [None] * len(player.inventory.armorInventory)

    def shouldDrawHUD(self):
        return False

    def onWorldChange(self, world):
        super().onWorldChange(world)
        world.survivalWorld = False
        self.__mobSpawner = MobSpawner(world)

    def onUpdate(self):
        self.__mobSpawner.performSpawning()
