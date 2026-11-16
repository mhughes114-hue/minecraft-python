from importlib import import_module
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import_module('mc.net.minecraft.client.Minecraft')
FactionVehicle = import_module(
    'mc.net.minecraft.game.entity.monster.FactionVehicle'
).FactionVehicle
World = import_module('mc.net.minecraft.game.level.World').World


class FactionVehicleTests(unittest.TestCase):
    def test_world_decrements_global_tsar_cooldown_each_tick(self):
        world = World()
        world.tsarBombaCooldown = 2

        world.tick()

        self.assertEqual(world.tsarBombaCooldown, 1)

    def test_aircraft_drops_normal_bombs_during_tsar_warmup(self):
        target = SimpleNamespace(
            posX=12.5,
            posY=24.0,
            posZ=36.5,
            isEntityAlive=lambda: True,
        )
        world = SimpleNamespace(
            tsarBombs=[],
            spawnEntityInWorld=lambda bomb: world.droppedBombs.append(bomb),
            droppedBombs=[],
            tsarBombaCooldown=0,
        )
        aircraft = SimpleNamespace(
            vehicle='aircraft',
            health=50,
            _playerToAttack=target,
            _tsarBombCooldown=FactionVehicle.TSAR_BOMBA_INITIAL_DELAY,
            _normalBombCooldown=0,
            _worldObj=world,
            NORMAL_BOMB_COOLDOWN=FactionVehicle.NORMAL_BOMB_COOLDOWN,
        )
        aircraft._dropNormalBombWhenReady = lambda bombTarget: \
            FactionVehicle._dropNormalBombWhenReady(aircraft, bombTarget)
        aircraft._dropNormalBomb = lambda bombTarget: \
            FactionVehicle._dropNormalBomb(aircraft, bombTarget)
        normal_bomb = SimpleNamespace()
        with patch(
            'mc.net.minecraft.game.entity.misc.EntityTNTPrimed.EntityTNTPrimed',
            return_value=normal_bomb,
        ) as create_bomb:
            FactionVehicle._updateTsarBomba(aircraft)

        self.assertEqual(
            aircraft._tsarBombCooldown,
            FactionVehicle.TSAR_BOMBA_INITIAL_DELAY - 1,
        )
        create_bomb.assert_called_once_with(world, 12.5, 34.0, 36.5)
        self.assertEqual(world.droppedBombs, [normal_bomb])
        self.assertEqual(normal_bomb.fuse, 40)
        self.assertEqual(normal_bomb.motionY, -0.2)
        self.assertEqual(world.tsarBombs, [])

    def test_aircraft_global_cooldown_limits_tsar_drops(self):
        target = SimpleNamespace(
            posX=12.5,
            posY=24.0,
            posZ=36.5,
            isEntityAlive=lambda: True,
        )
        world = SimpleNamespace(
            tsarBombs=[],
            tsarBombaCooldown=0,
            rand=SimpleNamespace(nextInt=lambda bound: 0),
        )
        aircraft = SimpleNamespace(
            vehicle='aircraft',
            health=50,
            _playerToAttack=target,
            _tsarBombCooldown=0,
            _normalBombCooldown=FactionVehicle.NORMAL_BOMB_COOLDOWN,
            _worldObj=world,
            TSAR_BOMBA_COOLDOWN=FactionVehicle.TSAR_BOMBA_COOLDOWN,
            TSAR_BOMBA_COOLDOWN_VARIANCE=FactionVehicle.TSAR_BOMBA_COOLDOWN_VARIANCE,
        )
        bomb = object()

        with patch(
            'mc.net.minecraft.game.level.TsarBomba.TsarBomba',
            return_value=bomb,
        ) as create_bomb:
            FactionVehicle._updateTsarBomba(aircraft)

        create_bomb.assert_called_once_with(world, 12.5, 24.0, 36.5)
        self.assertEqual(world.tsarBombs, [bomb])
        self.assertEqual(world.tsarBombaCooldown, FactionVehicle.TSAR_BOMBA_COOLDOWN)


if __name__ == '__main__':
    unittest.main()
