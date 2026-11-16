from importlib import import_module
from types import SimpleNamespace
import unittest


import_module('mc.net.minecraft.client.Minecraft')
EntityFPVDrone = import_module(
    'mc.net.minecraft.game.entity.monster.EntityFPVDrone'
).EntityFPVDrone
EntityPlayer = import_module(
    'mc.net.minecraft.game.entity.player.EntityPlayer'
).EntityPlayer


class FPVDroneTests(unittest.TestCase):
    def test_attack_action_chases_and_damages_target_in_range(self):
        hits = []
        target = SimpleNamespace(
            posX=0.0,
            posY=0.0,
            posZ=1.0,
            height=1.8,
            attackEntityFrom=lambda source, damage: hits.append((source, damage)),
        )
        drone = SimpleNamespace(
            _findPlayerToAttack=lambda: target,
            posX=0.0,
            posY=0.0,
            posZ=0.0,
            height=0.45,
            _playerToAttack=None,
            _moveStrafing=0.0,
            _moveForward=0.0,
            _isJumping=False,
            _moveSpeed=0.9,
            attackTime=0,
            ATTACK_COOLDOWN=EntityFPVDrone.ATTACK_COOLDOWN,
            _attackStrength=5,
            _hasAttacked=False,
        )

        EntityFPVDrone._updatePlayerActionState(drone)

        self.assertIs(drone._playerToAttack, target)
        self.assertGreater(drone._moveForward, 0)
        self.assertEqual(hits, [(drone, 5)])
        self.assertEqual(drone.attackTime, EntityFPVDrone.ATTACK_COOLDOWN)

    def test_debt_decreases_without_a_lower_bound(self):
        player = SimpleNamespace(debt=0)

        for _ in range(1000):
            EntityPlayer.incurDebt(player)

        self.assertEqual(player.debt, -1000)


if __name__ == '__main__':
    unittest.main()
