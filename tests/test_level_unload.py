from types import SimpleNamespace
import unittest
from unittest.mock import Mock

from mc.net.minecraft.client.Minecraft import Minecraft


class LevelUnloadTests(unittest.TestCase):
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
