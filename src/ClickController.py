import threading
import time
import pyautogui
import random


class ClickController:
    shouldStop = False
    numberOfClicks = 0

    def start(settings: dict):
        ClickController.shouldStop = False
        ClickController.numberOfClicks = 0
        startTime = time.time()
        threading.Thread(target=ClickController._runClicks, args=[settings], daemon=True).start()
        print("Dispatched threads in", time.time() - startTime, "seconds")

    def stop():
        ClickController.shouldStop = True

    def _runClicks(settings):
        processStartTime = time.time()
        while not ClickController.shouldStop:
            startedWaitingAt = time.time()
            humanRandomizationFactor = 0
            if settings["humanRandomize"]:
                humanRandomizationFactor = (random.random() * 2) - 1

            while time.time() - startedWaitingAt < settings["waitTime"] + humanRandomizationFactor and not ClickController.shouldStop:
                continue
            
            if ClickController.shouldStop: return

            if settings["key"] == "Left Click" or settings["key"] == "Right Click" or settings["key"] == "Middle Click":
                position = pyautogui.position()

                if settings["fixedPos"]:
                    position = pyautogui.Point(settings["locationX"], settings["locationY"])

                if settings["clickType"] == "Single Click":
                    pyautogui.click(button=ClickController._getMouseButtonMap(settings["key"]), x=position.x, y=position.y)
                elif settings["clickType"] == "Double Click":
                    pyautogui.doubleClick(button=ClickController._getMouseButtonMap(settings["key"]), x=position.x, y=position.y)
                elif settings["clickType"] == "Tripple Click":
                    pyautogui.tripleClick(button=ClickController._getMouseButtonMap(settings["key"]), x=position.x, y=position.y)

            else:
                pyautogui.press(settings["key"])
            
            ClickController.numberOfClicks += 1

            if settings["limitRepeats"]:
                if settings["repeatMode"] == "clicks":
                    if ClickController.numberOfClicks > settings["repeatClicks"]: ClickController.stop()
                elif settings["repeatMode"] == "duration":
                    if time.time() - processStartTime > settings["durationLimit"]: ClickController.stop()
                
    

    def _getMouseButtonMap(value):
        if value == "Left Click":
            return "left"
        if value == "Right Click":
            return "right"
        if value == "Middle Click":
            return "middle"
