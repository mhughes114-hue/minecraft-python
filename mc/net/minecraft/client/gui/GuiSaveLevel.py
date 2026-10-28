from mc.net.minecraft.client.gui.GuiLoadLevel import GuiLoadLevel
from mc.net.minecraft.client.gui.GuiNameLevel import GuiNameLevel
from mc.net.minecraft.client.PlayerLoader import PlayerLoader

import os

class GuiSaveLevel(GuiLoadLevel):

    def __init__(self, screen):
        super().__init__(screen)
        self._title = 'Save level'

    def initGui(self):
        super().initGui()
        self._controlList[5].displayString = 'Save file...'

    def _setLevels(self, levels):
        for i in range(5):
            self._controlList[i].displayString = (
                levels[i] if levels[i] != '-' else f'World {i + 1}'
            )
            self._controlList[i].enabled = True
            self._controlList[i].visible = True

        self._controlList[5].visible = True

    def _openFile(self, file):
        PlayerLoader(self.mc, self.mc.loadingScreen).save(self.mc.theWorld, file)

    def _saveLevel(self, name, slot):
        self.mc.theWorld.name = name
        saves = os.path.join(self.mc.mcDataDir, 'saves')
        os.makedirs(saves, exist_ok=True)
        self._openFile(os.path.join(saves, f'level{slot}.mclevel'))

    def _openLevel(self, i):
        self.mc.displayGuiScreen(GuiNameLevel(self, self._controlList[i].displayString, i))
