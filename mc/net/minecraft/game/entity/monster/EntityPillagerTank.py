from mc.net.minecraft.game.entity.monster.FactionVehicle import FactionVehicle


class EntityPillagerTank(FactionVehicle):

    def __init__(self, world):
        super().__init__(world, 'pillager', 'tank')

    def _getEntityString(self):
        return 'PillagerTank'
