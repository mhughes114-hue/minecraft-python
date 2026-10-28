from mc.net.minecraft.game.entity.monster.EntityMob import EntityMob

class EntityChupacabra(EntityMob):

    def __init__(self, world):
        super().__init__(world)
        self._texture = 'mob/chupacabra.png'
        self.setSize(0.9, 1.0)
        self._moveSpeed = 1.0
        self._attackStrength = 4

    def _getEntityString(self):
        return 'Chupacabra'
