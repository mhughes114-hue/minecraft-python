## Minecraft: Rust Edition

![Minecraft](/screenshot.png?raw=true)

_**Minecraft: Rust Edition**_ is an in-progress native Rust prototype using a software renderer.

It currently includes procedural terrain, first-person movement, basic block rendering from the
existing terrain tiles, a hotbar, title/pause/inventory overlays, and a few placeholder wandering
mobs. This is **not a complete port** of the Python game: most gameplay systems, entities, menus,
items, crafting, audio, Java-compatible NBT saves, and the original rendering pipeline have not yet
been implemented in Rust. The Python game remains available separately using the launch command below.

This version adds paintings to the game and makes wood logs drop as logs instead of planks.
It also includes four original creatures inspired by Lycanites Mobs: the peaceful Aegis and the hostile Cinder, Chupacabra, and Ventoraptor.

Features added in Indev include the wood spawn house, NBT level file saving, mobs and animals, farming, furnaces,
durable tools, armor, day and night cycle, difficulty, torches, advanced liquid spread,
TNT explosives, chests, the main menu, workbench crafting, porkchops, soup, and flint and steel.

To easily install this version of *Minecraft: Python Edition*, just run `python -m pip install minecraft-python==20100223`.

You can learn more about this version [on the Minecraft wiki.](https://minecraft.wiki/w/Java_Edition_Indev_20100223)

### Organization

This project's commits represent the Python versions of each Minecraft Java game version.
You can view source code changes between game versions by checking the commit history or comparing branches.
To play any version, specify it in the `pip install` command as demonstrated below.

### General Usage

*Pyglet*, *Cython*, *Pillow*, *PyOgg*, *NumPy*, and *nbtlib* are required dependencies which can easily be installed with *pip*. Use the versions specified in `requirements.txt`.
*wxPython* is an optional dependency for the level file picker, but if you don't have it then *Tkinter* is used instead.

### Rust build

The native Rust client requires a recent stable Rust toolchain.

```powershell
cargo run --release
```

Use WASD to move, mouse to look, Space to jump, number keys to select blocks, left/right click to
mine/place, I to open inventory, and Escape to pause. Click Play/Resume to enter the world. F5/F9
save/load the world.

For audio to work you will either need *PyOgg* which is recommended, or *FFmpeg* which has to be installed on your system.
*GStreamer* is also supported on Linux through the *gst-python* library.
PyOgg requires that your system have one of the Opus, FLAC, or Vorbis codecs.
*OpenAL* is required and comes bundled with the source on Windows.

For a manual Cython source build, run `python setup.py build_ext --inplace`.

Run `python -m mc.net.minecraft.client.Minecraft` with the Python environment where the dependencies are installed to launch the game. On Windows, if you use this repository's virtual environment, run `.\.venv\Scripts\python.exe -m mc.net.minecraft.client.Minecraft`; using a different Python installation can fail because the compiled extensions require NumPy. *Minecraft: Python Edition* should be compatible with any modern platform that supports OpenGL and Cython.

Run with the argument `-fullscreen` to open the window in fullscreen mode (or press F11 in-game).
The argument `-creative` will force the game to be in creative mode.

### Gameplay

All controls are as you would expect for the game and they can be configured in the options menu.
Press Left Control (configurable in Controls) to toggle sprint, or double-tap Forward to start sprinting. Sprinting increases ground movement speed.
Creative flight speed can be adjusted with `creativeFlightMultiplier` in `options.txt` (default `10.0`); this setting only affects creative flight.
Press I to open your inventory (or the item catalog in creative mode), F5 for third person view and F7 to take an isometric screenshot.
The creative catalog has item categories, pages, and spawn eggs; click an item to put a stack in the selected hotbar slot.
Press `/` to enter a command. Available commands include `/gamemode c|s`, `/give <item> [amount]`, `/spawn <entity> [count]` (also `/summon`), `/tp <x> <y> <z>` (also `/teleport`), `/spawnpoint`, `/time set <day|night|ticks>`, `/heal`, and `/clear`. Teleports accept relative coordinates such as `~5`. This is a local single-player command set, so give and teleport target only the current player.
Trigger Noah's Flood with `/flood start` (or `/noahsflood`); God warns you to build an ark before the waters rise across the world. Use `/flood status` or `/flood stop` to check or stop the event. Sinkholes also occur randomly and can consume mobs or the player; use `/sinkhole [player|mob|random]` to trigger one manually.
In creative mode, hold Space to fly up and Left Shift to fly down. On foot, hold Left Shift to sneak and avoid stepping off block edges. Right-click a spawn egg to create its mob.
Hostile FPV drones hunt players, villagers, and pillagers, attacking on contact. Spawn one with `/spawn fpvdrone` or its creative spawn egg. The DEBT counter in the top-right decreases once per tick while the player is alive, with additional decreases for walking and each block broken; it has no gameplay effect and no lower limit.
Lucky Blocks are available in the creative catalog; breaking one can drop a random reward, spawn a hostile Lycanites mob, or cause an explosion.
Villagers and pillagers naturally spawn in larger groups and fight each other. Both factions use colored laser rifles, tanks, MLRS launchers, and aircraft; tanks use explosive shells, MLRS vehicles fire delayed indirect cluster volleys that leave several small craters, and aircraft patrol above the battlefield, dropping conventional TNT bombs for their first three in-game days before escalating to Tsar Bombas at a rate of roughly one or two per day across all aircraft. Landmines are scattered across newly generated worlds, trigger when a living entity gets close, and avoid the spawn area. Faction units can break ordinary blocks blocking their path, but leave bedrock, containers, ores, TNT, obsidian, Lucky Blocks, and the Tsar Bomba intact. Spawn people with `/spawn villager` or `/spawn pillager`, and vehicles with `/spawn villagertank`, `/spawn pillagertank`, `/spawn villagermlrs`, `/spawn pillagermlrs`, `/spawn villageraircraft`, or `/spawn pillageraircraft`; all have creative spawn eggs.
The Tsar Bomba is an assembly block with a GUI. Insert 1 TNT block, 8 gunpowder, and 1 diamond, then place a redstone torch next to it to detonate a much larger expanding crater and surrounding shockwave, crowned by a rising mushroom cloud. The blast targets nearby Wither Storms and destroys them if caught in range. Obtain the block with `/give tsarbomba`; it is also available in the creative catalog.
The Wither Storm is a large boss with its own animated model and texture. It does not despawn, tracks and periodically chases the player, absorbs nearby mobs and terrain to evolve through larger, stronger stages, and attacks with increasingly powerful explosions. Terrain absorption grows exponentially with each stage: it can absorb up to 2, 4, 8, then 16 blocks per pulse. Spawn it with `/spawn witherstorm` or its spawn egg. Absorption changes terrain; bedrock, containers, rare blocks, TNT, obsidian, and Lucky Blocks are protected. The current world engine has no chunk system, so the boss cannot load distant chunks or render outside the loaded world.

The Indev level generator is customizable and you can choose between the *Inland*, *Island*, *Floating*, and *Flat* level types.
You can specify the world theme as *Normal*, *Hell* (lava and dirt instead of water and grass), *Paradise* (always daylight), *Woods*, or *Aether*.
The *Aether* theme generates a bright sky world with floating islands; it can be selected independently of the world type.
World size and world shape (*Square*, *Long*, *Deep*) may also be selected.
For smoother frame pacing on large worlds, chunk meshes rebuild incrementally (at most two per frame), chunk sorting is cached until the player moves about one chunk, frustum checks and entity rendering are restricted to the configured view-distance area, lighting work runs on game ticks, and nearby entities use the entity grid for collision and landmine checks. Render distance can be lowered in Options. The renderer follows chunk-culling and incremental-rebuild principles, but remains on the legacy fixed-function OpenGL path; modern Sodium/Angelica renderers target newer Minecraft engines and are not drop-in compatible.

Levels can be saved to a single *.mclevel* NBT file in the pause menu. The level files are perfectly compatible with Java and vice versa.

Porkchops, mushroom bowl soup, and bread will restore health. Check the Wiki for crafting recipes added in this version.

![Isometric screenshot](/map.png?raw=true)

*An isometric screenshot of a normal Woods map generated by the game.*

### Additional Notes

The `mc.resources` directory contains the textures and sounds used by this version. Terrain textures
are stored as individual 16-by-16 PNG files in `mc/resources/texture/terrain/tiles`; their numbered
filenames retain the legacy row-major tile indices used by the block renderer. `mc.Resources`
assembles these tiles into the runtime terrain atlas, while the other texture files are loaded
directly. Keeping the source textures separate makes them easier to replace and maintain.

This would have been much more challenging to work on without the great tools provided by [RetroMCP-Java](https://github.com/MCPHackers/RetroMCP-Java).

All credit for Minecraft goes towards its creator Notch and Mojang Specifications.

Yeah ok but what I do is
.\.venv\Scripts\python.exe -m mc.net.minecraft.client.Minecraft


-add landmines
-add MLRS
-add WRATH
-add entire earth
-add FPV drones
-add debt
-add LODs
