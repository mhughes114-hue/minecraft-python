from mc.net.minecraft.game.entity.FactionAI import (
    breakObstructingBlock,
    findFactionTarget,
)
from mc.net.minecraft.game.entity.animal.EntityAnimal import EntityAnimal


class EntityVillager(EntityAnimal):

    def __init__(self, world):
        super().__init__(world)
        self._texture = 'char.png'
        self._moveSpeed = 0.65
        self._attackStrength = 3

    def onLivingUpdate(self):
        super().onLivingUpdate()
        if self.ticksExisted % 40 == 0:
            breakObstructingBlock(self, self._playerToAttack)

    def _findPlayerToAttack(self):
        from mc.net.minecraft.game.entity.monster.EntityPillager import EntityPillager

        return findFactionTarget(self, EntityPillager)

    def _attackEntity(self, entity, distance):
        if self.attackTime == 0 and distance < 2.5 and \
           entity.boundingBox.maxY > self.boundingBox.minY and \
           entity.boundingBox.minY < self.boundingBox.maxY:
            self.attackTime = 20
            entity.attackEntityFrom(self, self._attackStrength)
            self._hasAttacked = True

    def _getEntityString(self):
        return 'Villager'
