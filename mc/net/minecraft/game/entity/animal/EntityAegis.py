from mc.net.minecraft.game.entity.animal.EntityAnimal import EntityAnimal

class EntityAegis(EntityAnimal):

    def __init__(self, world):
        super().__init__(world)
        self._texture = 'mob/aegis.png'
        self.setSize(0.9, 1.4)
        self._moveSpeed = 0.6

    def _getEntityString(self):
        return 'Aegis'
