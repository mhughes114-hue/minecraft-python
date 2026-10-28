from mc.net.minecraft.client.RenderHelper import RenderHelper
from mc.net.minecraft.client.gui.GuiScreen import GuiScreen
from mc.net.minecraft.client.render.entity.RenderItem import RenderItem
from mc.net.minecraft.game.item.ItemArmor import ItemArmor
from mc.net.minecraft.game.item.ItemStack import ItemStack
from mc.net.minecraft.game.item.ItemTool import ItemTool
from mc.net.minecraft.game.item.Items import items
from mc.net.minecraft.game.level.MobSpawner import SPAWN_EGG_ENTITIES
from mc.net.minecraft.game.level.block.Blocks import blocks
from pyglet import gl, window

import re


class GuiCreativeInventory(GuiScreen):
    CATEGORIES = (
        'All Items',
        'Building',
        'Decoration',
        'Materials',
        'Tools',
        'Spawn Eggs',
    )
    COLUMNS = 5
    ROWS = 3
    PAGE_SIZE = COLUMNS * ROWS

    def __init__(self):
        self.xSize = 304
        self.ySize = 220
        self.category = 0
        self.page = 0
        self.__itemRenderer = RenderItem()
        self.__entries = []
        self.__labels = {}

    def initGui(self):
        self.__labels = {}
        for name, block in vars(blocks).items():
            if hasattr(block, 'blockID') and block.blockID:
                self.__labels[block.blockID] = self.__formatName(name)
        for name, item in vars(items).items():
            if hasattr(item, 'shiftedIndex'):
                self.__labels[item.shiftedIndex] = self.__formatName(name)
        self.__labels[items.spawnEgg.shiftedIndex] = 'Spawn Egg'
        self.__refreshEntries()

    @staticmethod
    def __formatName(name):
        return re.sub(r'([a-z])([A-Z])', r'\1 \2', name).replace('_', ' ').title()

    def __refreshEntries(self):
        category = self.CATEGORIES[self.category]
        entries = []
        if category == 'Spawn Eggs':
            for index, (name, _) in enumerate(SPAWN_EGG_ENTITIES):
                entries.append((ItemStack(items.spawnEgg, 64, index), name + ' Spawn Egg'))
        elif category in ('All Items', 'Building', 'Decoration'):
            if category == 'All Items':
                blockIds = [
                    block.blockID for block in blocks.blocksList
                    if block and block.blockID
                ]
            elif category == 'Building':
                excluded = {
                    blocks.sapling.blockID, blocks.waterMoving.blockID,
                    blocks.waterStill.blockID, blocks.lavaMoving.blockID,
                    blocks.lavaStill.blockID, blocks.fire.blockID,
                    blocks.crops.blockID, blocks.tilledField.blockID,
                    blocks.plantYellow.blockID, blocks.plantRed.blockID,
                    blocks.mushroomBrown.blockID, blocks.mushroomRed.blockID,
                }
                blockIds = [
                    block.blockID for block in blocks.blocksList
                    if block and block.blockID and block.blockID not in excluded
                ]
            else:
                decorative = {
                    blocks.sapling.blockID, blocks.torch.blockID,
                    blocks.bookShelf.blockID, blocks.glass.blockID,
                    blocks.chest.blockID, blocks.cog.blockID,
                    blocks.plantYellow.blockID, blocks.plantRed.blockID,
                    blocks.mushroomBrown.blockID, blocks.mushroomRed.blockID,
                    blocks.workbench.blockID, blocks.clothGray.blockID,
                    blocks.clothWhite.blockID,
                }
                blockIds = [
                    block.blockID for block in blocks.blocksList
                    if block and block.blockID in decorative
                ]

            for itemId in blockIds:
                entries.append((ItemStack(itemId, 64), self.__getItemName(itemId)))

            if category == 'All Items':
                for itemId in range(256, len(items.itemsList)):
                    if items.itemsList[itemId]:
                        entries.append((
                            ItemStack(itemId, 64),
                            self.__getItemName(itemId)
                        ))
        else:
            for itemId in range(256, len(items.itemsList)):
                item = items.itemsList[itemId]
                if not item or itemId == items.spawnEgg.shiftedIndex:
                    continue
                if category == 'Materials' and not isinstance(item, (ItemTool, ItemArmor)):
                    entries.append((ItemStack(itemId, 64), self.__getItemName(itemId)))
                elif category == 'Tools' and isinstance(item, (ItemTool, ItemArmor)):
                    entries.append((ItemStack(itemId, 1), self.__getItemName(itemId)))

        self.__entries = entries
        self.page = min(self.page, max(0, (len(entries) - 1) // self.PAGE_SIZE))

    def __getItemName(self, itemId):
        return self.__labels.get(itemId, 'Item ' + str(itemId))

    def _keyTyped(self, key, char, motion):
        if key in (window.key.ESCAPE, self.mc.options.keyBindInventory.keyCode):
            self.mc.displayGuiScreen(None)
            return
        if key == window.key.PAGEUP:
            self.page = max(0, self.page - 1)
        elif key == window.key.PAGEDOWN:
            self.page = min(self.__getPageCount() - 1, self.page + 1)
        elif key in (window.key.LEFT, window.key.RIGHT):
            direction = -1 if key == window.key.LEFT else 1
            self.category = (self.category + direction) % len(self.CATEGORIES)
            self.page = 0
            self.__refreshEntries()
        elif window.key._1 <= key <= window.key._9:
            self.mc.thePlayer.inventory.currentItem = key - window.key._1
        else:
            super()._keyTyped(key, char, motion)

    def __getPageCount(self):
        return max(1, (len(self.__entries) + self.PAGE_SIZE - 1) // self.PAGE_SIZE)

    def _mouseClicked(self, xm, ym, button):
        if button not in (window.mouse.LEFT, window.mouse.RIGHT):
            return

        x = (self.width - self.xSize) // 2
        y = (self.height - self.ySize) // 2
        localX = xm - x
        localY = ym - y

        if 8 <= localX < 76 and 34 <= localY < 34 + len(self.CATEGORIES) * 19:
            category = (localY - 34) // 19
            if category < len(self.CATEGORIES):
                self.category = category
                self.page = 0
                self.__refreshEntries()
            return

        if 82 <= localX < 132 and 108 <= localY < 126:
            self.page = max(0, self.page - 1)
            return
        if 135 <= localX < 185 and 108 <= localY < 126:
            self.page = min(self.__getPageCount() - 1, self.page + 1)
            return

        if 82 <= localX < 82 + 9 * 19 and 145 <= localY < 167:
            slot = (localX - 82) // 19
            if slot < 9:
                self.mc.thePlayer.inventory.currentItem = slot
            return

        if not (82 <= localX < 82 + self.COLUMNS * 22 and
                36 <= localY < 36 + self.ROWS * 22):
            return

        column = (localX - 82) // 22
        row = (localY - 36) // 22
        entryIndex = self.page * self.PAGE_SIZE + row * self.COLUMNS + column
        if entryIndex >= len(self.__entries):
            return

        template, _ = self.__entries[entryIndex]
        item = template.getItem()
        amount = 1 if button == window.mouse.RIGHT else item.getItemStackLimit()
        inventory = self.mc.thePlayer.inventory
        inventory.mainInventory[inventory.currentItem] = ItemStack(
            template.itemID, amount, template.itemDamage
        )

    def drawScreen(self, xm, ym, renderPartialTicks):
        self.drawDefaultBackground()
        x = (self.width - self.xSize) // 2
        y = (self.height - self.ySize) // 2
        self._drawRect(x - 2, y - 2, x + self.xSize + 2, y + self.ySize + 2,
                       0xD0000000)
        self._drawRect(x, y, x + self.xSize, y + self.ySize, 0xF02B2925)
        self._drawRect(x, y, x + self.xSize, y + 27, 0xFF3D3A32)
        self._fontRenderer.drawStringWithShadow(
            'CREATIVE INVENTORY', x + 12, y + 10, 0xFFFFFF
        )
        self._fontRenderer.drawStringWithShadow(
            '4J item catalog', x + 198, y + 10, 0xD6D0C2
        )

        for index, category in enumerate(self.CATEGORIES):
            tabY = y + 34 + index * 19
            active = index == self.category
            color = 0xFF98703B if active else 0xFF45433D
            self._drawRect(x + 8, tabY, x + 76, tabY + 17, color)
            self._fontRenderer.drawStringWithShadow(
                category, x + 13, tabY + 5, 0xFFFFFF if active else 0xC6C1B5
            )

        self._drawRect(x + 80, y + 32, x + 194, y + 104, 0xFF171715)
        start = self.page * self.PAGE_SIZE
        visible = self.__entries[start:start + self.PAGE_SIZE]
        hoveredName = ''
        for index, (stack, name) in enumerate(visible):
            column = index % self.COLUMNS
            row = index // self.COLUMNS
            cellX = x + 82 + column * 22
            cellY = y + 36 + row * 22
            hovered = cellX <= xm < cellX + 20 and cellY <= ym < cellY + 20
            self._drawRect(
                cellX, cellY, cellX + 20, cellY + 20,
                0xFF857244 if hovered else 0xFF34332F
            )
            if hovered:
                hoveredName = name
        gl.glPushMatrix()
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        RenderHelper.enableStandardItemLighting()
        for index, (stack, _) in enumerate(visible):
            column = index % self.COLUMNS
            row = index // self.COLUMNS
            cellX = x + 82 + column * 22
            cellY = y + 36 + row * 22
            self.__itemRenderer.renderItemIntoGUI(
                self.mc.renderEngine, stack, cellX + 2, cellY + 2
            )
        RenderHelper.disableStandardItemLighting()
        gl.glPopMatrix()

        self._drawRect(x + 198, y + 32, x + 296, y + 104, 0xFF34332F)
        if hoveredName:
            self._fontRenderer.drawStringWithShadow(
                hoveredName[:16], x + 204, y + 42, 0xFFFFFF
            )
        else:
            self._fontRenderer.drawStringWithShadow(
                'Select an item', x + 204, y + 42, 0xD6D0C2
            )
        self._fontRenderer.drawStringWithShadow(
            'Click to equip', x + 204, y + 63, 0xB9B2A2
        )
        self._fontRenderer.drawStringWithShadow(
            'Right-click: 1', x + 204, y + 78, 0xB9B2A2
        )

        self._drawRect(x + 82, y + 108, x + 132, y + 126, 0xFF45433D)
        self._drawRect(x + 135, y + 108, x + 185, y + 126, 0xFF45433D)
        pageText = 'PAGE ' + str(self.page + 1) + '/' + str(self.__getPageCount())
        self._fontRenderer.drawStringWithShadow('< PREV', x + 86, y + 113, 0xFFFFFF)
        self._fontRenderer.drawStringWithShadow('NEXT >', x + 139, y + 113, 0xFFFFFF)
        self._fontRenderer.drawStringWithShadow(pageText, x + 204, y + 113, 0xD6D0C2)

        inventory = self.mc.thePlayer.inventory
        self._fontRenderer.drawStringWithShadow('HOTBAR', x + 8, y + 151, 0xD6D0C2)
        for slot in range(9):
            slotX = x + 82 + slot * 19
            selected = slot == inventory.currentItem
            self._drawRect(
                slotX, y + 145, slotX + 18, y + 167,
                0xFF98703B if selected else 0xFF34332F
            )
        gl.glPushMatrix()
        gl.glColor4f(1.0, 1.0, 1.0, 1.0)
        RenderHelper.enableStandardItemLighting()
        for slot in range(9):
            slotX = x + 82 + slot * 19
            stack = inventory.mainInventory[slot]
            if stack:
                self.__itemRenderer.renderItemIntoGUI(
                    self.mc.renderEngine, stack, slotX + 1, y + 148
                )
        RenderHelper.disableStandardItemLighting()
        gl.glPopMatrix()

        self._fontRenderer.drawStringWithShadow(
            'I/ESC close  arrows category  PgUp/PgDn page',
            x + 8, y + 201, 0xB9B2A2
        )
