import platform
import os
from webbrowser import get
import yaml
import logging
import datetime

from pprint import pprint

#Update = Discord
apps = ('steam', 'Overwolf', 'dota2', 'csgo',
        'Telegram', 'Update', 'EpicGamesLauncher', 'chrome')


def get_Datetime():
    now = datetime.datetime.now()
    pretty_str = now.strftime("%d.%m.%Y_%H.%M.%S")
    return pretty_str


logging.basicConfig(
    level=logging.DEBUG,
    filename=f"logs/{get_Datetime()}.log",
    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
)


def getSystem():
    if platform.system() == "Windows":
        return 'Windows'
    elif platform.system() == "Darwin":
        return 'Mac'
    elif platform.system() == "Linux":
        return 'Linux'
    else:
        return 'Unknown'


def find_path(name, path="\\"):
    for dirpath, dirname, filenames in os.walk(path):
        if name in filenames:
            return os.path.join(dirpath, name)


def get_path_info():
    try:
        with open('settings.yaml', 'r') as stream:
            pass
    except FileNotFoundError:
        with open('settings.yaml', 'w+') as stream:
            stream.write('{}')
    finally:
        with open('settings.yaml', 'r') as stream:
            try:
                paths = yaml.full_load(stream)
                logging.info("Paths from .yaml loaded successfully")
            except yaml.YAMLError as exc:
                logging.error(exc)
    return paths


def set_path_info(data):
    if not get_path_info():
        settings = {}
    else:
        settings = get_path_info()
    settings.update(data)
    with open('settings.yaml', 'w+') as outfile:
        yaml.dump(settings, stream=outfile)


def to_r_string(path):
    return f'r"{path}"'


def find_app_path(app):
    try:
        drives = ('C:\\', 'D:\\', 'E:\\', 'F:\\', 'G:\\', 'H:\\')
        for drive in drives:
            path = find_path(f'{app}.exe', path=drive)
            if path:
                break
        path = "\"" + path + "\""
        adder = {app.lower(): path}
        pprint(adder)
        logging.info(f"{app} path found successfully")
        logging.info(adder)
        return adder
    except:
        logging.error("App not found")


def set_paths():
    for app in apps:
        set_path_info(find_app_path(app))


def check_for_values_in_path():
    try:
        if len(apps) > len(get_path_info()):
            print('Перенастраиваю пути до новых приложений...')
            set_paths()
    except TypeError:
        set_paths()


check_for_values_in_path()
