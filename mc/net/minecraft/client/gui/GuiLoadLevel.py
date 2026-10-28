from mc.net.minecraft.client.gui.GuiLevelDialog import GuiLevelDialog
from mc.net.minecraft.client.gui.GuiScreen import GuiScreen
from mc.net.minecraft.client.gui.GuiButton import GuiButton
from mc.net.minecraft.client.PlayerLoader import PlayerLoader

import os
import traceback

class GuiLoadLevel(GuiScreen):

    def __init__(self, screen):
        self.__parent = screen
        self.__finished = False
        self.__loaded = False
        self.__levels = []
        self.__status = ''
        self._title = 'Load level'
        self.__frozen = False
        self.__selectedFile = ''

    def updateScreen(self):
        if self.__selectedFile:
            if not self.__selectedFile.lower().endswith('.mclevel'):
                self.__selectedFile += '.mclevel'

            self._openFile(self.__selectedFile)
            self.__selectedFile = ''
            self.mc.displayGuiScreen(None)

    def _setLevels(self, levels):
        for i in range(5):
            self._controlList[i].enabled = levels[i] != '-'
            self._controlList[i].displayString = levels[i]
            self._controlList[i].visible = True

        self._controlList[5].visible = True

    def _getLevelFile(self, slot):
        return os.path.join(self.mc.mcDataDir, 'saves', f'level{slot}.mclevel')

    def _getLevels(self):
        return [f'World {i + 1}' if os.path.isfile(self._getLevelFile(i)) else '-'
                for i in range(5)]

    def initGui(self):
        for i in range(5):
            self._controlList.append(GuiButton(i, self.width // 2 - 100,
                                               self.height // 6 + i * 24, '---'))
            self._controlList[i].visible = False

        self._controlList.append(GuiButton(5, self.width // 2 - 100,
                                           self.height // 6 + 120 + 12, 'Load file...'))
        self._controlList.append(GuiButton(6, self.width // 2 - 100,
                                           self.height // 6 + 168, 'Cancel'))
        self._controlList[5].visible = False

        self._setLevels(self._getLevels())
        self.__loaded = True

    def _actionPerformed(self, button):
        if self.__frozen or not button.enabled:
            return

        if self.__loaded and button.id < 5:
            self._openLevel(button.id)
        elif self.__finished or self.__loaded and button.id == 5:
            self.__frozen = True
            GuiLevelDialog(self).run()
        elif self.__finished or self.__loaded and button.id == 6:
            self.mc.displayGuiScreen(self.__parent)

    def _openLevel(self, id_):
        self._openFile(self._getLevelFile(id_))
        self.mc.displayGuiScreen(None)

    def drawScreen(self, xm, ym, renderPartialTicks):
        self.drawDefaultBackground()
        self.drawCenteredString(self._fontRenderer, self._title, self.width // 2, 20, 0xFFFFFF)
        if not self.__loaded:
            self.drawCenteredString(self._fontRenderer, self.__status, self.width // 2, self.height // 2 - 4, 0xFFFFFF)

        super().drawScreen(xm, ym, renderPartialTicks)

    def _openFile(self, file):
        world = PlayerLoader(self.mc, self.mc.loadingScreen).load(file)
        self.mc.setLevel(world)

    def setFile(self, file):
        self.__selectedFile = file

    def setFrozen(self, frozen):
        self.__frozen = False
