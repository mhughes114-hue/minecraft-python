from mc.net.minecraft.game.entity.monster.FactionVehicle import FactionVehicle


class EntityPillagerAircraft(FactionVehicle):

    def __init__(self, world):
        super().__init__(world, 'pillager', 'aircraft')

    def _getEntityString(self):
        return 'PillagerAircraft'
