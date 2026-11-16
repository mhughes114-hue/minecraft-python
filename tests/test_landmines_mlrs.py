from importlib import import_module
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

import_module('mc.net.minecraft.client.Minecraft')
EntityLandmine = import_module(
    'mc.net.minecraft.game.entity.misc.EntityLandmine'
).EntityLandmine
EntityLiving = import_module(
    'mc.net.minecraft.game.entity.EntityLiving'
).EntityLiving
EntityClusterShell = import_module(
    'mc.net.minecraft.game.entity.projectile.EntityClusterShell'
).EntityClusterShell
FactionVehicle = import_module(
    'mc.net.minecraft.game.entity.monster.FactionVehicle'
).FactionVehicle
World = import_module('mc.net.minecraft.game.level.World').World
blocks = import_module('mc.net.minecraft.game.level.block.Blocks').blocks


class LandmineMLRSTests(unittest.TestCase):
    def make_world(self):
        world = World()
        world.generate(32, 16, 32, bytearray(32 * 16 * 32), None)
        return world

    def test_landmine_detonates_for_a_nearby_living_entity(self):
        world = self.make_world()
        mine = EntityLandmine(world)
        mine.setPosition(8.5, 4.12, 8.5)
        world.spawnEntityInWorld(mine)
        target = EntityLiving(world)
        target.setPosition(9.5, 4.12, 8.5)
        world.spawnEntityInWorld(target)

        mine._checkForDetonation()

        self.assertTrue(mine.isDead)

    def test_landmine_stays_armed_when_no_living_entity_is_close(self):
        world = self.make_world()
        mine = EntityLandmine(world)
        mine.setPosition(8.5, 4.12, 8.5)
        world.spawnEntityInWorld(mine)
        target = EntityLiving(world)
        target.setPosition(12.0, 4.12, 8.5)
        world.spawnEntityInWorld(target)

        mine._checkForDetonation()

        self.assertFalse(mine.isDead)

    def test_explosion_damage_at_source_position_does_not_divide_by_zero(self):
        world = self.make_world()
        world.survivalWorld = True
        target = EntityLiving(world)
        source = EntityLiving(world)
        target.setPosition(8.5, 4.0, 8.5)
        source.setPosition(8.5, 4.0, 8.5)

        self.assertTrue(target.attackEntityFrom(source, 1))
        self.assertEqual(target.health, 9)

    def test_knockback_handles_distances_that_underflow_when_squared(self):
        world = self.make_world()
        world.survivalWorld = True
        target = EntityLiving(world)
        source = EntityLiving(world)
        target.setPosition(8.5, 4.0, 8.5)
        source.setPosition(8.5 + 1e-30, 4.0, 8.5 + 1e-30)

        self.assertTrue(target.attackEntityFrom(source, 1))

    def test_knockback_handles_axis_aligned_attacker_positions(self):
        world = self.make_world()
        world.survivalWorld = True
        target = EntityLiving(world)
        source = EntityLiving(world)
        target.setPosition(8.5, 4.0, 8.5)
        source.setPosition(8.5, 4.0, 9.5)

        self.assertTrue(target.attackEntityFrom(source, 1))
        self.assertAlmostEqual(target.motionX, 0.0)
        self.assertAlmostEqual(target.motionZ, -0.4)

    def test_mlrs_launches_a_cluster_shell_at_the_enemy_position(self):
        target = SimpleNamespace(posX=32.5, posZ=48.5)
        shell = Mock()
        world = SimpleNamespace(spawnEntityInWorld=Mock())
        launcher = SimpleNamespace(
            _worldObj=world,
            posX=8.5,
            posY=5.0,
            posZ=12.5,
            height=1.8,
            MLRS_COOLDOWN=FactionVehicle.MLRS_COOLDOWN,
            _mlrsCooldown=0,
            _hasAttacked=False,
            rotationYaw=0.0,
        )

        with patch(
            'mc.net.minecraft.game.entity.projectile.EntityClusterShell.EntityClusterShell',
            return_value=shell,
        ) as create_shell:
            FactionVehicle._fireMLRS(launcher, target)

        create_shell.assert_called_once_with(world, launcher, 32.5, 48.5)
        shell.setLaunchPosition.assert_called_once_with(8.5, 5.9, 12.5)
        world.spawnEntityInWorld.assert_called_once_with(shell)
        self.assertEqual(launcher._mlrsCooldown, FactionVehicle.MLRS_COOLDOWN)
        self.assertTrue(launcher._hasAttacked)

    def test_cluster_shell_uses_target_surface_and_longer_flight_for_range(self):
        world = self.make_world()
        for x in range(world.width):
            for z in range(world.length):
                world.setBlock(x, 4, z, blocks.stone.blockID)
        shell = EntityClusterShell(world, targetX=28.0, targetZ=28.0)
        shell.setLaunchPosition(1.0, 8.0, 1.0)

        self.assertEqual(shell.targetY, 5.0)
        self.assertGreater(shell.totalFlightTicks, 20)
        self.assertGreaterEqual(shell.arcHeight, 8.0)

        shell._detonate()

        remainingSurface = sum(
            world.getBlockId(x, 4, z) == blocks.stone.blockID
            for x in range(world.width)
            for z in range(world.length)
        )
        self.assertLess(remainingSurface, world.width * world.length)


if __name__ == '__main__':
    unittest.main()
