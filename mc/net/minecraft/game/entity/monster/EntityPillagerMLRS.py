from mc.net.minecraft.game.entity.monster.FactionVehicle import FactionVehicle


class EntityPillagerMLRS(FactionVehicle):

    def __init__(self, world):
        super().__init__(world, 'pillager', 'mlrs')

    def _getEntityString(self):
        return 'PillagerMLRS'
