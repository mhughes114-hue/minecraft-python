from types import SimpleNamespace
import unittest
from unittest.mock import Mock

from mc.net.minecraft.client.Minecraft import Minecraft


class LevelUnloadTests(unittest.TestCase):
    def test_loading_level_precedes_render_registration(self):
        events = []
        world = Mock()
        world.defaultFluid = -1
        world.findSubclassOf.return_value = Mock()
        world.load.side_effect = lambda: events.append("load")
        render_global = Mock()
        render_global.changeWorld.side_effect = lambda _: events.append(
            "changeWorld"
        )
        minecraft = SimpleNamespace(
            theWorld=None,
            thePlayer=None,
            renderGlobal=render_global,
            playerController=Mock(),
            effectRenderer=Mock(),
            options=Mock(),
            session=None,
            renderEngine=Mock(),
            _Minecraft__textureWaterFX=SimpleNamespace(textureId=0),
            _Minecraft__textureLavaFX=SimpleNamespace(textureId=0),
        )

        Minecraft.setLevel(minecraft, world)

        self.assertEqual(events, ["load", "changeWorld"])
        world.load.assert_called_once_with()
        render_global.changeWorld.assert_called_once_with(world)

    def test_unloading_level_detaches_world_state(self):
        old_world = Mock()
        render_global = Mock()
        player_controller = Mock()
        effect_renderer = Mock()
        minecraft = SimpleNamespace(
            theWorld=old_world,
            thePlayer=Mock(),
            renderGlobal=render_global,
            playerController=player_controller,
            effectRenderer=effect_renderer,
        )

        Minecraft.setLevel(minecraft, None)

        old_world.setLevel.assert_called_once_with()
        render_global.changeWorld.assert_called_once_with(None)
        player_controller.onWorldChange.assert_called_once_with(None)
        effect_renderer.clearEffects.assert_called_once_with(None)
        self.assertIsNone(minecraft.theWorld)
        self.assertIsNone(minecraft.thePlayer)


if __name__ == "__main__":
    unittest.main()
