import config
import sound_to_text
#import text_to_sound
from pydub import AudioSegment
from pydub.playback import play
from fuzzywuzzy import fuzz
import webbrowser
import random
import path_finder as pf
import launch_apps as launch
import os


def clearConsole(): return os.system(
    'cls' if os.name in ('nt', 'dos') else 'clear')


answers = {
    'yes': {
        'yes_one': 'jarvis_voice/Да сэр.wav',
        'yes_two': 'jarvis_voice/Да сэр(второй).wav',
        'affirmative': 'jarvis_voice/Есть.wav',
        'at_your_service': 'jarvis_voice/К вашим услугам сэр.wav'
    },
    'other': {
        'loading': 'jarvis_voice/Загружаю сэр.wav',
        'request completed': 'jarvis_voice/Запрос выполнен сэр.wav',
        'negative': 'jarvis_voice/Чего вы пытаетесь добиться сэр.wav',
        'wakeup': 'jarvis_voice/Доброе утро.wav',
        'sleep': 'jarvis_voice/Отключаю питание.wav',
        'all_for_you': 'jarvis_voice/Всегда к вашим услугам сэр.wav',
        'ready': 'jarvis_voice/Мы подключены и готовы.wav',
        'reserve_power': 'jarvis_voice/Включилось аварийное резервное питание.wav',
        'funny': 'jarvis_voice/О чем я думал, обычно у нас все веселенькое.wav'
    }
}


def get_random_yes_answer():
    keys = tuple(answers['yes'].keys())
    return random.choice(keys)


def play_yes_answer():
    sound = AudioSegment.from_file(answers['yes'][get_random_yes_answer()])
    sound = change_volume(sound)
    play(sound)


def va_respond(voice: str):
    print(voice)
    global is_sleep_mode
    is_sleep_mode = False
    if voice.startswith(config.VA_ALIAS):
        # обращаются к ассистенту
        cmd = recognize_cmd(filter_cmd(voice))

        if cmd['cmd'] not in config.VA_CMD_LIST.keys():
            play(change_volume(AudioSegment.from_file(
                answers['other']['negative'])))

        elif cmd['cmd'] == 'sleep':
            is_sleep_mode = True
            pf.logging.info("Sleep mode activated")
            play(change_volume(AudioSegment.from_file(
                answers['other']['sleep'])))

        elif cmd['cmd'] == 'wakeup':
            is_sleep_mode = False
            pf.logging.info("Jarvis is awake")
            play(change_volume(AudioSegment.from_file(
                answers['other']['wakeup'])))

        else:
            execute_cmd(cmd['cmd'], is_sleep_mode)


def filter_cmd(raw_voice: str):
    cmd = raw_voice
    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()
    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()

    return cmd


def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in config.VA_CMD_LIST.items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt

    return rc


def change_volume(sound):  # изменение громкости звука на -30
    if int(sound.dBFS) > -30:  # .dBFS возвращает громкость в дБ
        while int(sound.dBFS) > -30:
            sound = sound.apply_gain(-1)
    elif int(sound.dBFS) < -30:
        while int(sound.dBFS) < -30:
            sound = sound.apply_gain(+1)
    return sound


print(f"{clearConsole()}\n{config.VA_NAME} (v{config.VA_VER}) начал свою работу ...")
play(change_volume(AudioSegment.from_file(answers['other']['wakeup'])))


def execute_cmd(cmd: str, is_sleep_mode: bool):  # настройка выполнения команд и ответов

    if cmd == 'check_mode':
        if is_sleep_mode:
            play(change_volume(AudioSegment.from_file(
                answers['other']['reserve_power'])))
        else:
            play(change_volume(AudioSegment.from_file(
                answers['other']['ready'])))

    elif cmd == 'dota' and not is_sleep_mode:
        play_yes_answer()
        launch.launch_dota()
        pf.logging.info("Dota 2 started successfully")

    elif cmd == 'open_browser' and not is_sleep_mode:
        play_yes_answer()
        webbrowser.open_new_tab('https://www.google.com/')
        pf.logging.info("Browser opened successfully")

    elif cmd == 'accept_game' and not is_sleep_mode:
        play_yes_answer()
        launch.accept_game()
        pf.logging.info("Game accepter started successfully")

    elif cmd == 'game_protocol':
        play(change_volume(AudioSegment.from_file(answers['other']['funny'])))
        launch.game_protocol()
        pf.logging.info("Game protocol activated successfully")


def __main__():
    pf.check_for_values_in_path()
    # начать прослушивание команд
    sound_to_text.va_listen(va_respond)


__main__()
