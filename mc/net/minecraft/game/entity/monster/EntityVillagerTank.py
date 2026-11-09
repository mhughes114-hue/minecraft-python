from mc.net.minecraft.game.entity.monster.FactionVehicle import FactionVehicle


class EntityVillagerTank(FactionVehicle):

    def __init__(self, world):
        super().__init__(world, 'villager', 'tank')

    def _getEntityString(self):
        return 'VillagerTank'
