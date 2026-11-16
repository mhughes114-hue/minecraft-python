from mc.net.minecraft.game.entity.monster.FactionVehicle import FactionVehicle


class EntityVillagerMLRS(FactionVehicle):

    def __init__(self, world):
        super().__init__(world, 'villager', 'mlrs')

    def _getEntityString(self):
        return 'VillagerMLRS'
