from mc.net.minecraft.game.entity.EntityLiving import EntityLiving
from mc.net.minecraft.game.entity.animal.EntityAegis import EntityAegis
from mc.net.minecraft.game.entity.animal.EntityAnimal import EntityAnimal
from mc.net.minecraft.game.entity.animal.EntityPig import EntityPig
from mc.net.minecraft.game.entity.animal.EntitySheep import EntitySheep
from mc.net.minecraft.game.entity.animal.EntityVillager import EntityVillager
from mc.net.minecraft.game.entity.monster.EntityChupacabra import EntityChupacabra
from mc.net.minecraft.game.entity.monster.EntityCinder import EntityCinder
from mc.net.minecraft.game.entity.monster.EntityCreeper import EntityCreeper
from mc.net.minecraft.game.entity.monster.EntityGiantZombie import EntityGiantZombie
from mc.net.minecraft.game.entity.monster.EntitySkeleton import EntitySkeleton
from mc.net.minecraft.game.entity.monster.EntitySpider import EntitySpider
from mc.net.minecraft.game.entity.monster.EntityVentoraptor import EntityVentoraptor
from mc.net.minecraft.game.entity.monster.EntityWitherStorm import EntityWitherStorm
from mc.net.minecraft.game.entity.monster.EntityZombie import EntityZombie
from mc.net.minecraft.game.entity.monster.EntityPillager import EntityPillager
from mc.net.minecraft.game.entity.monster.EntityPillagerAircraft import EntityPillagerAircraft
from mc.net.minecraft.game.entity.monster.EntityPillagerTank import EntityPillagerTank
from mc.net.minecraft.game.entity.monster.EntityVillagerAircraft import EntityVillagerAircraft
from mc.net.minecraft.game.entity.monster.EntityVillagerTank import EntityVillagerTank
from mc.net.minecraft.game.entity.monster.EntityMob import EntityMob
from mc.JavaUtils import random

SPAWN_EGG_ENTITIES = (
    ('Pig', EntityPig),
    ('Sheep', EntitySheep),
    ('Villager', EntityVillager),
    ('Aegis', EntityAegis),
    ('Pillager', EntityPillager),
    ('Villager Tank', EntityVillagerTank),
    ('Pillager Tank', EntityPillagerTank),
    ('Villager Aircraft', EntityVillagerAircraft),
    ('Pillager Aircraft', EntityPillagerAircraft),
    ('Zombie', EntityZombie),
    ('Skeleton', EntitySkeleton),
    ('Creeper', EntityCreeper),
    ('Spider', EntitySpider),
    ('Cinder', EntityCinder),
    ('Chupacabra', EntityChupacabra),
    ('Ventoraptor', EntityVentoraptor),
    ('Wither Storm', EntityWitherStorm),
)

ENTITY_TYPES = {
    name.lower(): entityClass
    for name, entityClass in SPAWN_EGG_ENTITIES
}
ENTITY_TYPES['giant'] = EntityGiantZombie
ENTITY_TYPES['giantzombie'] = EntityGiantZombie
ENTITY_TYPES['witherstorm'] = EntityWitherStorm
ENTITY_TYPES['villagers'] = EntityVillager
ENTITY_TYPES['pillagers'] = EntityPillager
ENTITY_TYPES.update({
    'villagertank': EntityVillagerTank,
    'pillagertank': EntityPillagerTank,
    'villageraircraft': EntityVillagerAircraft,
    'pillageraircraft': EntityPillagerAircraft,
    'villagerplane': EntityVillagerAircraft,
    'pillagerplane': EntityPillagerAircraft,
})


class MobSpawner:

    def __init__(self, world):
        self.__worldObj = world

    def performSpawning(self):
        mobSize = self.__worldObj.width * self.__worldObj.length * \
               self.__worldObj.height * 20 // 64 // 64 // 64
        mobSize = mobSize * 2
        if self.__worldObj.difficultySetting == 0:
            mobSize = 0 // 4
        elif self.__worldObj.difficultySetting == 1:
            mobSize = mobSize * 3 // 4
        elif self.__worldObj.difficultySetting == 2:
            mobSize = (mobSize << 2) // 4
        elif self.__worldObj.difficultySetting == 3:
            mobSize = mobSize * 6 // 4

        animalSize = self.__worldObj.width * self.__worldObj.length * 3 // 4000
        totalMobs = self.__worldObj.entitiesInLevelList(EntityMob)
        for i in range(8):
            if totalMobs >= mobSize:
                break

            mobs = 0
            choice = self.__worldObj.rand.nextInt(14)
            blockX = self.__worldObj.rand.nextInt(self.__worldObj.width)
            blockY = int(min(self.__worldObj.rand.nextFloat(),
                             self.__worldObj.rand.nextFloat()) * self.__worldObj.height)
            blockZ = self.__worldObj.rand.nextInt(self.__worldObj.length)
            for j in range(3):
                xx = blockX
                yy = blockY
                zz = blockZ
                for k in range(3):
                    xx += self.__worldObj.rand.nextInt(6) - self.__worldObj.rand.nextInt(6)
                    yy += self.__worldObj.rand.nextInt(1) - self.__worldObj.rand.nextInt(1)
                    zz += self.__worldObj.rand.nextInt(6) - self.__worldObj.rand.nextInt(6)
                    if xx >= 0 and zz > 0 and yy >= 0 and \
                       yy < self.__worldObj.height - 2 and \
                       xx < self.__worldObj.width and zz < self.__worldObj.length:
                        x = xx + 0.5
                        y = yy + 0.5
                        z = zz + 0.5
                        if self.__worldObj.playerEntity:
                            xd = x - self.__worldObj.playerEntity.posX
                            yd = y - self.__worldObj.playerEntity.posY
                            zd = z - self.__worldObj.playerEntity.posZ
                        else:
                            xd = x - self.__worldObj.xSpawn
                            yd = y - self.__worldObj.ySpawn
                            zd = z - self.__worldObj.zSpawn

                        if xd * xd + yd * yd + zd * zd < 1024.0:
                            continue

                        mob = None
                        if choice == 0:
                            mob = EntitySkeleton(self.__worldObj)
                        elif choice == 1:
                            mob = EntityCreeper(self.__worldObj)
                        elif choice == 2:
                            mob = EntitySpider(self.__worldObj)
                        elif choice == 3:
                            mob = EntityZombie(self.__worldObj)
                        elif choice == 4:
                            mob = EntityCinder(self.__worldObj)
                        elif choice == 5:
                            mob = EntityChupacabra(self.__worldObj)
                        elif choice == 6:
                            mob = EntityVentoraptor(self.__worldObj)
                        elif choice in (7, 8, 13):
                            mob = EntityPillager(self.__worldObj)
                        elif choice == 9:
                            mob = EntityVillagerTank(self.__worldObj)
                        elif choice == 10:
                            mob = EntityPillagerTank(self.__worldObj)
                        elif choice == 11:
                            mob = EntityVillagerAircraft(self.__worldObj)
                        elif choice == 12:
                            mob = EntityPillagerAircraft(self.__worldObj)

                        if isinstance(mob, EntityMob) and self.__worldObj.difficultySetting == 0:
                            mob = None

                        if not mob or self.__worldObj.isBlockNormalCube(xx, yy, zz) or \
                           not self.__worldObj.isBlockNormalCube(xx, yy - 1, zz) or \
                           not mob.getCanSpawnHere(x, y, z):
                            continue

                        yaw = self.__worldObj.rand.nextFloat() * 360.0
                        mob.setPositionAndRotation(x, y, z, yaw, 0.0)
                        mobs += 1
                        self.__worldObj.spawnEntityInWorld(mob)

            totalMobs += mobs

        totalAnimals = self.__worldObj.entitiesInLevelList(EntityAnimal)
        for i in range(6):
            if totalAnimals >= animalSize:
                break

            animals = 0
            choice = self.__worldObj.rand.nextInt(7)
            blockX = self.__worldObj.rand.nextInt(self.__worldObj.width)
            blockY = self.__worldObj.rand.nextInt(self.__worldObj.height)
            blockZ = self.__worldObj.rand.nextInt(self.__worldObj.length)
            for j in range(5):
                xx = blockX
                yy = blockY
                zz = blockZ
                for k in range(3):
                    xx += self.__worldObj.rand.nextInt(6) - self.__worldObj.rand.nextInt(6)
                    yy += self.__worldObj.rand.nextInt(1) - self.__worldObj.rand.nextInt(1)
                    zz += self.__worldObj.rand.nextInt(6) - self.__worldObj.rand.nextInt(6)
                    if xx >= 0 and zz > 0 and yy >= 0 and \
                       yy < self.__worldObj.height - 2 and \
                       xx < self.__worldObj.width and zz < self.__worldObj.length:
                        x = xx + 0.5
                        y = yy + 0.5
                        z = zz + 0.5
                        if self.__worldObj.playerEntity:
                            xd = x - self.__worldObj.playerEntity.posX
                            yd = y - self.__worldObj.playerEntity.posY
                            zd = z - self.__worldObj.playerEntity.posZ
                        else:
                            xd = x - self.__worldObj.xSpawn
                            yd = y - self.__worldObj.ySpawn
                            zd = z - self.__worldObj.zSpawn

                        if xd * xd + yd * yd + zd * zd < 1024.0:
                            continue

                        animal = None
                        if choice == 0:
                            animal = EntityPig(self.__worldObj)
                        elif choice == 1:
                            animal = EntitySheep(self.__worldObj)
                        elif choice == 2:
                            animal = EntityAegis(self.__worldObj)
                        elif choice in (3, 4):
                            animal = EntityVillager(self.__worldObj)

                        if not animal or self.__worldObj.isBlockNormalCube(xx, yy, zz) or \
                           not self.__worldObj.isBlockNormalCube(xx, yy - 1, zz) or \
                           not animal.getCanSpawnHere(x, y, z):
                            continue

                        yaw = self.__worldObj.rand.nextFloat() * 360.0
                        animal.setPositionAndRotation(x, y, z, yaw, 0.0)
                        animals += 1
                        self.__worldObj.spawnEntityInWorld(animal)

            totalAnimals += animals
