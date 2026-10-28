from mc.net.minecraft.client.gui.GuiScreen import GuiScreen
from pyglet import window


class GuiChat(GuiScreen):

    def __init__(self):
        self.__message = ''
        self.__counter = 0

    def _keyTyped(self, key, char, motion):
        if key in (window.key.ENTER, window.key.NUM_ENTER):
            message = self.__message.strip()
            if message:
                result = self.mc.executeCommand(message)
                self.mc.ingameGUI.addChatMessage(result)

            self.mc.displayGuiScreen(None)
            return

        if motion == window.key.MOTION_BACKSPACE:
            self.__message = self.__message[:-1]
        elif char and char.isprintable():
            self.__message += char

        super()._keyTyped(key, char, motion)

    def updateScreen(self):
        self.__counter += 1

    def drawScreen(self, xm, ym, renderPartialTicks):
        self.drawDefaultBackground()
        self._drawRect(1, self.height - 15, self.width - 1, self.height - 2,
                       -16777216)
        cursor = '_' if self.__counter // 6 % 2 == 0 else ''
        self.drawString(
            self._fontRenderer,
            '>' + self.__message + cursor,
            4, self.height - 12, 0xFFFFFF
        )
