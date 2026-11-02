from mc.net.minecraft.game.entity.monster.EntityGiantZombie import EntityGiantZombie


class EntityWitherStorm(EntityGiantZombie):

    def __init__(self, world):
        super().__init__(world)
        self._texture = 'mob/witherstorm.png'
        self.health = 600
        self._attackStrength = 12

    def onLivingUpdate(self):
        super().onLivingUpdate()
        if self.isDead or self.health <= 0 or self.ticksExisted % 100:
            return

        player = self._worldObj.getPlayerEntity()
        if not player:
            return

        x = player.posX - self.posX
        y = player.posY - self.posY
        z = player.posZ - self.posZ
        if x * x + y * y + z * z <= 1024.0:
            self._worldObj.createExplosion(
                self, player.posX, player.posY, player.posZ, 3.0
            )

    def _getEntityString(self):
        return 'WitherStorm'
