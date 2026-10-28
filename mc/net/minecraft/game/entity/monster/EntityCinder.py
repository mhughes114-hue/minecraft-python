from mc.net.minecraft.game.entity.monster.EntityMob import EntityMob

class EntityCinder(EntityMob):

    def __init__(self, world):
        super().__init__(world)
        self._texture = 'mob/cinder.png'
        self.setSize(0.8, 1.2)
        self._moveSpeed = 0.9
        self._attackStrength = 3

    def _attackEntity(self, entity, distance):
        if self.attackTime == 0 and distance < 2.5:
            super()._attackEntity(entity, distance)
            if self.attackTime > 0:
                entity.fire = max(entity.fire, 60)

    def _getEntityString(self):
        return 'Cinder'
