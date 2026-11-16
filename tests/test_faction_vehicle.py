from importlib import import_module
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import_module('mc.net.minecraft.client.Minecraft')
FactionVehicle = import_module(
    'mc.net.minecraft.game.entity.monster.FactionVehicle'
).FactionVehicle


class FactionVehicleTests(unittest.TestCase):
    def test_aircraft_drops_tsar_bomba_on_target_after_cooldown(self):
        target = SimpleNamespace(
            posX=12.5,
            posY=24.0,
            posZ=36.5,
            isEntityAlive=lambda: True,
        )
        world = SimpleNamespace(tsarBombs=[])
        aircraft = SimpleNamespace(
            vehicle='aircraft',
            health=50,
            _playerToAttack=target,
            _tsarBombCooldown=0,
            _worldObj=world,
            TSAR_BOMBA_COOLDOWN=FactionVehicle.TSAR_BOMBA_COOLDOWN,
        )
        bomb = object()

        with patch(
            'mc.net.minecraft.game.level.TsarBomba.TsarBomba',
            return_value=bomb,
        ) as create_bomb:
            FactionVehicle._updateTsarBomba(aircraft)
            FactionVehicle._updateTsarBomba(aircraft)

        create_bomb.assert_called_once_with(world, 12.5, 24.0, 36.5)
        self.assertEqual(world.tsarBombs, [bomb])
        self.assertEqual(
            aircraft._tsarBombCooldown,
            FactionVehicle.TSAR_BOMBA_COOLDOWN - 1,
        )


if __name__ == '__main__':
    unittest.main()
