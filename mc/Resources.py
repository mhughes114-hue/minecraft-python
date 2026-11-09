from pathlib import Path

from PIL import Image


_TEXTURE_ROOT = Path(__file__).parent / "resources" / "texture"
_TERRAIN_TILE_ROOT = _TEXTURE_ROOT / "terrain" / "tiles"
_TILE_SIZE = 16
_TERRAIN_SIZE = 256
_TILE_COUNT = (_TERRAIN_SIZE // _TILE_SIZE) ** 2


def _texture_data(image: Image.Image) -> tuple[int, int, list[int]]:
    rgba = image.convert("RGBA").tobytes()
    pixels = [value if value < 128 else value - 256 for value in rgba]
    return image.width, image.height, pixels


def _load_terrain_atlas() -> tuple[int, int, list[int]]:
    atlas = Image.new("RGBA", (_TERRAIN_SIZE, _TERRAIN_SIZE))
    for tile_index in range(_TILE_COUNT):
        tile_path = _TERRAIN_TILE_ROOT / f"tile_{tile_index:03d}.png"
        with Image.open(tile_path) as tile_image:
            tile = tile_image.convert("RGBA")

        if tile.size != (_TILE_SIZE, _TILE_SIZE):
            raise ValueError(
                f"Terrain tile {tile_path} must be "
                f"{_TILE_SIZE}x{_TILE_SIZE}, got {tile.size}"
            )

        x = tile_index % (_TERRAIN_SIZE // _TILE_SIZE) * _TILE_SIZE
        y = tile_index // (_TERRAIN_SIZE // _TILE_SIZE) * _TILE_SIZE
        atlas.paste(tile, (x, y))

    return _texture_data(atlas)


textures: dict[str, tuple[int, int, list[int]]] = {}
for path in sorted(_TEXTURE_ROOT.rglob("*")):
    if not path.is_file() or path.suffix.lower() not in {".png", ".gif"}:
        continue
    if path.parent == _TERRAIN_TILE_ROOT:
        continue

    with Image.open(path) as texture_image:
        textures[path.relative_to(_TEXTURE_ROOT).as_posix()] = _texture_data(
            texture_image
        )

textures["terrain.png"] = _load_terrain_atlas()
