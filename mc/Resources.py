from pathlib import Path

from PIL import Image


_TEXTURE_ROOT = Path(__file__).parent / "resources" / "texture"
_TERRAIN_TILE_ROOT = _TEXTURE_ROOT / "terrain" / "tiles"
_TILE_SIZE = 16
_TERRAIN_SIZE = 256
_TILE_COUNT = (_TERRAIN_SIZE // _TILE_SIZE) ** 2


def _texture_data(image):
    rgba = image.convert("RGBA").tobytes()
    pixels = [value if value < 128 else value - 256 for value in rgba]
    return image.width, image.height, pixels


def _load_terrain_atlas():
    atlas = Image.new("RGBA", (_TERRAIN_SIZE, _TERRAIN_SIZE))
    for tile_index in range(_TILE_COUNT):
        tile_path = _TERRAIN_TILE_ROOT / f"tile_{tile_index:03d}.png"
        with Image.open(tile_path) as source:
            tile = source.convert("RGBA")

        if tile.size != (_TILE_SIZE, _TILE_SIZE):
            raise ValueError(
                f"Terrain tile {tile_path} must be "
                f"{_TILE_SIZE}x{_TILE_SIZE}, got {tile.size}"
            )

        x = tile_index % (_TERRAIN_SIZE // _TILE_SIZE) * _TILE_SIZE
        y = tile_index // (_TERRAIN_SIZE // _TILE_SIZE) * _TILE_SIZE
        atlas.paste(tile, (x, y))

    return _texture_data(atlas)


textures = {}
for _path in _TEXTURE_ROOT.rglob("*"):
    if not _path.is_file() or _path.suffix.lower() not in {".png", ".gif"}:
        continue
    if _path.parent == _TERRAIN_TILE_ROOT:
        continue

    with Image.open(_path) as _source:
        textures[_path.relative_to(_TEXTURE_ROOT).as_posix()] = _texture_data(
            _source
        )

textures["terrain.png"] = _load_terrain_atlas()
