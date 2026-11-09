## Minecraft: Python Edition

![Minecraft](/screenshot.png?raw=true)

_**Minecraft: Python Edition**_ is a project that strives to recreate each and every old Minecraft version in Python 3 using the **Pyglet** multimedia library and **Cython** for performance.

The project has completed the Indev versions of Minecraft.
This version of Indev, the final one, is **Indev 20100223** as released on _**February 23, 2010**_.

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

For audio to work you will either need *PyOgg* which is recommended, or *FFmpeg* which has to be installed on your system.
*GStreamer* is also supported on Linux through the *gst-python* library.
PyOgg requires that your system have one of the Opus, FLAC, or Vorbis codecs.
*OpenAL* is required and comes bundled with the source on Windows.

For a manual Cython source build, run `python setup.py build_ext --inplace`.

Run `python -m mc.net.minecraft.client.Minecraft` to launch the game. *Minecraft: Python Edition* should be compatible with any modern platform that supports OpenGL and Cython.

Run with the argument `-fullscreen` to open the window in fullscreen mode (or press F11 in-game).
The argument `-creative` will force the game to be in creative mode.

### Gameplay

All controls are as you would expect for the game and they can be configured in the options menu.
Press Left Control (configurable in Controls) to toggle sprint, or double-tap Forward to start sprinting. Sprinting increases ground movement speed.
Creative flight speed can be adjusted with `creativeFlightMultiplier` in `options.txt` (default `10.0`); this setting only affects creative flight.
Press I to open your inventory (or the item catalog in creative mode), F5 for third person view and F7 to take an isometric screenshot.
The creative catalog has item categories, pages, and spawn eggs; click an item to put a stack in the selected hotbar slot.
Press `/` to enter a command. Available commands include `/gamemode c|s`, `/give <item> [amount]`, `/spawn <entity> [count]` (also `/summon`), `/tp <x> <y> <z>` (also `/teleport`), `/spawnpoint`, `/time set <day|night|ticks>`, `/heal`, and `/clear`. Teleports accept relative coordinates such as `~5`. This is a local single-player command set, so give and teleport target only the current player.
In creative mode, hold Space to fly up and Left Shift to fly down. Right-click a spawn egg to create its mob.
Lucky Blocks are available in the creative catalog; breaking one can drop a random reward, spawn a hostile Lycanites mob, or cause an explosion.
The Tsar Bomba is an assembly block with a GUI. Insert 1 TNT block, 8 gunpowder, and 1 diamond, then place a redstone torch next to it to detonate a much larger expanding crater and surrounding shockwave. The blast targets nearby Wither Storms and destroys them if caught in range. Obtain the block with `/give tsarbomba`; it is also available in the creative catalog.
The Wither Storm is a large boss with its own animated model and texture. It does not despawn, tracks and periodically chases the player, absorbs nearby mobs and terrain to evolve through larger, stronger stages, and attacks with increasingly powerful explosions. Terrain absorption grows exponentially with each stage: it can absorb up to 2, 4, 8, then 16 blocks per pulse. Spawn it with `/spawn witherstorm` or its spawn egg. Absorption changes terrain; bedrock, containers, rare blocks, TNT, obsidian, and Lucky Blocks are protected. The current world engine has no chunk system, so the boss cannot load distant chunks or render outside the loaded world.

The Indev level generator is customizable and you can choose between the *Inland*, *Island*, *Floating*, and *Flat* level types.
You can specify the world theme as *Normal*, *Hell* (lava and dirt instead of water and grass), *Paradise* (always daylight), or *Woods*.
World size and world shape (*Square*, *Long*, *Deep*) may also be selected.

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


todo: add aether
todo: clean up texture mapping/make it easier to add LOTS of content.