from mc.net.minecraft.game.entity.monster.EntityMob import EntityMob

import math

class EntityVentoraptor(EntityMob):

    def __init__(self, world):
        super().__init__(world)
        self._texture = 'mob/ventoraptor.png'
        self.setSize(1.0, 1.3)
        self._moveSpeed = 1.1
        self._attackStrength = 3

    def _attackEntity(self, entity, distance):
        if 2.0 < distance < 6.0 and self._rand.nextInt(10) == 0 and self.onGround:
            xd = entity.posX - self.posX
            zd = entity.posZ - self.posZ
            d = math.sqrt(xd * xd + zd * zd)
            if d > 0.0:
                self.motionX = xd / d * 0.55 + self.motionX * 0.2
                self.motionZ = zd / d * 0.55 + self.motionZ * 0.2
                self.motionY = 0.4
                return

        super()._attackEntity(entity, distance)

    def _getEntityString(self):
        return 'Ventoraptor'
