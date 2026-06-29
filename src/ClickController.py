import time
import pyautogui
import random
import datetime


class ClickController:
    shouldStop = True
    numberOfClicks = 0

    _root = None
    _settings = None
    _processStartTime = None
    _afterId = None

    @staticmethod
    def start(root, settings: dict):
        ClickController.shouldStop = False
        ClickController.numberOfClicks = 0
        ClickController._root = root
        ClickController._settings = settings
        ClickController._processStartTime = time.time()
        ClickController._scheduleNext()

    @staticmethod
    def stop():
        ClickController.shouldStop = True
        if ClickController._afterId is not None:
            try:
                ClickController._root.after_cancel(ClickController._afterId)
            except Exception:
                pass
            ClickController._afterId = None

    @staticmethod
    def _scheduleNext():
        if ClickController.shouldStop:
            return
        waitMs = int(ClickController._settings["waitTime"] * 1000)
        if ClickController._settings["humanRandomize"]:
            waitMs += int((random.random() * 2 - 1) * 1000)
        waitMs = max(0, waitMs)
        ClickController._afterId = ClickController._root.after(waitMs, ClickController._doClick)

    @staticmethod
    def _doClick():
        if ClickController.shouldStop:
            return

        s = ClickController._settings

        if s["key"] in ("Left Click", "Right Click", "Middle Click"):
            position = pyautogui.position()
            if s["fixedPos"]:
                position = pyautogui.Point(s["locationX"], s["locationY"])
            if s["humanRandomize"]:
                position = pyautogui.Point(position.x + random.randint(-1, 1), position.y + random.randint(-1, 1))
            btn = ClickController._getMouseButtonMap(s["key"])

            if s["hold"]:
                pyautogui.mouseDown(button=btn, x=position.x, y=position.y)
                ClickController._afterId = ClickController._root.after(
                    s["holdMs"],
                    lambda: ClickController._finishMouseHold(btn, position)
                )
                return
            else:
                if s["clickType"] == "Single Click":
                    pyautogui.click(button=btn, x=position.x, y=position.y)
                elif s["clickType"] == "Double Click":
                    pyautogui.doubleClick(button=btn, x=position.x, y=position.y)
                elif s["clickType"] == "Tripple Click":
                    pyautogui.tripleClick(button=btn, x=position.x, y=position.y)
        else:
            if s["hold"]:
                pyautogui.keyDown(s["key"])
                ClickController._afterId = ClickController._root.after(
                    s["holdMs"],
                    lambda: ClickController._finishKeyHold(s["key"])
                )
                return
            else:
                pyautogui.press(s["key"])

        ClickController._incrementAndSchedule()

    @staticmethod
    def _finishMouseHold(btn, position):
        pyautogui.mouseUp(button=btn, x=position.x, y=position.y)
        ClickController._incrementAndSchedule()

    @staticmethod
    def _finishKeyHold(key):
        pyautogui.keyUp(key)
        ClickController._incrementAndSchedule()

    @staticmethod
    def _incrementAndSchedule():
        ClickController.numberOfClicks += 1
        s = ClickController._settings

        if s["limitRepeats"]:
            if s["repeatMode"] == "clicks":
                if ClickController.numberOfClicks >= s["repeatClicks"]:
                    ClickController.stop()
                    return
            elif s["repeatMode"] == "duration":
                if time.time() - ClickController._processStartTime >= s["durationLimit"]:
                    ClickController.stop()
                    return
            elif s["repeatMode"] == "datetime":
                stopDt = datetime.datetime(
                    s["stopYear"], s["stopMonth"], s["stopDay"],
                    s["stopHour"], s["stopMinute"], s["stopSecond"]
                )
                if datetime.datetime.now() >= stopDt:
                    ClickController.stop()
                    return

        ClickController._scheduleNext()

    @staticmethod
    def _getMouseButtonMap(value):
        if value == "Left Click": return "left"
        if value == "Right Click": return "right"
        if value == "Middle Click": return "middle"
