from time import sleep
import pyautogui as pag
import pyperclip

sleep(5)
pyperclip.copy('@')

pag.FAILSAFE = True


while True:
    pag.hotkey('ctrl', 'v')
    pag.write("xxxTris")
    pag.press("Enter")
    pag.press("Enter")
