from importlib import import_module
from types import SimpleNamespace
import unittest

import_module('mc.net.minecraft.client.Minecraft')
EntityPlayerSP = import_module(
    'mc.net.minecraft.client.player.EntityPlayerSP'
).EntityPlayerSP
TsarBomba = import_module(
    'mc.net.minecraft.game.level.TsarBomba'
).TsarBomba
EntityTsarCloudFX = import_module(
    'mc.net.minecraft.client.effect.EntityTsarCloudFX'
).EntityTsarCloudFX
AxisAlignedBB = import_module(
    'mc.net.minecraft.game.physics.AxisAlignedBB'
).AxisAlignedBB


class TsarCloudAndSneakingTests(unittest.TestCase):
    def test_moved_collision_box_offsets_each_axis_correctly(self):
        box = AxisAlignedBB(1.0, 2.0, 3.0, 4.0, 5.0, 6.0)

        moved = box.cloneMove(0.5, 1.0, -0.5)

        self.assertEqual(
            (moved.minX, moved.minY, moved.minZ,
             moved.maxX, moved.maxY, moved.maxZ),
            (1.5, 3.0, 2.5, 4.5, 6.0, 5.5),
        )

    def test_tsar_bomba_emits_a_tall_mushroom_cloud(self):
        particles = []
        world = SimpleNamespace(
            height=64,
            entityMap=SimpleNamespace(all=[]),
            spawnParticle=lambda *particle: particles.append(particle),
        )

        TsarBomba(world, 20.5, 20.5, 20.5)

        self.assertGreater(len(particles), 40)
        self.assertTrue(all(particle[0] == 'tsar' for particle in particles))
        self.assertGreater(max(particle[2] for particle in particles), 50.0)

    def test_tsar_cloud_particles_are_large_and_long_lived(self):
        particle = EntityTsarCloudFX(None, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

        self.assertGreaterEqual(particle._particleScale, 15.0)
        self.assertGreaterEqual(particle._particleMaxAge, 160)

    def test_sneak_movement_stops_at_the_supported_edge(self):
        class PlayerStub:
            boundingBox = AxisAlignedBB(0.0, 0.0, 0.0, 0.6, 1.8, 0.6)

            class WorldStub:
                @staticmethod
                def getCollidingBoundingBoxes(box):
                    return [object()] if box.maxX <= 0.8 and box.maxZ <= 0.8 else []

            _worldObj = WorldStub()

            def _hasSneakSupport(self, x, z):
                return EntityPlayerSP._hasSneakSupport(self, x, z)

        x, z = EntityPlayerSP._getSneakSafeMovement(PlayerStub(), 0.5, 0.0)

        self.assertGreater(x, 0.0)
        self.assertLessEqual(x, 0.2)
        self.assertEqual(z, 0.0)


if __name__ == '__main__':
    unittest.main()
