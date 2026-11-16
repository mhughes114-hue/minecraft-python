from importlib import import_module
from types import SimpleNamespace
import unittest
from unittest.mock import Mock

import_module('mc.net.minecraft.client.Minecraft')
Minecraft = import_module('mc.net.minecraft.client.Minecraft').Minecraft
WorldEvents = import_module(
    'mc.net.minecraft.game.level.WorldEvents'
).WorldEvents
blocks = import_module(
    'mc.net.minecraft.game.level.block.Blocks'
).blocks


class WorldEventsTests(unittest.TestCase):
    def make_world(self):
        block_ids = {}
        return SimpleNamespace(
            width=5,
            length=5,
            height=5,
            waterLevel=1,
            entityMap=SimpleNamespace(all=[]),
            playerEntity=None,
            getBlockId=lambda x, y, z: block_ids.get((x, y, z), 0),
            setBlock=lambda x, y, z, block_id: (
                block_ids.__setitem__((x, y, z), block_id) or True
            ),
            spawnParticle=lambda *args: None,
            block_ids=block_ids,
        )

    def test_flood_warns_then_fills_every_open_world_layer(self):
        world = self.make_world()
        messages = []
        events = WorldEvents(world, messages.append)

        self.assertIn('Build an ark', events.flood.start())
        self.assertEqual(events.flood.status(), "Noah's Flood begins in 30 seconds.")
        for _ in range(events.flood.WARNING_TICKS + 3):
            events.update()

        self.assertEqual(events.flood.state, 'complete')
        self.assertTrue(any('The rain begins' in message for message in messages))
        self.assertEqual(
            {
                world.block_ids[(x, y, z)]
                for x in range(1, world.width - 1)
                for y in range(1, world.height - 1)
                for z in range(1, world.length - 1)
            },
            {blocks.waterStill.blockID},
        )

    def test_flood_command_reports_status_and_can_stop(self):
        events = WorldEvents(self.make_world(), lambda _: None)
        minecraft = SimpleNamespace(
            _Minecraft__worldEvents=events,
            theWorld=events.world,
            thePlayer=SimpleNamespace(),
        )

        self.assertIn('Build an ark', Minecraft.executeCommand(
            minecraft, '/flood start'
        ))
        self.assertIn('begins in 30 seconds', Minecraft.executeCommand(
            minecraft, '/flood status'
        ))
        self.assertIn('stopped', Minecraft.executeCommand(
            minecraft, '/flood stop'
        ))

    def test_sinkhole_command_can_target_the_player(self):
        events = WorldEvents(self.make_world(), lambda _: None)
        player = SimpleNamespace()
        events.selectSinkholeTarget = Mock(return_value=player)
        events.startSinkhole = Mock(return_value=True)
        minecraft = SimpleNamespace(
            _Minecraft__worldEvents=events,
            theWorld=events.world,
            thePlayer=player,
        )

        result = Minecraft.executeCommand(minecraft, '/sinkhole player')

        self.assertIn('opened', result)
        events.selectSinkholeTarget.assert_called_once_with('player')
        events.startSinkhole.assert_called_once_with(player)

    def test_sinkhole_consumes_player_after_opening_a_pit(self):
        world = self.make_world()
        for x in range(1, world.width - 1):
            for z in range(1, world.length - 1):
                for y in (1, 2):
                    world.block_ids[(x, y, z)] = blocks.stone.blockID
        target = SimpleNamespace(
            posX=2.5,
            posZ=2.5,
            boundingBox=SimpleNamespace(minY=3.0),
            motionY=0.0,
            health=20,
            deathTime=0,
            isEntityAlive=lambda: target.health > 0,
        )
        world.playerEntity = target
        messages = []
        events = WorldEvents(world, messages.append)

        self.assertTrue(events.startSinkhole(target))
        self.assertTrue(any(block_id == 0 for block_id in world.block_ids.values()))
        for _ in range(40):
            events.update()

        self.assertEqual(target.health, 0)
        self.assertTrue(any('consumes its victim' in message for message in messages))


if __name__ == '__main__':
    unittest.main()
