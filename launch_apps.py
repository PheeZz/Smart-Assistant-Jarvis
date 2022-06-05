import pyautogui as pag
import path_finder as pf
from time import sleep
import subprocess
from os import startfile
import threading
import pygetwindow as gw
import webbrowser as webbr
# function to find the button on the screen
paths = pf.get_path_info()


def get_image_coordinates(img, gray=True):
    try:
        coordinates = pag.locateCenterOnScreen(
            img, grayscale=gray, confidence=0.9)
        if coordinates is None:
            pf.logging.warning(f"{img} not found")
        else:
            pf.logging.info(
                f"{img} coordinates found successfully: {coordinates}")
            return coordinates
    except Exception as e:
        pf.logging.error(e)
        return False


def click_button(img):
    is_none = True
    while is_none:
        try:
            x, y = get_image_coordinates(img)
            if x is not None:
                pag.moveTo(x, y)
                sleep(0.05)
                pag.click()
                is_none = False
        except Exception as e:
            pf.logging.error(e)
            sleep(0.5)
    pf.logging.info(f"{img} clicked successfully")


def is_launched(app):
    if app is 'update':
        app = 'discord'

    if len(gw.getWindowsWithTitle(app)) == 0:
        return False
    else:
        return True


def util_launch(app):  # в threading.Thread нельзя передать длинный неитерируемый объект, т.е путь (костыль, че сказать)
    startfile(paths[app])


def launch_app(app):
    threading.Thread(target=util_launch, args=(app)).start()


def game_protocol():
    apps = ('steam', 'update')
    for app in apps:
        if not is_launched(app):
            launch_app(app)
            if app == 'update':
                app = 'discord'
            sleep(1)
    webbr.open_new_tab('https://music.yandex.ru/home')
    not_music_started = True
    while not_music_started:
        try:
            if len(gw.getWindowsWithTitle('Музыка')) != 0:
                gw.getWindowsWithTitle('Музыка')[0].activate()
                click_button('assets/browser/my_wave.png')
                not_music_started = False
                gw.getActiveWindow().minimize()
        except Exception as e:
            pf.logging.error(e)
            sleep(0.5)


def launch_overwolf():
    '''
    запуск овервульфа
    '''
    startfile(paths['overwolf'])
    while len(gw.getWindowsWithTitle('overwolf')) > 0:
        gw.getWindowsWithTitle('overwolf')[0].activate()
        sleep(0.5)


def launch_dota():
    '''
    запуск доты через овервульф
    '''
    startfile(paths['steam'])
    threading.Thread(target=launch_overwolf).start()

    click_button('assets/overwolf/login.png')
    click_button('assets/overwolf/launch.png')


def accept_game():
    '''
    автопринятие каточки
    '''
    click_button('assets/dota2/accept.png')
