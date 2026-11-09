from mc.net.minecraft.game.entity.monster.FactionVehicle import FactionVehicle


class EntityVillagerAircraft(FactionVehicle):

    def __init__(self, world):
        super().__init__(world, 'villager', 'aircraft')

    def _getEntityString(self):
        return 'VillagerAircraft'
