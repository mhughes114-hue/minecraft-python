from pathlib import Path
import unittest

from PIL import Image

from mc.Resources import textures


_TEXTURE_ROOT = Path(__file__).parents[1] / "mc" / "resources" / "texture"


class TextureResourceTests(unittest.TestCase):
    def test_terrain_atlas_is_built_from_numbered_tiles(self):
        width, height, atlas_pixels = textures["terrain.png"]
        self.assertEqual((width, height), (256, 256))

        for tile_index in range(256):
            tile_path = (
                _TEXTURE_ROOT
                / "terrain"
                / "tiles"
                / f"tile_{tile_index:03d}.png"
            )
            with Image.open(tile_path) as source:
                tile_pixels = source.convert("RGBA").tobytes()

            x = tile_index % 16 * 16
            y = tile_index // 16 * 16
            atlas_tile = bytearray()
            for row in range(16):
                start = ((y + row) * width + x) * 4
                atlas_tile.extend(
                    value & 0xFF
                    for value in atlas_pixels[start : start + 16 * 4]
                )

            self.assertEqual(tile_pixels, atlas_tile, tile_path.name)

    def test_regular_textures_are_loaded_by_relative_path(self):
        width, height, pixels = textures["gui/gui.png"]
        with Image.open(_TEXTURE_ROOT / "gui" / "gui.png") as source:
            expected = source.convert("RGBA").tobytes()

        self.assertEqual(bytes(value & 0xFF for value in pixels), expected)
        self.assertGreater(width, 0)
        self.assertGreater(height, 0)

    def test_menu_background_is_loaded_as_a_texture(self):
        width, height, pixels = textures["background.png"]
        with Image.open(_TEXTURE_ROOT / "background.png") as source:
            expected = source.convert("RGBA").tobytes()

        self.assertEqual(bytes(value & 0xFF for value in pixels), expected)
        self.assertEqual((width, height), (512, 512))

    def test_custom_mob_textures_are_loaded(self):
        for texture_name in (
            "mob/aegis.png",
            "mob/cinder.png",
            "mob/chupacabra.png",
            "mob/ventoraptor.png",
        ):
            with self.subTest(texture_name=texture_name):
                width, height, _ = textures[texture_name]
                self.assertEqual((width, height), (64, 32))


if __name__ == "__main__":
    unittest.main()
